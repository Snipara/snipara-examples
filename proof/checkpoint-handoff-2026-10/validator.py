import importlib.util, json, pathlib, sys
workspace = pathlib.Path(sys.argv[1]); stage = sys.argv[2]
spec = importlib.util.spec_from_file_location('candidate_slug', workspace/'slug.py')
module = importlib.util.module_from_spec(spec); spec.loader.exec_module(module)
cases = [(' Hello World ', 'hello-world'), ('A___B', 'a-b'), ('API.v2!', 'api-v2'),
         ('foo---bar','foo-bar'), ('abc123', 'abc123'), ('-- A B --','a-b')]
if stage == 'full':
    cases += [('Crème brûlée', 'creme-brulee'), ('Café déjà vu','cafe-deja-vu'),
              ('MÜNCHEN_2026', 'munchen-2026'), ('e\u0301cole','ecole'),
              ('Straße', 'stra-e'), ('À + Ö','a-o')]
for value, expected in cases:
    actual = module.slugify(value)
    assert actual == expected, (value, actual, expected)
errors = 0
if stage == 'full':
    for value in [None, 12, [], {}, b'abc']:
        try: module.slugify(value)
        except TypeError: errors += 1
        else: raise AssertionError(('expected TypeError',repr(value)))
    for value in ['', '   ', '___---!!!', '😀']:
        try: module.slugify(value)
        except ValueError: errors += 1
        else: raise AssertionError(('expected ValueError',repr(value)))
print(json.dumps({'accepted': True, 'stage': stage, 'cases': len(cases)+errors}))
