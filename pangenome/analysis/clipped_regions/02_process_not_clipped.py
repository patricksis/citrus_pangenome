import sys, re
pat = re.compile(r'^([^#\[]+)#(\d+)#([^#\[\r\n]+?)(?:#\d+)?\[(\d+)-(\d+)\]$')

inp = sys.argv[1] if len(sys.argv) > 1 else "-"
src = sys.stdin if inp == "-" else open(inp)
for line in src:
    s = line.strip()
    if not s: 
        continue
    m = pat.match(s)
    if not m:
        continue
    hap, hapnum, scaffold, start, end = m.groups()
    start_i = int(start)            # already 0-based
    end_i   = int(end) + 1          
    name = f"{hap}#{hapnum}"
    print(f"{scaffold}\t{start_i}\t{end_i}\t{name}")
if src is not sys.stdin: src.close()
