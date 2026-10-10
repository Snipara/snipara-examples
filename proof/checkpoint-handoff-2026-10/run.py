"""One paired continuation of frozen native Claude input; not a reliability study."""
import argparse
import hashlib
import json
import os
import pathlib
import shutil
import signal
import subprocess
import sys
import time

ROOT = pathlib.Path(__file__).resolve().parent
PROMPT = '''Continue this isolated project after an earlier Claude Code session completed the plan and ASCII phase and exited. You have no earlier conversation.
First run python3 {driver} resume. Read SPEC.md, PLAN.json, DECISIONS.md, slug.py and artifacts/ascii-evidence.json. Use the available ordinary files and, when present, the saved workflow to identify completed and remaining work.
Implement ONLY the Unicode/invalid-input requirements in slug.py. Write artifacts/HANDOFF.json with restored or inferred phase, completed tasks, next verification step and constraints. Do not redo completed planning or ASCII work.
Write only slug.py and artifacts/HANDOFF.json. Do not edit source contracts, prior evidence, .snipara, the driver or validator. Do not read credentials, previous conversations, controller receipts, other projects or network except the supplied resume adapter. No new agents, installs or extra features. The external operator validates and closes the remaining workflow. Use at most eight tool calls. Keep the final answer concise.
'''


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=pathlib.Path, required=True)
    parser.add_argument('--model', required=True, help='Same Codex model in both arms')
    parser.add_argument('--order', choices=['baseline-first','snipara-first'], default='baseline-first')
    args = parser.parse_args()
    output = args.output.resolve()
    if output.exists():
        raise SystemExit('Use a fresh output directory; historical runs are immutable')
    manifest = json.loads((ROOT/'manifest.json').read_text())
    assert all(digest(ROOT/'fixture'/name)==value for name,value in manifest.items())
    cli = os.environ.get('COMPANION_BIN','snipara-companion')
    codex_help = subprocess.check_output([os.environ.get('CODEX_BIN','codex'),'exec','--help'],text=True)
    if '--approve-for-me' not in codex_help:
        raise SystemExit('This frozen protocol requires the Codex distribution with --approve-for-me automatic approval review; do not bypass sandboxing')
    version = subprocess.check_output([cli,'--version'],text=True).strip()
    assert version.endswith('3.7.0'), f'Frozen protocol requires Companion 3.7.0, found {version}'
    assert os.environ.get('SNIPARA_PROJECT_ID'), 'Set your own Snipara project slug'
    assert os.environ.get('SNIPARA_API_KEY') or os.environ.get('RLM_API_KEY'), 'Missing API key'
    output.mkdir(parents=True)
    results = {}
    order = ['baseline','snipara'] if args.order=='baseline-first' else ['snipara','baseline']
    for arm in order:
        workspace = output/arm
        workspace.mkdir()
        (workspace/'artifacts').mkdir()
        for name in ['SPEC.md','PLAN.json','DECISIONS.md','slug.py']:
            shutil.copy2(ROOT/'fixture'/name,workspace/name)
        shutil.copy2(ROOT/'fixture'/'ascii-evidence.json',workspace/'artifacts/ascii-evidence.json')
        if arm=='snipara':
            (workspace/'.snipara/workflow').mkdir(parents=True)
            state=json.loads((ROOT/'fixture'/'checkpoint.json').read_text().replace('__WORKSPACE__',str(workspace)))
            (workspace/'.snipara/workflow/current.json').write_text(json.dumps(state,indent=2)+'\n')
            (workspace/'.snipara/project').write_text(os.environ['SNIPARA_PROJECT_ID']+'\n')
        protected = {str(p.relative_to(workspace)):digest(p) for p in workspace.rglob('*') if p.is_file() and p.name!='slug.py'}
        control = output/'control'/arm
        control.mkdir(parents=True)
        command = [os.environ.get('CODEX_BIN','codex'),'exec','--ignore-user-config',
            '--model',args.model,'-c','model_reasoning_effort="low"','--approve-for-me',
            '--skip-git-repo-check','--ephemeral','--json','-']
        prompt = PROMPT.format(driver=ROOT/'driver.py')
        (control/'prompt.txt').write_text(prompt)
        env=os.environ.copy()
        if arm=='baseline':
            for key in ['SNIPARA_API_KEY','RLM_API_KEY','SNIPARA_PROJECT_ID','SNIPARA_API_URL']:
                env.pop(key,None)
        start=time.monotonic()
        with (control/'events-private.jsonl').open('w') as out, (control/'stderr-private.txt').open('w') as err:
            process=subprocess.Popen(command,cwd=workspace,env=env,stdin=subprocess.PIPE,
                stdout=out,stderr=err,text=True,start_new_session=True)
            timed_out=False
            try:
                process.communicate(prompt,timeout=210)
            except subprocess.TimeoutExpired:
                timed_out=True
                os.killpg(process.pid,signal.SIGTERM)
                try:process.wait(timeout=5)
                except subprocess.TimeoutExpired:
                    os.killpg(process.pid,signal.SIGKILL);process.wait()
        seconds=round(time.monotonic()-start,3)
        events=[]
        for line in (control/'events-private.jsonl').read_text().splitlines():
            try:events.append(json.loads(line))
            except json.JSONDecodeError:pass
        usage=next((e.get('usage') for e in reversed(events) if e.get('type')=='turn.completed'),None)
        before=digest(workspace/'slug.py')
        validation=subprocess.run([sys.executable,str(ROOT/'validator.py'),str(workspace),'full'],capture_output=True,text=True)
        source_unchanged=digest(workspace/'slug.py')==before
        preserved=all((workspace/name).exists() and digest(workspace/name)==value for name,value in protected.items())
        metric_path=control/'resume-metrics.json'
        metrics=json.loads(metric_path.read_text()) if metric_path.exists() else None
        commands=[e['item']['command'] for e in events if e.get('type')=='item.completed' and e.get('item',{}).get('type')=='command_execution']
        # No invented time-to-first-progress or avoided-task metric: snapshots cannot prove those.
        result={'agent_exit_code':process.returncode,'timed_out':timed_out,'agent_session_seconds':seconds,
            'usage':usage,'billing_usd':None,'resume':metrics,'acceptance':json.loads(validation.stdout) if validation.returncode==0 else {'accepted':False},
            'protected_files_unchanged':preserved,'source_unchanged_during_validation':source_unchanged,
            'source_sha256':before,'command_execution_count':len(commands),
            'resume_attempts':sum('driver.py' in c and 'resume' in c for c in commands),
            'failed_resume_attempts':sum(e.get('item',{}).get('exit_code',0)!=0 for e in events if e.get('type')=='item.completed' and 'driver.py' in e.get('item',{}).get('command','')),
            'completed_tasks_redone':None,'time_to_first_useful_progress_seconds':None,
            'total_harness_overhead_seconds':None}
        results[arm]=result
        print(json.dumps({'arm':arm,**result}),flush=True)
    receipt={'protocol':'checkpoint-paired-continuation-v1','date_utc':time.strftime('%Y-%m-%d',time.gmtime()),
        'pairs':1,'model':args.model,'reasoning_effort':'low','order':order,'companion_version':'3.7.0',
        'input_manifest':manifest,'results':results,
        'limits':['One small local fixture and one paired continuation; no statistical reliability claim.',
        'Frozen input was produced by native Claude Code in the earlier October 10 demonstration; Claude was not rerun for this pair.',
        'Both arms receive the identical source, plan, decisions and original ASCII evidence. Snipara additionally has portable checkpoint state and Hosted MCP access.',
        'Checkpoint paths are rebased and private telemetry/memory identifiers redacted. Completed phases and attempt counters are preserved.',
        'Same model/settings/prompts and 210-second budget; sequential runs may differ due to caching and provider conditions.',
        'Resume command time includes hosted context retrieval, excluding a separately measured MCP probe. Session time includes implementation.',
        'Tokens are client-reported. Billing, avoided redo work, first useful progress and total harness overhead are not measured.',
        'No live process migration, MCP-only restoration, Orchestrator controller handoff or authenticated human acceptance.']}
    (output/'result.json').write_text(json.dumps(receipt,indent=2)+'\n')
    if not all(x['acceptance']['accepted'] and x['protected_files_unchanged'] and x['source_unchanged_during_validation'] and x['agent_exit_code']==0 for x in results.values()):
        raise SystemExit('Pair not fully accepted; failed outcomes were retained')

if __name__=='__main__':main()
