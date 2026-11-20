#!/usr/bin/env python3
"""Deploy the Foxy Green pitch: "/" serves the concept page, "/proposal" serves the proposal.
Same Worker, checks, and token handling as the sticky-mule-website skill's deploy_pitch.py,
extended with a second route. Usage: python3 scripts/deploy.py"""
import gzip, json, subprocess, sys, tempfile, importlib.util
from pathlib import Path
root = Path(__file__).resolve().parent.parent
SKILL = Path("/root/.claude/skills/synced/88260777-ad37-4998-a3f4-9af9e0223dc3_61237372-4da9-4979-a265-5686cc2fa274/sticky-mule-website/scripts/deploy_pitch.py")
spec = importlib.util.spec_from_file_location("deploy_pitch", SKILL); dp = importlib.util.module_from_spec(spec); spec.loader.exec_module(dp)
NAME = "foxygreen-concept"
page = (root / "dist/foxygreen-concept.html").read_text(encoding="utf-8")
proposal = (root / "proposal/proposal.html").read_text(encoding="utf-8")
dp.check_page(page, False)
if 'content="noindex' not in proposal: dp.fail("proposal is missing noindex")
worker = dp.WORKER_TEMPLATE.replace("__HTML__", json.dumps(page))
worker = worker.replace('const ROBOTS', 'const PROPOSAL = ' + json.dumps(proposal) + ';\nconst ROBOTS', 1)
worker = worker.replace('    if (url.pathname !== "/") {',
    '    if (url.pathname === "/proposal" || url.pathname === "/proposal/") {\n'
    '      return new Response(request.method === "HEAD" ? null : PROPOSAL, { headers: HEADERS });\n    }\n'
    '    if (url.pathname !== "/") {', 1)
assert "PROPOSAL, { headers" in worker
size = len(gzip.compress(worker.encode()))
print(f"worker {size // 1024} KB gzipped")
if size > dp.MAX_GZIP_BYTES: dp.fail("worker too large")
with tempfile.TemporaryDirectory() as tmp:
    tmp = Path(tmp)
    (tmp / "worker.js").write_text(worker, encoding="utf-8")
    (tmp / "meta.json").write_text(json.dumps({"main_module": "worker.js", "compatibility_date": "2025-09-01"}))
    r = dp.curl_json(["-X", "PUT", f"{dp.API}/accounts/{dp.DEFAULT_ACCOUNT}/workers/scripts/{NAME}",
                      "-F", f"metadata=@{tmp / 'meta.json'};type=application/json",
                      "-F", f"worker.js=@{tmp / 'worker.js'};type=application/javascript+module"])
if not r.get("success"): dp.fail(f"upload failed: {r.get('errors')}")
print(f"uploaded Worker '{NAME}' with / and /proposal")
