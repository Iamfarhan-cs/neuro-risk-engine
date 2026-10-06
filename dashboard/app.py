"""Zero-dependency research dashboard for Neuro-Risk Engine.

Run from repository root:
    python dashboard/app.py

The dashboard reads structured experiment results from experiments/runs and
never executes models. It is intentionally a reporting layer so future tasks
can extend metrics without changing experiment logic.
"""

from __future__ import annotations

import json
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import urlparse

ROOT = Path(__file__).resolve().parents[1]
RUNS_DIR = ROOT / "experiments" / "runs"
HOST = "127.0.0.1"
PORT = 8501


def read_json(path: Path) -> dict:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return {}


def load_runs() -> list[dict]:
    if not RUNS_DIR.exists():
        return []
    runs = []
    for directory in sorted(p for p in RUNS_DIR.iterdir() if p.is_dir()):
        runs.append({
            "run_id": directory.name,
            "config": read_json(directory / "config.json"),
            "metrics": read_json(directory / "metrics.json"),
            "resources": read_json(directory / "resource_metrics.json"),
            "integrity": read_json(directory / "integrity.json"),
        })
    return runs


def model_rows(run: dict) -> list[dict]:
    models = run.get("metrics", {}).get("models", {})
    resources = run.get("resources", {}).get("models", {})
    rows = []
    for name, metrics in models.items():
        metrics = metrics if isinstance(metrics, dict) else {}
        resource = resources.get(name, {})
        resource = resource if isinstance(resource, dict) else {}
        rows.append({
            "run_id": run["run_id"], "model": name,
            "f1": metrics.get("f1"), "roc_auc": metrics.get("roc_auc"),
            "pr_auc": metrics.get("pr_auc"), "precision": metrics.get("precision"),
            "recall": metrics.get("recall"),
            "false_positive_rate": metrics.get("false_positive_rate"),
            "false_negative_rate": metrics.get("false_negative_rate"),
            "p95_latency_ms": resource.get("p95_latency_ms"),
            "parameters": resource.get("parameters"),
            "memory_mb": resource.get("memory_mb"),
            "events": resource.get("events"),
            "synaptic_operations": resource.get("synaptic_operations"),
        })
    return rows


def payload() -> dict:
    runs = load_runs()
    return {
        "runs": runs,
        "rows": [row for run in runs for row in model_rows(run)],
        "meta": {"dashboard_version": "0.1", "research_only": True},
    }


HTML = """<!doctype html>
<html><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Neuro-Risk Engine Research Dashboard</title>
<style>
:root{color-scheme:dark;--bg:#0b1020;--panel:#121a2e;--line:#273452;--text:#e8edf7;--muted:#93a0b8;--good:#70d6a1}
*{box-sizing:border-box}body{margin:0;background:var(--bg);color:var(--text);font-family:system-ui,sans-serif}
main{max-width:1400px;margin:auto;padding:28px}.header{display:flex;justify-content:space-between;gap:20px;margin-bottom:20px}
h1{margin:0 0 5px;font-size:28px}h2{font-size:17px}.muted{color:var(--muted)}
.badge{border:1px solid var(--line);border-radius:99px;padding:7px 12px;color:var(--good);font-size:12px}
.grid{display:grid;grid-template-columns:repeat(4,1fr);gap:12px}.panel{background:var(--panel);border:1px solid var(--line);border-radius:12px;padding:17px;margin-bottom:12px}
.value{font-size:24px;font-weight:700}.label{font-size:11px;color:var(--muted);text-transform:uppercase}
.toolbar{display:flex;gap:8px;flex-wrap:wrap}select,button{background:#0d1528;color:var(--text);border:1px solid var(--line);border-radius:8px;padding:9px 11px}
.table{overflow:auto}table{width:100%;border-collapse:collapse;font-size:13px}th,td{padding:9px;border-bottom:1px solid var(--line);text-align:right;white-space:nowrap}th:first-child,td:first-child{text-align:left}th{color:var(--muted)}
canvas{width:100%;height:260px}.controls{display:grid;grid-template-columns:repeat(3,1fr);gap:8px}.control{border:1px solid var(--line);border-radius:8px;padding:11px}.pass{color:var(--good)}
@media(max-width:850px){.grid{grid-template-columns:repeat(2,1fr)}.controls{grid-template-columns:1fr}}@media(max-width:550px){main{padding:14px}.grid{grid-template-columns:1fr}.header{display:block}}
</style></head><body><main>
<div class="header"><div><h1>Neuro-Risk Engine</h1><div class="muted">Research evaluation dashboard — results only; no model execution.</div></div><div class="badge">SYNTHETIC / RESEARCH ONLY</div></div>

<div class="grid">
<div class="panel"><div class="label">Best F1</div><div class="value" id="f1">—</div></div>
<div class="panel"><div class="label">Best ROC-AUC</div><div class="value" id="auc">—</div></div>
<div class="panel"><div class="label">Lowest P95 latency</div><div class="value" id="lat">—</div></div>
<div class="panel"><div class="label">Lowest recorded cost</div><div class="value" id="cost">—</div></div>
</div>

<div class="panel"><h2>Experiment selection</h2><div class="toolbar">
<select id="run"><option value="all">All runs</option></select><button onclick="location.reload()">Refresh</button>
</div></div>

<div class="panel"><h2>Model comparison</h2><div class="table"><table><thead><tr>
<th>Model</th><th>F1</th><th>ROC-AUC</th><th>PR-AUC</th><th>P95 ms</th><th>Params</th><th>Memory MB</th><th>Events</th><th>Synaptic ops</th>
</tr></thead><tbody id="rows"></tbody></table></div></div>

<div class="panel"><h2>Performance vs computational cost</h2><div class="muted">Only interpret after confirming matched information, training budget, sparsity, and topology controls.</div><canvas id="costChart"></canvas></div>
<div class="panel"><h2>Performance vs latency</h2><canvas id="latChart"></canvas></div>

<div class="panel"><h2>Experiment integrity</h2><div class="controls" id="integrity"></div></div>
<div class="panel"><h2>Scientific boundary</h2><div class="muted">The dashboard reports recorded measurements. It does not select topology, thresholds, features, hyperparameters, or models based on financial performance.</div></div>
</main>
<script>
var DATA={runs:[],rows:[]};
function fmt(v,d){return v===null||v===undefined||isNaN(Number(v))?"—":Number(v).toFixed(d===undefined?3:d)}
function safe(s){return String(s==null?"":s).replace(/[&<>"']/g,function(c){return {"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;","'":"&#39;"}[c]})}
function selected(){var r=document.getElementById("run").value;return DATA.rows.filter(function(x){return r==="all"||x.run_id===r})}
function best(rows,key,asc){var a=rows.filter(function(x){return x[key]!=null}).slice().sort(function(x,y){return (asc?1:-1)*(Number(x[key])-Number(y[key]))});return a[0]}
function render(){
 var rows=selected(), body=document.getElementById("rows");
 body.innerHTML=rows.length?rows.map(function(r){return "<tr><td>"+safe(r.model)+"</td><td>"+fmt(r.f1)+"</td><td>"+fmt(r.roc_auc)+"</td><td>"+fmt(r.pr_auc)+"</td><td>"+fmt(r.p95_latency_ms,2)+"</td><td>"+fmt(r.parameters,0)+"</td><td>"+fmt(r.memory_mb,1)+"</td><td>"+fmt(r.events,0)+"</td><td>"+fmt(r.synaptic_operations,0)+"</td></tr>"}).join(""):"<tr><td colspan=9 class=muted>No results yet. Add experiments/runs/<run_id>/metrics.json.</td></tr>";
 var f=best(rows,"f1"),a=best(rows,"roc_auc"),l=best(rows,"p95_latency_ms",true),c=best(rows,"synaptic_operations",true);
 document.getElementById("f1").textContent=f?f.model+" · "+fmt(f.f1):"—";
 document.getElementById("auc").textContent=a?a.model+" · "+fmt(a.roc_auc):"—";
 document.getElementById("lat").textContent=l?l.model+" · "+fmt(l.p95_latency_ms,2)+" ms":"—";
 document.getElementById("cost").textContent=c?c.model+" · "+fmt(c.synaptic_operations,0):"—";
 chart(document.getElementById("costChart"),rows,"synaptic_operations","F1");chart(document.getElementById("latChart"),rows,"p95_latency_ms","F1");integrity();
}
function chart(canvas,rows,xkey,ykey){
 var d=devicePixelRatio||1,w=canvas.clientWidth||800,h=260;canvas.width=w*d;canvas.height=h*d;var c=canvas.getContext("2d");c.scale(d,d);c.clearRect(0,0,w,h);c.font="12px system-ui";
 var p=rows.filter(function(r){return r[xkey]!=null&&r[ykey]!=null});if(!p.length){c.fillStyle="#93a0b8";c.fillText("No compatible results yet.",20,30);return}
 var xs=p.map(function(r){return +r[xkey]}),ys=p.map(function(r){return +r[ykey]}),xmin=Math.min.apply(null,xs),xmax=Math.max.apply(null,xs),ymin=Math.min.apply(null,ys),ymax=Math.max.apply(null,ys);
 var sx=function(v){return 55+(v-xmin)/((xmax-xmin)||1)*(w-90)},sy=function(v){return h-45-(v-ymin)/((ymax-ymin)||1)*(h-80)};
 c.strokeStyle="#273452";c.beginPath();c.moveTo(55,20);c.lineTo(55,h-45);c.lineTo(w-35,h-45);c.stroke();
 p.forEach(function(r,i){var x=sx(+r[xkey]),y=sy(+r[ykey]);c.fillStyle=i%2?"#72a7ff":"#70d6a1";c.beginPath();c.arc(x,y,5,0,Math.PI*2);c.fill();c.fillStyle="#e8edf7";c.fillText(r.model,x+8,y-6)});
}
function integrity(){
 var run=DATA.runs.filter(function(r){return r.run_id===document.getElementById("run").value})[0]||DATA.runs[0],checks=(run&&run.integrity&&run.integrity.checks)||{};
 var names=["same_split","same_information","synthetic_only","topology_frozen","no_performance_based_topology_selection","parameter_budget_recorded","sparsity_recorded","seeds_recorded","topology_controls_included"];
 document.getElementById("integrity").innerHTML=names.map(function(k){var v=checks[k];return "<div class=control><b>"+safe(k.replaceAll("_"," "))+"</b><br><span class="+(v===true?"pass":"")+">"+(v===true?"PASS":v===false?"FAIL":"NOT RECORDED")+"</span></div>"}).join("");
}
fetch("/api/results").then(function(r){return r.json()}).then(function(d){DATA=d;var s=document.getElementById("run");DATA.runs.forEach(function(r){var o=document.createElement("option");o.value=r.run_id;o.textContent=r.run_id;s.appendChild(o)});s.onchange=render;render()}).catch(function(){render()});
</script></body></html>"""


class Handler(BaseHTTPRequestHandler):
    def do_GET(self) -> None:
        path = urlparse(self.path).path
        if path == "/api/results":
            body = json.dumps(payload()).encode("utf-8")
            self.send_response(200)
            self.send_header("Content-Type", "application/json; charset=utf-8")
            self.send_header("Cache-Control", "no-store")
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()
            self.wfile.write(body)
            return
        if path in {"/", "/index.html"}:
            body = HTML.encode("utf-8")
            self.send_response(200)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()
            self.wfile.write(body)
            return
        self.send_error(404)

    def log_message(self, fmt: str, *args: object) -> None:
        return


def main() -> None:
    RUNS_DIR.mkdir(parents=True, exist_ok=True)
    server = ThreadingHTTPServer((HOST, PORT), Handler)
    print(f"Neuro-Risk Engine dashboard: http://{HOST}:{PORT}")
    print(f"Reading experiment results from: {RUNS_DIR}")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.server_close()


if __name__ == "__main__":
    main()
