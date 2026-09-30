"""Write all-screens.svg: every Letshego screen in one file, for a single import into Adobe XD."""
import glob, os, re
os.chdir(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
nat = lambda f: [int(x) if x.isdigit() else x for x in re.split(r'(\d+)', os.path.basename(f))]
web = sorted(glob.glob('web/*.svg'), key=nat); mob = sorted(glob.glob('mobile/*.svg'), key=nat)
parts = []; GAP = 200; LABEL = 60
def body(f):
    t = open(f, encoding='utf-8').read()
    t = re.sub(r'^.*?<svg[^>]*>\s*', '', t, flags=re.S); t = re.sub(r'</svg>\s*$', '', t)
    return re.sub(r'<title>.*?</title>', '', t)
lab = lambda x, y, t: f'<text x="{x}" y="{y}" font-family="Segoe UI" font-size="36" font-weight="600" fill="#1B1C3A">{t}</text>'
cols = 4; W, H = 1920, 1080
for i, f in enumerate(web):
    x = (i % cols) * (W + GAP); y = (i // cols) * (H + GAP + LABEL) + LABEL; n = os.path.basename(f)[:-4]
    parts += [lab(x, y - 16, n), f'<g id="{n}" transform="translate({x} {y})">{body(f)}</g>']
my = ((len(web) + cols - 1) // cols) * (H + GAP + LABEL) + LABEL + 100
for i, f in enumerate(mob):
    x = (i % 8) * 520; yy = my + (i // 8) * (800 + LABEL + 120); n = os.path.basename(f)[:-4]
    parts += [lab(x, yy - 16, '-'.join(n.split('-')[:3])), f'<g id="{n}" transform="translate({x} {yy})">{body(f)}</g>']
TW = cols * W + (cols - 1) * GAP; TH = my + 2 * (800 + LABEL + 120)
open('all-screens.svg', 'w', encoding='utf-8').write(f'<svg xmlns="http://www.w3.org/2000/svg" width="{TW}" height="{TH}" viewBox="0 0 {TW} {TH}">\n' + "\n".join(parts) + '\n</svg>\n')
print(len(web), "web +", len(mob), "mobile in all-screens.svg")
