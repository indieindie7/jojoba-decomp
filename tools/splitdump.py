# split a CsDumpAll dump into N slices on '// ====' boundaries. usage: splitdump.py dump.c outprefix N
import sys
src, pre, n = sys.argv[1], sys.argv[2], int(sys.argv[3])
parts = open(src, encoding='utf-8', errors='replace').read().split('\n// ==== ')
head, funcs = parts[0], ['// ==== ' + p for p in parts[1:]]
if head.startswith('// ===='): funcs.insert(0, head)
total = sum(len(f) for f in funcs); per = total / n
cur, size, k = [], 0, 1
for f in funcs:
    cur.append(f); size += len(f)
    if size >= per and k < n:
        open('%s_%d.c' % (pre, k), 'w', encoding='utf-8').write('\n'.join(cur)); k += 1; cur, size = [], 0
open('%s_%d.c' % (pre, k), 'w', encoding='utf-8').write('\n'.join(cur))
print(len(funcs), 'funcs ->', k, 'slices')
