// Helpers used to edit the report and semantic model as code through the Fabric REST API.
// Run in the browser console of a signed-in app.fabric.microsoft.com tab (the page exposes
// window.powerBIAccessToken). Nothing here contains a secret; the token never leaves the page.
//
// Pattern: def = await fab.getAny('reports', fab.rid)   -> { parts: [{ path, payload(base64) }] }
//          edit the decoded JSON / TMDL of the parts you need
//          await fab.putAny('reports', fab.rid, def.parts)
// A long-running-operation result of 400 "OperationHasNoResult" after a 202 means the update succeeded.
// Workspace and item ids are for the tft-dev workspace.
window.fab = {
  ws: '6fc0ae0f-a1c1-485e-b7c3-0022d860b8a8',
  rid: '92794f35-4986-4e37-935f-173abf578c2e',   // report: Treasury Forecast Tracker
  ds: '68cf5727-e77f-4361-ba33-7c4c286b0464',    // semantic model: sm_forecast_tracker_public
  hdr() { return { Authorization: 'Bearer ' + window.powerBIAccessToken, 'Content-Type': 'application/json' }; },
  async lro(r) {
    if (r.status !== 202) return r;
    const id = r.headers.get('x-ms-operation-id');
    for (let i = 0; i < 40; i++) {
      await new Promise(s => setTimeout(s, 2500));
      const j = await (await fetch('https://api.fabric.microsoft.com/v1/operations/' + id, { headers: this.hdr() })).json();
      if (j.status === 'Succeeded') return fetch('https://api.fabric.microsoft.com/v1/operations/' + id + '/result', { headers: this.hdr() });
      if (j.status === 'Failed') return { status: 'FAILED', text: async () => JSON.stringify(j) };
    }
    return { status: 'TIMEOUT', text: async () => 'timeout' };
  },
  async getAny(kind, id) {   // kind: 'reports' | 'semanticModels'
    const url = `https://api.fabric.microsoft.com/v1/workspaces/${this.ws}/${kind}/${id}/getDefinition` + (kind === 'semanticModels' ? '?format=TMDL' : '');
    const r = await this.lro(await fetch(url, { method: 'POST', headers: this.hdr() }));
    const j = JSON.parse(await r.text());
    return j.definition || j;
  },
  async putAny(kind, id, parts) {
    const body = { definition: { parts: parts.filter(p => p.path !== '.platform').map(p => ({ path: p.path, payload: p.payload, payloadType: p.payloadType || 'InlineBase64' })) } };
    const r0 = await fetch(`https://api.fabric.microsoft.com/v1/workspaces/${this.ws}/${kind}/${id}/updateDefinition`, { method: 'POST', headers: this.hdr(), body: JSON.stringify(body) });
    const r = await this.lro(r0);
    return 'post ' + r0.status + ' -> ' + r.status + ' ' + (await r.text()).slice(0, 300);
  },
  dec(p) { return new TextDecoder().decode(Uint8Array.from(atob(p), c => c.charCodeAt(0))); },
  enc(s) { const b = new TextEncoder().encode(s); let bin = ''; for (let i = 0; i < b.length; i += 8192) bin += String.fromCharCode.apply(null, b.subarray(i, i + 8192)); return btoa(bin); },
  async dax(q) {             // run a DAX query against the model without changing it
    const r = await fetch(`https://api.powerbi.com/v1.0/myorg/groups/${this.ws}/datasets/${this.ds}/executeQueries`, { method: 'POST', headers: this.hdr(), body: JSON.stringify({ queries: [{ query: q }], serializerSettings: { includeNulls: true } }) });
    return { status: r.status, t: await r.text() };
  },
  async refresh() {          // refresh the import model
    const r = await fetch(`https://api.powerbi.com/v1.0/myorg/groups/${this.ws}/datasets/${this.ds}/refreshes`, { method: 'POST', headers: this.hdr(), body: JSON.stringify({ notifyOption: 'NoNotification' }) });
    return r.status;         // 202 = accepted
  }
};
