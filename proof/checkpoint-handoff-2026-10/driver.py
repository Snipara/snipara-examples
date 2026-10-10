"""Operator-owned resume adapter. Never edit this file from a producing agent."""
import json
import os
import pathlib
import subprocess
import sys
import time
import urllib.request

workspace = pathlib.Path.cwd()
control = workspace.parent / 'control' / workspace.name
control.mkdir(parents=True, exist_ok=True)
start = time.monotonic()
arm = workspace.name
assert arm in {'baseline', 'snipara'}
assert sys.argv[1:] == ['resume']
if arm == 'snipara':
    key = os.environ.get('SNIPARA_API_KEY') or os.environ.get('RLM_API_KEY')
    assert key, 'Set an environment-backed project API key'
    slug = os.environ['SNIPARA_PROJECT_ID']
    request = urllib.request.Request(
        f'https://api.snipara.com/mcp/{slug}',
        data=json.dumps({'jsonrpc':'2.0','id':1,'method':'tools/list'}).encode(),
        headers={'X-API-Key':key,'Content-Type':'application/json',
                 'Accept':'application/json, text/event-stream'})
    with urllib.request.urlopen(request, timeout=30) as response:
        payload = response.read().decode()
    result = json.loads(payload) if payload.startswith('{') else json.loads(
        next(line[6:] for line in payload.splitlines() if line.startswith('data: ')))
    assert len(result.get('result', {}).get('tools', [])) > 0
    probe_seconds = time.monotonic() - start
    command_start = time.monotonic()
    process = subprocess.run([os.environ.get('COMPANION_BIN','snipara-companion'),
        'workflow','resume','--include-session-context','--json'],
        capture_output=True, text=True, timeout=90)
    (control/'resume-private.json').write_text(process.stdout)
    if process.returncode:
        raise RuntimeError('Companion resume failed; inspect private local receipt')
    data = json.loads(process.stdout)
    state = data['workflow']
    assert state['currentPhaseId'] == 'unicode'
    print(process.stdout)
    metrics = {'hosted_probe_seconds':round(probe_seconds,3),
               'resume_command_seconds':round(time.monotonic()-command_start,3),
               'restored_phase':state['currentPhaseId'],
               'completed_tasks':sum(t['status']=='completed' for p in state['phases'] for t in p['tasks'])}
else:
    print(json.dumps({'ordinary_project_files': ['SPEC.md','PLAN.json','DECISIONS.md','slug.py','artifacts/ascii-evidence.json'],
                     'instructions':'Read the ordinary project files to determine remaining work.'}))
    metrics = {'hosted_probe_seconds':None,'resume_command_seconds':None,
               'restored_phase':None,'completed_tasks':None}
metrics['adapter_seconds'] = round(time.monotonic()-start,3)
(control/'resume-metrics.json').write_text(json.dumps(metrics,indent=2)+'\n')
