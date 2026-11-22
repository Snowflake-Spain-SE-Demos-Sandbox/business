"""Build index.html for the use-case site from data/cases.json and data/videos.json.

To add a video: put videos/<file>.mp4, .jpg (poster) and .vtt (subtitles) in videos/, add an entry keyed by the
case slug to data/videos.json, run `python3 tools/build_site.py`, then commit and push.
"""
import html, json, os

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
cases = json.load(open(os.path.join(HERE, 'data', 'cases.json'), encoding='utf-8'))
videos = json.load(open(os.path.join(HERE, 'data', 'videos.json'), encoding='utf-8'))
for c in cases:
    if c['slug'] in videos:
        c['video'] = videos[c['slug']]
missing = [s for s in videos if s not in {c['slug'] for c in cases}]
if missing:
    raise SystemExit(f'videos.json slugs with no case: {missing}')
for v in videos.values():
    for ext in ('mp4', 'jpg', 'vtt'):
        p = os.path.join(HERE, 'videos', f"{v['file']}.{ext}")
        if not os.path.exists(p):
            raise SystemExit(f'missing {p}')

ORDER = ["Automoción", "Aeroespacial y Aviación", "Construcción e Inmobiliario", "Energía y Renovables",
         "Banca y Servicios Financieros", "Gobierno y Seguridad", "Salud y Ciencias de la Vida", "Seguros",
         "Logística", "Fabricación e Industria", "Medios y Telecomunicaciones", "Retail y Consumo",
         "Utilities y Química", "Servicios Profesionales", "Transversal"]
inds = [i for i in ORDER if any(c['industria'] == i for c in cases)] + \
       sorted({c['industria'] for c in cases} - set(ORDER))
nvid = sum(1 for c in cases if 'video' in c)
data = json.dumps({'cases': cases, 'industries': inds}, ensure_ascii=False).replace('</', '<\\/')

page = open(os.path.join(HERE, 'tools', 'template.html'), encoding='utf-8').read()
page = (page.replace('{{DATA}}', data)
            .replace('{{N_CASES}}', str(len(cases)))
            .replace('{{N_INDS}}', str(len(inds)))
            .replace('{{N_VIDEOS}}', str(nvid)))
open(os.path.join(HERE, 'index.html'), 'w', encoding='utf-8').write(page)
print(f'index.html: {len(cases)} casos, {len(inds)} industrias, {nvid} vídeos')
