import sys, re, glob
# glmergejj.py: gn_JJ_*.txt -> globals_JOJOBA.txt; checks addrs vs gl_JJ_ram.txt, unique vs other globals and function names
want = [l.split()[0] for l in open('gl_JJ_ram.txt')]
fn = set()
for l in open('funcinfo_JOJOBA.tsv', encoding='utf-8', errors='replace'):
    p = l.rstrip('\n').split('\t')
    if p[0] == 'F' and len(p) > 2: fn.add(p[2])
got = {}; bad = 0
for f in sorted(glob.glob('gn_JJ_*.txt')):
    for l in open(f):
        p = l.split()
        if len(p) < 2: continue
        if not re.fullmatch(r'[A-Za-z_]\w*', p[1]): bad += 1; continue
        got[p[0].lower()] = p[1]
seen = set(); out = []; dup = 0
for a in want:
    n = got.get(a)
    if not n: continue
    if n in seen or n in fn: n = '%s_%s' % (n, a[-4:]); dup += 1
    seen.add(n); out.append('%s %s' % (a, n))
open('globals_JOJOBA.txt', 'w').write('\n'.join(out) + '\n')
print('want', len(want), 'named', len(out), 'missing', len(want) - len(out), 'dup-fixed', dup, 'bad', bad, 'generic', sum(1 for o in out if re.search(r'_[0-9a-f]{4}$', o)))
