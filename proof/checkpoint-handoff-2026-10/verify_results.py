"""Recompute input/result hashes and rerun both candidates with the frozen validator."""
import json
import pathlib
import subprocess
import sys
import tempfile
from run import digest

root=pathlib.Path(__file__).resolve().parent
receipt=json.loads((root/'paired-result.json').read_text())
manifest=json.loads((root/'manifest.json').read_text())
assert receipt['pairs']==1 and receipt['input_manifest']==manifest
assert all(digest(root/'fixture'/name)==value for name,value in manifest.items())
for arm,result in receipt['results'].items():
    source=root/'solutions'/(arm+'.py')
    assert digest(source)==result['source_sha256']
    with tempfile.TemporaryDirectory() as directory:
        workspace=pathlib.Path(directory)
        (workspace/'slug.py').write_bytes(source.read_bytes())
        actual=json.loads(subprocess.check_output([sys.executable,str(root/'validator.py'),str(workspace),'full'],text=True))
    assert actual==result['acceptance']=={'accepted':True,'stage':'full','cases':21}
    assert result['protected_files_unchanged'] and result['source_unchanged_during_validation']
    assert result['billing_usd'] is None and result['completed_tasks_redone'] is None
assert receipt['results']['snipara']['resume']['completed_tasks']==2
assert receipt['results']['snipara']['resume']['restored_phase']=='unicode'
print(json.dumps({'verified':True,'pairs':1,'independent_cases_per_arm':21,
    'scope':'Recomputed frozen inputs, reported hashes and candidate correctness; durations/tokens are operator-reported observations, not replayable assertions.'}))
