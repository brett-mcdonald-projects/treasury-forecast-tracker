# Treasury Forecast Tracker - ingest and transform
# Fabric PySpark notebook. Attach lakehouse lh_tft as the default lakehouse, then Run all.
# Flow: probe sources -> hash -> land raw file if new/changed -> parse -> star schema -> tests.

import hashlib, io, os, re, datetime as dt
import pandas as pd
import requests

FORCE_REBUILD = False   # True = rebuild tables even if no source changed
BASE = "https://budget.govt.nz/budget/excel"
LANDING = "/lakehouse/default/Files/landing"

# ---- Source registry: one row per forecast round. A new round = one new row. ----
REGISTRY = [
    # code,      name,                               order, url
    ("HYEFU25", "Half Year Update 2025",              1, f"{BASE}/hyefu2025/hyefu25-economic-forecasts-data.xlsx"),
    ("BEFU26",  "Budget Update 2026",                 2, f"{BASE}/befu2026/befu26-economic-forecasts-data.xlsx"),
    ("PREFU26", "Pre-election Update 2026",           3, f"{BASE}/prefu2026/prefu26-economic-forecasts-data.xlsx"),
    ("HYEFU26", "Half Year Update 2026",              4, f"{BASE}/hyefu2026/hyefu26-economic-forecasts-data.xlsx"),
]
registry_df = pd.DataFrame(REGISTRY, columns=["round_code", "round_name", "round_order", "url"])

# ---------------------------------------------------------------- parsing
LABELS = ["Description", "Source", "Units", "Magnitude", "Type", "ID"]

def _period(v):
    """Return (label, period_end date) for a quarterly 'YYYYQn' label or a June-year date; else None."""
    if isinstance(v, (dt.datetime, dt.date, pd.Timestamp)):
        d = pd.Timestamp(v).date()
        return (f"{d.year - 1}/{str(d.year)[2:]}", d)      # June year, e.g. 2025/26
    m = re.fullmatch(r"(\d{4})Q([1-4])", str(v).strip())
    if m:
        y, q = int(m.group(1)), int(m.group(2))
        d = (pd.Timestamp(year=y, month=q * 3, day=1) + pd.offsets.MonthEnd(0)).date()
        return (f"{y}Q{q}", d)
    return None

def parse_sheet(raw, domain):
    """raw: DataFrame read with header=None. Returns (series_df, long_df)."""
    meta = {str(raw.iat[i, 0]).strip(): i for i in range(len(raw)) if str(raw.iat[i, 0]).strip() in LABELS}
    desc = raw.iloc[meta["Description"]]
    ids = raw.iloc[meta["ID"]]
    flag_col = next((c for c in raw.columns if str(desc[c]).strip().lower() == "is forecast"), None)
    cols = [c for c in raw.columns[1:] if pd.notna(ids[c]) and c != flag_col]

    def m(label, c):
        return str(raw.iat[meta[label], c]).strip() if label in meta and pd.notna(raw.iat[meta[label], c]) else None

    series = pd.DataFrame([{
        "series_id": str(ids[c]).strip(), "series_name": str(desc[c]).strip(), "domain": domain,
        "source": m("Source", c), "units": m("Units", c), "magnitude": m("Magnitude", c), "adjustment": m("Type", c),
    } for c in cols])

    recs = []
    for i in range(len(raw)):
        p = _period(raw.iat[i, 0])
        if p is None:
            continue
        flag = raw.iat[i, flag_col] if flag_col is not None else None
        for c in cols:
            v = pd.to_numeric(raw.iat[i, c], errors="coerce")
            if pd.notna(v):
                recs.append((str(ids[c]).strip(), domain, p[0], p[1], None if flag is None or pd.isna(flag) else bool(flag), float(v)))
    long = pd.DataFrame(recs, columns=["series_id", "domain", "period_label", "period_end", "is_forecast", "value"])
    return series, long

def parse_workbook(content, round_code):
    sheets = pd.read_excel(io.BytesIO(content), sheet_name=None, header=None, engine="openpyxl")
    out_s, out_l = [], []
    for name, raw in sheets.items():
        domain = "Fiscal" if "fiscal" in name.lower() else "Economic"
        s, l = parse_sheet(raw, domain)
        l.insert(0, "round_code", round_code)
        out_s.append(s); out_l.append(l)
    return pd.concat(out_s, ignore_index=True), pd.concat(out_l, ignore_index=True)

def flag_economic_forecast(fact):
    """The economic sheet has no forecast flag. Published CPI is a whole-number index and forecasts
    are not, so the last whole-number CPI quarter in each round marks the last actual quarter."""
    fact = fact.copy()
    cpi = fact[fact.series_id == "pcpiq"]
    last_actual = cpi[(cpi.value % 1).abs() < 1e-9].groupby("round_code")["period_end"].max().to_dict()
    eco = fact.domain == "Economic"
    fact.loc[eco, "is_forecast"] = [pe > last_actual[rc] for rc, pe in zip(fact.loc[eco, "round_code"], fact.loc[eco, "period_end"])]
    fact["is_forecast"] = fact["is_forecast"].astype(bool)
    return fact

# ---------------------------------------------------------------- headline measures
def build_headline(fact):
    """Derived measures used by the report. fact = long table for all rounds."""
    def s(sid):
        return fact[fact.series_id == sid][["round_code", "period_label", "period_end", "is_forecast", "value"]]
    out = []

    def add(df, measure, group, unit, sort):
        d = df.dropna(subset=["value"]).copy()
        d["measure"], d["measure_group"], d["unit"], d["measure_sort"] = measure, group, unit, sort
        out.append(d)

    def annual_pct(sid):   # quarter on same quarter a year earlier
        d = s(sid).sort_values(["round_code", "period_end"]).copy()
        d["value"] = d.groupby("round_code")["value"].pct_change(4) * 100
        return d

    add(annual_pct("ngdpp_zq"), "Real GDP growth", "Economic", "Annual % change", 1)
    add(annual_pct("pcpiq"), "CPI inflation", "Economic", "Annual % change", 2)
    add(s("lhurzq"), "Unemployment rate", "Economic", "% of labour force", 3)

    gdp = s("nznaac0317_fisc")[["round_code", "period_end", "value"]].rename(columns={"value": "gdp"})
    def pct_gdp(sid):
        d = s(sid).merge(gdp, on=["round_code", "period_end"], how="inner")
        d["value"] = d["value"] / d["gdp"] * 100
        return d.drop(columns="gdp")

    add(s("nzgpfiobegalexacc"), "OBEGAL (excluding ACC)", "Fiscal", "$ million", 4)
    add(pct_gdp("nzgpfiobegalexacc"), "OBEGAL (excluding ACC), % of GDP", "Fiscal", "% of GDP", 5)
    add(pct_gdp("nzgpfi0024"), "Net core Crown debt, % of GDP", "Fiscal", "% of GDP", 6)
    add(pct_gdp("nzgpfi0001"), "Core Crown expenses, % of GDP", "Fiscal", "% of GDP", 7)
    add(pct_gdp("nzgpfi0017"), "Core Crown tax revenue, % of GDP", "Fiscal", "% of GDP", 8)
    return pd.concat(out, ignore_index=True)

def build_revisions(headline, rounds):
    """Latest round minus the previous round, for periods both cover."""
    order = rounds.sort_values("round_order")["round_code"].tolist()
    if len(order) < 2:
        return pd.DataFrame(columns=["measure", "measure_group", "unit", "measure_sort", "period_label", "period_end",
                                     "previous_round", "latest_round", "previous_value", "latest_value", "is_forecast", "revision"])
    prev, last = order[-2], order[-1]
    keys = ["measure", "measure_group", "unit", "measure_sort", "period_label", "period_end"]
    a = headline[headline.round_code == prev][keys + ["value"]].rename(columns={"value": "previous_value"})
    b = headline[headline.round_code == last][keys + ["value", "is_forecast"]].rename(columns={"value": "latest_value"})
    r = a.merge(b, on=keys, how="inner")
    r["previous_round"], r["latest_round"] = prev, last
    r["revision"] = r["latest_value"] - r["previous_value"]
    return r

def run_tests(dim_series, fact, headline):
    t = []
    def check(name, ok, detail=""):
        t.append({"test": name, "passed": bool(ok), "detail": str(detail)})
    check("fact has rows", len(fact) > 0, len(fact))
    check("no duplicate fact keys", not fact.duplicated(["round_code", "series_id", "period_end"]).any())
    check("no null values in fact", fact["value"].notna().all())
    check("every fact series is in dim_series", set(fact.series_id) <= set(dim_series.series_id))
    need = {"ngdpp_zq", "pcpiq", "lhurzq", "nzgpfiobegalexacc", "nzgpfi0024", "nznaac0317_fisc"}
    check("headline source series present in every round",
          all(need <= set(g.series_id) for _, g in fact.groupby("round_code")), sorted(need))
    q = fact[(fact.domain == "Economic") & (fact.series_id == "ngdpp_zq")]
    gaps = q.groupby("round_code")["period_end"].apply(lambda x: (pd.to_datetime(x).sort_values().diff().dt.days.dropna() > 93).sum()).sum()
    check("quarterly GDP series has no gaps", gaps == 0, gaps)
    check("forecast flag set on every row", fact["is_forecast"].isin([True, False]).all())
    check("unemployment rate within 0-20%", headline[headline.measure == "Unemployment rate"]["value"].between(0, 20).all())
    return pd.DataFrame(t)

# ================================================================ Fabric run (skipped when imported for local testing)
if "spark" in globals():
    from pyspark.sql import functions as F
    run_ts = dt.datetime.utcnow()
    os.makedirs(LANDING, exist_ok=True)

    try:
        prev_log = spark.table("ingest_log").toPandas()
    except Exception:
        prev_log = pd.DataFrame(columns=["round_code", "sha256", "status", "run_ts"])
    last_hash = (prev_log[prev_log.status.isin(["loaded", "unchanged"])].sort_values("run_ts")
                 .groupby("round_code")["sha256"].last().to_dict())

    log, contents = [], {}
    for code, name, order, url in REGISTRY:
        entry = {"run_ts": run_ts, "round_code": code, "url": url, "http_status": None, "sha256": None,
                 "bytes": None, "landing_path": None, "status": None}
        content = None
        try:
            r = requests.get(url, timeout=60, headers={"User-Agent": "Mozilla/5.0 (treasury-forecast-tracker demo)"})
            entry["http_status"] = r.status_code
            if r.status_code == 200 and r.content[:2] == b"PK":
                content = r.content
            else:
                entry["status"] = "not_published"
        except Exception as e:
            entry["status"] = f"fetch_failed: {type(e).__name__}"
        manual = f"{LANDING}/manual/{url.rsplit('/', 1)[-1]}"      # fallback: file uploaded by hand
        if content is None and os.path.exists(manual):
            content = open(manual, "rb").read(); entry["status"] = None; entry["url"] = "manual upload: " + manual
        if content is not None:
            h = hashlib.sha256(content).hexdigest()
            entry["sha256"], entry["bytes"] = h, len(content)
            if last_hash.get(code) == h:
                entry["status"] = "unchanged"
            else:
                folder = f"{LANDING}/{code}/{run_ts:%Y%m%dT%H%M%SZ}"
                os.makedirs(folder, exist_ok=True)
                path = f"{folder}/{url.rsplit('/', 1)[-1]}"
                open(path, "wb").write(content)
                entry["landing_path"], entry["status"] = path.replace("/lakehouse/default/", ""), "loaded"
            contents[code] = content
        log.append(entry)

    log_df = pd.DataFrame(log)
    print(log_df[["round_code", "http_status", "status", "bytes"]].to_string(index=False))
    changed = (log_df.status == "loaded").any()

    def save(pdf, name, mode="overwrite"):
        sdf = spark.createDataFrame(pdf)
        for c in ("period_end",):
            if c in pdf.columns:
                sdf = sdf.withColumn(c, F.col(c).cast("date"))
        sdf.write.mode(mode).option("overwriteSchema", "true").format("delta").saveAsTable(name)
        print(f"saved {name}: {len(pdf)} rows")

    log_out = log_df.astype({"http_status": "float", "bytes": "float"})
    for c in ("sha256", "landing_path", "status", "url"):
        log_out[c] = log_out[c].astype("string").fillna("")
    save(log_out, "ingest_log", mode="append")
    save(registry_df, "source_registry")

    if changed or FORCE_REBUILD:
        series_parts, fact_parts = [], []
        for code, content in contents.items():
            s_, l_ = parse_workbook(content, code)
            series_parts.append(s_); fact_parts.append(l_)
        dim_series = pd.concat(series_parts).drop_duplicates("series_id", keep="last").reset_index(drop=True).fillna("")
        fact = flag_economic_forecast(pd.concat(fact_parts, ignore_index=True))
        dim_round = registry_df[registry_df.round_code.isin(contents)][["round_code", "round_name", "round_order"]]
        headline = build_headline(fact).merge(dim_round, on="round_code")
        revisions = build_revisions(headline, dim_round)
        tests = run_tests(dim_series, fact, headline)
        tests["run_ts"] = run_ts
        print(tests[["test", "passed", "detail"]].to_string(index=False))
        if not tests.passed.all():
            save(tests, "test_results", mode="append")
            raise Exception("Data tests failed - tables not refreshed. See test_results.")
        save(dim_series, "dim_series"); save(dim_round, "dim_round")
        save(fact, "fact_forecast"); save(headline, "fact_headline"); save(revisions, "fact_revision")
        save(tests, "test_results", mode="append")
        print("DONE: tables refreshed.")
    else:
        print("No source changed since the last run - nothing to do.")
