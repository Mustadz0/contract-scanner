#!/usr/bin/env python3
"""
Contract Clause Scanner — Web UI
Run: python web.py
"""

import json
import os
import tempfile
from pathlib import Path

from fastapi import FastAPI, UploadFile, File, Form, Request
from fastapi.responses import HTMLResponse, Response
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

from core.parser import extract_text
from core.analyzer import ContractAnalyzer

app = FastAPI(title="Contract Clause Scanner")
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])

INDEX_HTML = """<!DOCTYPE html>
<html lang="en" data-theme="dark">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Contract Scanner — AI Clause Analyzer</title>
<style>
*{margin:0;padding:0;box-sizing:border-box}
body{font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,sans-serif;background:#0a0a0f;color:#e2e8f0;min-height:100vh}
.nav{padding:16px 24px;border-bottom:1px solid #1e1e2e;display:flex;align-items:center;justify-content:space-between}
.nav h1{font-size:18px;font-weight:700}
.nav span{color:#64748b;font-size:13px}
.container{max-width:840px;margin:0 auto;padding:32px 20px}
.upload-box{border:2px dashed #2a2a3e;border-radius:14px;padding:48px 20px;text-align:center;cursor:pointer;transition:all .25s;background:#0f0f1a}
.upload-box:hover,.upload-box.dragover{border-color:#3b82f6;background:#0f172a}
.upload-box.has-file{border-color:#22c55e;border-style:solid}
.upload-box svg{width:36px;height:36px;stroke:#64748b;margin-bottom:10px}
.upload-box p{color:#94a3b8;font-size:14px}
.file-name{color:#22c55e;font-size:13px;margin-top:6px;font-weight:600}
.options{display:flex;gap:12px;margin-top:16px;flex-wrap:wrap}
.options select,.options button{padding:10px 16px;border-radius:10px;font-size:14px;border:1px solid #2a2a3e;background:#0f0f1a;color:#e2e8f0;cursor:pointer;flex:1;min-width:120px;font-family:inherit}
.options button{background:#3b82f6;color:#fff;font-weight:600;border:none}
.options button:hover{background:#2563eb}
.options button:disabled{opacity:.5;cursor:not-allowed}
.error{color:#ef4444;font-size:13px;margin-top:10px;display:none}
.hidden{display:none}
#report{margin-top:24px}
.score-card{background:#0f172a;border-radius:12px;padding:20px;margin-bottom:16px;display:flex;align-items:center;gap:20px;flex-wrap:wrap}
.score-number{font-size:42px;font-weight:800}
.score-number.low{color:#22c55e}
.score-number.medium{color:#eab308}
.score-number.high{color:#ef4444}
.score-number.critical{color:#dc2626}
.score-label{font-size:13px;color:#64748b;text-transform:uppercase;letter-spacing:1px}
.flag-card{background:#0f172a;border-radius:12px;padding:16px 20px;margin-bottom:12px;border-left:4px solid}
.flag-card.critical,.flag-card.high{border-color:#ef4444}
.flag-card.medium{border-color:#eab308}
.flag-card.low{border-color:#22c55e}
.flag-severity{font-size:11px;font-weight:700;text-transform:uppercase;letter-spacing:1px;margin-bottom:4px}
.flag-severity.high,.flag-severity.critical{color:#ef4444}
.flag-severity.medium{color:#eab308}
.flag-severity.low{color:#22c55e}
.flag-clause{font-size:13px;color:#94a3b8;margin-bottom:4px;font-style:italic}
.flag-why{font-size:14px;margin-bottom:4px}
.flag-tip{font-size:13px;color:#3b82f6}
.section-title{font-size:16px;font-weight:700;margin:20px 0 12px}
.watch-list{background:#0f172a;border-radius:12px;padding:16px 20px}
.watch-list li{font-size:14px;margin:6px 0;color:#94a3b8}
.steps{display:flex;flex-wrap:wrap;gap:8px}
.steps .step{background:#1e293b;border-radius:20px;padding:8px 16px;font-size:13px;color:#e2e8f0}
.loading{text-align:center;padding:40px;display:none}
.spinner{width:32px;height:32px;border:3px solid #1e293b;border-top-color:#3b82f6;border-radius:50%;animation:spin .8s linear infinite;margin:0 auto 12px}
@keyframes spin{to{transform:rotate(360deg)}}
footer{text-align:center;padding:32px;color:#475569;font-size:13px}
footer a{color:#3b82f6;text-decoration:none}
</style>
</head>
<body>
<div class="nav"><h1>Contract Scanner</h1><span>AI-Powered Clause Analyzer</span></div>
<div class="container">
  <form id="uploadForm">
    <div class="upload-box" id="uploadBox">
      <svg fill="none" stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" viewBox="0 0 24 24"><path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/><polyline points="17 8 12 3 7 8"/><line x1="12" y1="3" x2="12" y2="15"/></svg>
      <p>Drop contract here (PDF, DOCX, TXT) or click to upload</p>
      <div class="file-name" id="fileName"></div>
    </div>
    <input type="file" id="fileInput" accept=".pdf,.docx,.doc,.txt" style="display:none">
    <div class="options">
      <select name="language" id="langSelect">
        <option value="en">English</option>
        <option value="ar">العربية</option>
        <option value="fr">Français</option>
        <option value="es">Español</option>
        <option value="de">Deutsch</option>
        <option value="tr">Türkçe</option>
      </select>
      <button type="submit" id="analyzeBtn">Analyze</button>
    </div>
    <div class="error" id="errorMsg"></div>
  </form>

  <div class="loading" id="loading"><div class="spinner"></div><p>Analyzing contract with AI...</p></div>

  <div id="report" class="hidden"></div>
</div>
<footer>Built by <a href="https://github.com/Mustadz0">Mustadz0</a> &middot; Powered by Gemini AI</footer>

<script>
const uploadBox=document.getElementById('uploadBox'),fileInput=document.getElementById('fileInput'),fileName=document.getElementById('fileName'),analyzeBtn=document.getElementById('analyzeBtn'),errorMsg=document.getElementById('errorMsg'),loading=document.getElementById('loading'),report=document.getElementById('report');
let selectedFile=null;
uploadBox.addEventListener('click',()=>fileInput.click());
uploadBox.addEventListener('dragover',e=>{e.preventDefault();uploadBox.classList.add('dragover')});
uploadBox.addEventListener('dragleave',()=>uploadBox.classList.remove('dragover'));
uploadBox.addEventListener('drop',e=>{e.preventDefault();uploadBox.classList.remove('dragover');handleFile(e.dataTransfer.files[0])});
fileInput.addEventListener('change',e=>handleFile(e.target.files[0]));
function handleFile(f){if(!f){error('Select a file');return}const ext=f.name.split('.').pop().toLowerCase();if(!['pdf','docx','doc','txt'].includes(ext)){error('Supported: PDF, DOCX, TXT');return}selectedFile=f;fileName.textContent='✓ '+f.name;uploadBox.classList.add('has-file');errorMsg.style.display='none'}
document.getElementById('uploadForm').addEventListener('submit',async e=>{e.preventDefault();if(!selectedFile){error('Select a file first');return}
analyzeBtn.disabled=true;loading.style.display='block';report.classList.add('hidden');errorMsg.style.display='none'
const fd=new FormData();fd.append('file',selectedFile);fd.append('language',document.getElementById('langSelect').value)
try{const r=await fetch('/analyze',{method:'POST',body:fd});if(!r.ok){const e=await r.json();throw new Error(e.detail||'Analysis failed')}
const data=await r.json();showReport(data)}catch(e){error(e.message)}finally{analyzeBtn.disabled=false;loading.style.display='none'}})
function showReport(d){report.classList.remove('hidden')
const l=d.risk_level.toLowerCase();
report.innerHTML=`
<div class="score-card"><div><div class="score-label">Risk Score</div><div class="score-number ${l}">${d.overall_risk_score}/100</div><div style="font-size:13px;color:#64748b">${d.risk_level}</div></div><div><div class="score-label">Summary</div><div style="font-size:14px;color:#94a3b8;max-width:500px">${d.summary||''}</div></div></div>
${(d.red_flags||[]).map(f=>`<div class="flag-card ${f.severity.toLowerCase()}"><div class="flag-severity ${f.severity.toLowerCase()}">${f.severity}</div><div class="flag-clause">${f.clause||''}</div><div class="flag-why">${f.why_risky||''}</div>${f.negotiation_tip?`<div class="flag-tip">${f.negotiation_tip}</div>`:''}</div>`).join('')}
${(d.key_watchpoints||[]).length?`<div class="section-title">Watch Out For</div><div class="watch-list"><ul>${d.key_watchpoints.map(w=>`<li>${w}</li>`).join('')}</ul></div>`:''}
${(d.next_steps||[]).length?`<div class="section-title">Next Steps</div><div class="steps">${d.next_steps.map(s=>`<span class="step">${s}</span>`).join('')}</div>`:''}
`}
function error(msg){errorMsg.textContent=msg;errorMsg.style.display='block'}
</script>
</body>
</html>"""


@app.get("/", response_class=HTMLResponse)
async def index():
    return INDEX_HTML


@app.post("/analyze")
async def analyze(file: UploadFile = File(...), language: str = Form("en")):
    from fastapi import HTTPException

    ext = file.filename.split(".")[-1].lower()
    if ext not in ("pdf", "docx", "doc", "txt"):
        raise HTTPException(400, "Supported formats: PDF, DOCX, TXT")

    content = await file.read()
    suffix = f".{ext}"

    with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
        tmp.write(content)
        tmp_path = tmp.name

    try:
        text = extract_text(Path(tmp_path))
        analyzer = ContractAnalyzer()
        result = analyzer.analyze(text, language=language)
    except Exception as e:
        raise HTTPException(500, str(e))
    finally:
        os.unlink(tmp_path)

    return result


if __name__ == "__main__":
    uvicorn.run("web:app", host="0.0.0.0", port=8000, reload=True)
