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
:root{--bg:#f3f6fb;--panel:#ffffff;--panel-soft:#f8fafc;--line:#dbe3ee;--line-dark:#aebbd0;--text:#162033;--muted:#64748b;--navy:#18243d;--blue:#356ae6;--blue-soft:#eaf0ff;--cyan:#13a8a8;--green:#23936f;--green-soft:#e8f7f1;--purple:#7658d8;--purple-soft:#f0ecff;--amber:#c98520;--amber-soft:#fff5e5;--shadow:0 8px 24px rgba(32,55,92,.07)}
*{box-sizing:border-box}html{background:var(--bg)}body{margin:0;background:var(--bg);color:var(--text);font-family:Inter,ui-sans-serif,system-ui,-apple-system,"Segoe UI",sans-serif;font-size:14px;line-height:1.5}
main{max-width:1500px;margin:auto;padding:30px 34px 55px}.header{display:flex;justify-content:space-between;align-items:flex-start;gap:25px;margin-bottom:20px;padding-bottom:22px;border-bottom:1px solid var(--line-dark)}
h1{font-family:Georgia,"Times New Roman",serif;font-weight:500;letter-spacing:-.02em;font-size:30px;margin:3px 0 5px}h2{font-family:Georgia,"Times New Roman",serif;font-weight:500;font-size:18px;margin:0}.muted{color:var(--muted);font-size:12px}
.header>div:first-child:before{content:"NEURO-RISK ENGINE  /  EXPERIMENTAL COMPUTING LABORATORY";display:block;color:var(--accent);font-size:10px;letter-spacing:.14em;font-weight:800;margin-bottom:5px}.header>div:first-child:after{content:"Connectome-inspired architectures for synthetic financial risk research";display:block;color:var(--muted);font-size:12px;margin-top:3px}
.badge{border:1px solid var(--line-dark);border-radius:4px;padding:8px 11px;color:var(--accent);background:var(--panel);font-size:10px;letter-spacing:.1em;font-weight:800;white-space:nowrap}
.grid{display:grid;grid-template-columns:repeat(4,1fr);gap:12px}.panel{background:var(--panel);border:1px solid var(--line);border-radius:2px;padding:18px;margin-bottom:16px;box-shadow:var(--shadow)}
.value{font-family:Georgia,"Times New Roman",serif;font-size:23px;font-weight:500}.label{font-size:10px;color:var(--muted);text-transform:uppercase;letter-spacing:.11em;font-weight:800}
.toolbar{display:flex;justify-content:space-between;align-items:center;gap:10px;flex-wrap:wrap}select,button{background:var(--panel);color:var(--text);border:1px solid var(--line-dark);border-radius:3px;padding:8px 10px}button:hover{background:#f0f3f0}
.table{overflow:auto}table{width:100%;border-collapse:collapse;font-size:12px}th,td{padding:10px 9px;border-bottom:1px solid var(--line);text-align:right;white-space:nowrap;font-variant-numeric:tabular-nums}th:first-child,td:first-child{text-align:left}th{color:var(--muted);font-size:10px;text-transform:uppercase;letter-spacing:.07em;font-weight:800;background:#fafbfa}
canvas{width:100%;height:270px}.controls{display:grid;grid-template-columns:repeat(3,1fr);gap:9px}.control{border:1px solid var(--line);border-radius:2px;padding:12px;background:#fbfcfb}.pass{color:var(--accent)}
.panel h2{border-bottom:1px solid var(--line);padding-bottom:10px;margin-bottom:15px}.grid .panel{min-height:104px}.panel:nth-of-type(4){border-left:3px solid var(--accent)}.panel:nth-of-type(4):before{content:"PRE-REGISTERED RESEARCH QUESTION";display:block;color:var(--accent);font-size:10px;letter-spacing:.12em;font-weight:800;margin-bottom:7px}
@media(max-width:900px){.grid{grid-template-columns:repeat(2,1fr)}.controls{grid-template-columns:1fr 1fr}}@media(max-width:600px){main{padding:18px 13px}.grid{grid-template-columns:1fr}.header{display:block}.badge{display:inline-block;margin-top:12px}}@media(prefers-reduced-motion:reduce){*{scroll-behavior:auto!important;transition:none!important}}
.app{display:grid;grid-template-columns:176px minmax(0,1fr);min-height:100vh}.rail{background:#fff;color:#19345f;padding:30px 14px 22px;display:flex;flex-direction:column;min-height:100vh;border-right:1px solid #e1e7f0}.rail-title{font:800 15px/1.15 Inter,ui-sans-serif,system-ui,sans-serif;letter-spacing:-.02em;color:#18386d;padding:0 10px}.rail-title:before{content:"NR";display:inline-grid;place-items:center;width:28px;height:28px;border-radius:8px;background:#e9f1ff;color:#2f6fed;font-size:11px;margin-right:8px;vertical-align:middle}.rail-rule{height:1px;background:#e7ebf2;margin:28px 10px 22px}.nav-label{font:700 9px/1.2 Inter,ui-sans-serif,system-ui,sans-serif;letter-spacing:.1em;color:#9aa8bd;margin:0 10px 8px;text-transform:uppercase}.rail nav{display:flex;flex-direction:column;gap:3px}.rail nav a{color:#8290a7;text-decoration:none;padding:10px 12px 10px 14px;font-size:12px;border-radius:5px;position:relative}.rail nav a:hover{background:#f5f8fc;color:#31578f}.rail nav a.active{background:#f0f5ff;color:#1f55b5;font-weight:700}.rail nav a.active:before{content:"";position:absolute;left:0;top:8px;bottom:8px;width:3px;border-radius:3px;background:#3678f6}.rail-bottom{margin-top:auto;padding:0 10px}.env{font:600 9px Inter,ui-sans-serif,system-ui,sans-serif;color:#8997aa;margin:8px 0}.version{font:9px ui-monospace,SFMono-Regular,Menlo,monospace;color:#a4afbe;margin-top:18px}.workspace{min-width:0;background:#f4f6fa;padding:30px 34px 50px}.masthead{display:flex;justify-content:space-between;gap:28px;align-items:flex-start;padding:0 0 18px;border-bottom:1px solid #dce3ed}.eyebrow{font:700 10px Inter,ui-sans-serif,system-ui,sans-serif;letter-spacing:.02em;color:#6f7f97;text-transform:none}.masthead h1{font:700 31px Inter,ui-sans-serif,system-ui,sans-serif;letter-spacing:-.035em;margin:4px 0 5px;color:#183d72}.masthead p{margin:0;color:#74839a;font-size:12px}.runbox{display:flex;align-items:center;gap:8px;height:max-content}.runbox label{font:700 9px Inter,ui-sans-serif,system-ui,sans-serif;color:#8290a6}.runbox select,.runbox button{font:600 11px Inter,ui-sans-serif,system-ui,sans-serif;border:1px solid #dce3ed;border-radius:7px;background:#fff;padding:9px 11px;color:#24436e}.runbox button{background:#3275ed;color:#fff;border-color:#3275ed;cursor:pointer}.runbox button:hover{background:#2866d5}.provenance{display:grid;grid-template-columns:repeat(6,1fr);background:#fff;border:1px solid #e2e7ef;border-radius:12px;box-shadow:0 2px 10px rgba(40,66,104,.035);margin:20px 0}.provenance div{padding:12px 13px;border-right:1px solid #edf0f5}.provenance div:last-child{border-right:0}.provenance span{display:block;font:700 8px Inter,ui-sans-serif,system-ui,sans-serif;color:#9aa7ba;letter-spacing:.04em}.provenance b{display:block;font:600 11px Inter,ui-sans-serif,system-ui,sans-serif;margin-top:5px;overflow:hidden;text-overflow:ellipsis;white-space:nowrap;color:#203f6d}.question{border:1px solid #d8e5ff;border-radius:10px;padding:13px 17px;margin-bottom:18px;background:#f7faff}.section-label{font:700 9px Inter,ui-sans-serif,system-ui,sans-serif;letter-spacing:.06em;color:#3275ed;text-transform:uppercase}.question p{font:600 14px/1.5 Inter,ui-sans-serif,system-ui,sans-serif;margin:5px 0 2px;color:#24436e}.section{background:#fff;border:1px solid #e1e7ef;border-radius:12px;margin-bottom:18px;box-shadow:0 3px 14px rgba(40,66,104,.035);overflow:hidden}.section-head{display:flex;justify-content:space-between;align-items:baseline;padding:16px 22px;border-bottom:1px solid #edf0f5;background:#fff}.section-head h2{font:700 17px Inter,ui-sans-serif,system-ui,sans-serif;color:#173a6d}.section-head span{font:10px Inter,ui-sans-serif,system-ui,sans-serif;color:#8a98ab}.section .table{padding:0 18px 8px}.table table tbody tr:hover{background:#f8fbff}.table td:first-child b{color:#254b7d}.table th{background:#f7f9fc;color:#8a98ad;font-size:10px;padding-top:11px;padding-bottom:11px}.table td{border-bottom:1px solid #edf0f5}.figures{display:grid;grid-template-columns:1fr 1fr;gap:0;padding:2px 8px 8px}.figures figure{margin:0;padding:17px 16px;border-right:1px solid #edf0f5}.figures figure:last-child{border-right:0}.figures figcaption{font:600 12px Inter,ui-sans-serif,system-ui,sans-serif;margin-bottom:8px;color:#294a76}.figures figcaption b{color:#3275ed;margin-right:7px}.figures canvas{height:245px}.caption{font-size:10px;color:#8a98ab;line-height:1.45;margin:5px 0 0}.integrity{display:grid;grid-template-columns:repeat(3,1fr);gap:0}.integrity .control{border:0;border-right:1px solid #edf0f5;border-bottom:1px solid #edf0f5;background:#fff;padding:14px 17px}.integrity .control b{font:600 10px Inter,ui-sans-serif,system-ui,sans-serif;text-transform:none;color:#486284}.integrity .control span{font:700 9px Inter,ui-sans-serif,system-ui,sans-serif;display:block;margin-top:5px}.integrity .pass{color:#22a06b}.methods .notes{display:grid;grid-template-columns:repeat(3,1fr)}.notes>div{display:grid;grid-template-columns:28px 1fr;gap:8px;padding:15px 18px;border-right:1px solid #edf0f5}.notes>div:last-child{border-right:0}.notes b{font:700 10px Inter,ui-sans-serif,system-ui,sans-serif;color:#3275ed}.notes p{margin:0;font-size:11px;color:#75849a}.research-grid{display:grid;grid-template-columns:repeat(2,1fr);gap:0;background:#fff}.research-item{display:grid;grid-template-columns:36px 1fr;gap:12px;padding:18px 20px;background:#fff;border-right:1px solid #edf0f5;border-bottom:1px solid #edf0f5}.research-item.blue{border-top:3px solid #3a7af2}.research-item.purple{border-top:3px solid #7958d8}.research-item.cyan{border-top:3px solid #18a6a6}.research-item.amber{border-top:3px solid #d28a24}.research-index{width:28px;height:28px;border-radius:8px;display:grid;place-items:center;background:#edf4ff;color:#3275ed;font:700 9px Inter,ui-sans-serif,system-ui,sans-serif}.purple .research-index{background:#f1edff;color:#7958d8}.cyan .research-index{background:#e9f8f8;color:#18a6a6}.amber .research-index{background:#fff5e7;color:#c78320}.research-item b{font-size:12px;color:#274a77}.research-item p{font-size:11px;color:#7a899e;margin:4px 0 0;line-height:1.5}.research-item a{display:inline-block;margin-top:9px;font-size:10px;color:#3275ed;text-decoration:none;font-weight:700}.research-item a:hover{text-decoration:underline}.research-footer{display:flex;gap:10px;padding:14px 20px;background:#f8fafc;border-top:1px solid #edf0f5;font-size:10px;color:#7a899e}.research-footer b{color:#355579;white-space:nowrap}.tabs{display:flex;gap:26px;border-bottom:1px solid #dce3ed;margin-bottom:18px;padding-top:4px}.tabs a{font-size:12px;color:#7d8ca2;padding:11px 0 10px;position:relative}.tabs a.selected{color:#2457a5;font-weight:700}.tabs a.selected:after{content:"";position:absolute;left:0;right:0;bottom:-1px;height:2px;background:#3275ed;border-radius:2px}.hero-study{display:flex;justify-content:space-between;align-items:center;gap:20px;background:#fff;border:1px solid #e1e7ef;border-radius:12px;padding:18px 22px;margin-bottom:18px;box-shadow:0 3px 14px rgba(40,66,104,.035)}.hero-study h2{font:600 16px/1.45 Inter,ui-sans-serif,system-ui,sans-serif;color:#1d416f;margin:5px 0 0;max-width:850px}.study-state{font:600 10px Inter,ui-sans-serif,system-ui,sans-serif;color:#2a8b69;background:#ecf8f3;border:1px solid #ccecdf;border-radius:20px;padding:7px 10px;white-space:nowrap}.dot{display:inline-block;width:6px;height:6px;background:#27aa73;border-radius:50%;margin-right:6px}.section-head p{margin:3px 0 0;font-size:10px;color:#93a0b2}.legend{display:flex;justify-content:space-between;gap:10px;font-size:9px;color:#8b98aa;padding:4px 4px 0}.legend i{display:inline-block;width:7px;height:7px;border-radius:50%;margin-right:5px}.blue-dot{background:#3275ed}.green-dot{background:#25a873}.workspace footer{font:9px Inter,ui-sans-serif,system-ui,sans-serif;color:#9aa7b9;padding-top:12px}@media(max-width:1050px){.provenance{grid-template-columns:repeat(3,1fr)}.figures,.methods .notes,.research-grid{grid-template-columns:1fr}.figures figure{border-right:0;border-bottom:1px solid #edf0f5}.notes>div{border-right:0;border-bottom:1px solid #edf0f5}}@media(max-width:760px){.app{grid-template-columns:1fr}.rail{min-height:auto;padding:15px 18px}.rail nav,.rail-bottom{display:none}.rail-rule{margin:10px 0}.workspace{padding:20px 14px}.masthead{display:block}.runbox{margin-top:15px}.provenance{grid-template-columns:repeat(2,1fr)}.integrity{grid-template-columns:1fr}}
</style></head><body>
<div class="app">
<aside class="rail">
  <div class="rail-title">NEURO-RISK<br>ENGINE</div>
  <div class="rail-rule"></div>
  <div class="nav-label">Workspace</div>
  <nav>
    <a class="active">Overview</a><a>Experiments</a><a>Model Benchmark</a><a>Topology</a><a>Controls</a><a>Deep Research</a>
  </nav>
  <div class="rail-bottom">
    <div class="nav-label">ENVIRONMENT</div>
    <div class="env">Synthetic data</div>
    <div class="env">Research only</div>
    <div class="version">NRX dashboard 0.3</div>
  </div>
</aside>

<main class="workspace">
<header class="masthead">
  <div>
    <div class="eyebrow">Research workspace  /  Comparative evaluation</div>
    <h1>Neuro-Risk Engine</h1>
    <p>Connectome-inspired architectures for synthetic financial risk research</p>
  </div>
  <div class="runbox">
    <label for="run">Experiment</label>
    <select id="run"><option value="all">All recorded runs</option></select>
    <button onclick="location.reload()">Refresh</button>
  </div>
</header>

<div class="tabs"><a class="selected">Overview</a><a>Model benchmark</a><a>Topology</a><a>Deep Research</a></div>

<section class="hero-study"><div><div class="section-label">Research question</div><h2>Can biological neural connectivity provide useful computational properties for real-time financial risk decision-making?</h2></div><div class="study-state"><span class="dot"></span> Experimental study</div></section>

<section class="provenance">
  <div><span>DATASET</span><b id="metaDataset"></b></div>
  <div><span>TOPOLOGY</span><b id="metaTopology"></b></div>
  <div><span>SEED</span><b id="metaSeed"></b></div>
  <div><span>SPLIT</span><b id="metaSplit"></b></div>
  <div><span>INPUT</span><b id="metaInput"></b></div>
  <div><span>RUN STATUS</span><b id="runStatus">PRE-BENCHMARK</b></div>
</section>

<section class="section">
  <div class="section-head"><div><h2>Model benchmark</h2><p>Predictive performance and inference cost</p></div><span>Primary comparison</span></div>
  <div class="table"><table><thead><tr>
  <th>Architecture</th><th>F1</th><th>ROC-AUC</th><th>PR-AUC</th><th>Precision</th><th>Recall</th><th>P95 latency (ms)</th><th>Parameters</th><th>Memory (MB)</th><th>Synaptic ops</th>
  </tr></thead><tbody id="rows"></tbody></table></div>
</section>

<section class="section">
  <div class="section-head"><div><h2>Performance analysis</h2><p>Recorded model behavior across efficiency dimensions</p></div><span>Figures 01 to 02</span></div>
  <div class="figures">
    <figure><figcaption><b>01</b> F1 score vs computational cost</figcaption><canvas id="costChart"></canvas><p class="caption">F1 score against recorded synaptic/event operations. Lower cost is preferable at comparable predictive performance.</p></figure>
    <figure><figcaption><b>02</b> F1 score vs P95 latency</figcaption><canvas id="latChart"></canvas><p class="caption">F1 score against P95 inference latency. Values are reported per recorded run.</p></figure>
  </div>
</section>

<section class="section">
  <div class="section-head"><div><h2>Experimental integrity</h2><p>Conditions required for a valid model comparison</p></div><span>Study controls</span></div>
  <div class="integrity" id="integrity"></div>
</section>

<section class="section deep-research">
  <div class="section-head"><div><h2>Deep Research</h2><p>Scientific interpretation and experiment design</p></div><span>Research workspace</span></div>
  <div class="research-grid">
    <div class="research-item blue"><span class="research-index">01</span><div><b>Biological topology</b><p>Connectome structure, neuron populations, synaptic threshold, and circuit provenance.</p></div></div>
    <div class="research-item purple"><span class="research-index">02</span><div><b>Computational mechanism</b><p>Spiking dynamics, event representation, latency, computational cost, and parameter budget.</p></div></div>
    <div class="research-item cyan"><span class="research-index">03</span><div><b>Financial experiment</b><p>Predictive performance on synthetic transaction risk data using a frozen experimental protocol.</p></div></div>
    <div class="research-item amber"><span class="research-index">04</span><div><b>Control analysis</b><p>Randomized topology, degree-preserving topology, matched sparsity, and threshold sensitivity.</p></div></div>
  </div>
  <div class="research-footer"><b>Interpretation rule</b><span>Only attribute an advantage to connectome topology after the control experiments isolate topology from sparsity, dynamics, and model capacity.</span></div>
</section>

<section class="section methods">
  <div class="section-head"><div><h2>Interpretation notes</h2><p>Study constraints and reporting boundaries</p></div><span>Methods</span></div>
  <div class="notes">
    <div><b>01</b><p>A performance advantage for an SNN does not establish a biological-topology advantage. Sparsity, dynamics, parameter budget, and topology must be separated experimentally.</p></div>
    <div><b>02</b><p>The connectome topology is frozen before financial benchmarking. Threshold sensitivity and randomized topology controls are required for causal interpretation.</p></div>
    <div><b>03</b><p>This reporting layer reads experiment artifacts only. It does not execute models or make production payment, fraud, or account decisions.</p></div>
  </div>
</section>

<footer>NEURO-RISK ENGINE / RESEARCH REPORTING LAYER / SYNTHETIC / NON-PRODUCTION</footer>
</main>
<script>
var DATA={runs:[],rows:[]};
function fmt(v,d){return v===null||v===undefined||isNaN(Number(v))?"":Number(v).toFixed(d===undefined?3:d)}
function safe(s){return String(s==null?"":s).replace(/[&<>"']/g,function(c){return {"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;","'":"&#39;"}[c]})}
function selected(){var r=document.getElementById("run").value;return DATA.rows.filter(function(x){return r==="all"||x.run_id===r})}
function best(rows,key,asc){var a=rows.filter(function(x){return x[key]!=null}).slice().sort(function(x,y){return (asc?1:-1)*(Number(x[key])-Number(y[key]))});return a[0]}
function render(){
 var rows=selected(),body=document.getElementById("rows"),run=DATA.runs.find(function(x){return x.run_id===document.getElementById("run").value})||DATA.runs[0]||null,c=run?run.config||{}:{};
 body.innerHTML=rows.length?rows.map(function(r){return "<tr><td><b>"+safe(r.model)+"</b></td><td>"+fmt(r.f1)+"</td><td>"+fmt(r.roc_auc)+"</td><td>"+fmt(r.pr_auc)+"</td><td>"+fmt(r.precision)+"</td><td>"+fmt(r.recall)+"</td><td>"+fmt(r.p95_latency_ms,2)+"</td><td>"+fmt(r.parameters,0)+"</td><td>"+fmt(r.memory_mb,1)+"</td><td>"+fmt(r.synaptic_operations,0)+"</td></tr>"}).join(""):"<tr><td colspan=10 class=muted>No experiment results recorded. The reporting layer is ready for experiments/runs/&lt;run_id&gt;.</td></tr>";
 function set(id,v){document.getElementById(id).textContent=v==null||v===""?"":typeof v==="object"?JSON.stringify(v):v}
 set("metaDataset",c.dataset||c.data_source);set("metaTopology",c.topology_version||c.topology);set("metaSeed",c.seed);set("metaSplit",c.split);set("metaInput",c.input_representation||c.features);set("runStatus",rows.length?"RESULTS RECORDED":"PRE-BENCHMARK");
 chart(document.getElementById("costChart"),rows,"synaptic_operations","f1");chart(document.getElementById("latChart"),rows,"p95_latency_ms","f1");integrity();
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

