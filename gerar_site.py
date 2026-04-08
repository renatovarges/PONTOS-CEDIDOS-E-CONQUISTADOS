
# -*- coding: utf-8 -*-
"""
Gera o index.html usando template.html + substituição de tokens.
SEM f-strings – garante compatibilidade com qualquer JS embutido.
Assets (fontes, imagens, JS) são referenciados por URL relativa em vez de
base64 para manter o HTML pequeno e carregável no Streamlit Cloud.
"""
import base64, os, glob, json

def b64_image(path):
    ext = os.path.splitext(path)[1].lower().lstrip('.')
    mime = {'png':'image/png','jpg':'image/jpeg','jpeg':'image/jpeg','webp':'image/webp'}.get(ext,'image/png')
    with open(path, 'rb') as f:
        return 'data:' + mime + ';base64,' + base64.b64encode(f.read()).decode()

BASE = os.path.dirname(os.path.abspath(__file__))
ASSETS = os.path.join(BASE, 'assets')
OUT = os.path.join(BASE, 'static', 'index.html')
TEMPLATE = os.path.join(BASE, 'template.html')

# ── Carrega template ──────────────────────────────────────────────
with open(TEMPLATE, encoding='utf-8') as f:
    html = f.read()

# ── Fontes (URL relativa, sem base64) ────────────────────────────
MIME_EXT = {'otf': 'opentype', 'ttf': 'truetype', 'woff': 'woff', 'woff2': 'woff2'}
font_faces = []
font_files = (glob.glob(os.path.join(ASSETS, 'fonts', '*.otf')) +
              glob.glob(os.path.join(ASSETS, 'fonts', '*.ttf')) +
              glob.glob(os.path.join(ASSETS, 'fonts', '*.woff')) +
              glob.glob(os.path.join(ASSETS, 'fonts', '*.woff2')))
for fp in sorted(font_files):
    name = os.path.splitext(os.path.basename(fp))[0]
    ext  = os.path.splitext(fp)[1].lower().lstrip('.')
    fmt  = MIME_EXT.get(ext, 'truetype')
    weight = '700' if ('Bold' in name or 'bold' in name) else '400'
    style  = 'italic' if ('Italic' in name or 'italic' in name) else 'normal'
    url = './assets/fonts/' + os.path.basename(fp)
    font_faces.append(
        '@font-face {{ font-family: "Decalotype"; src: url({url}) format("{fmt}"); font-weight: {w}; font-style: {s}; }}'.format(
            url=url, fmt=fmt, w=weight, s=style))
html = html.replace('##FONT_FACES##', '\n'.join(font_faces))

# ── SheetJS e html2canvas (inline para funcionar no srcdoc do Streamlit) ─
xlsx_path = os.path.join(ASSETS, 'xlsx.full.min.js')
h2c_path  = os.path.join(ASSETS, 'html2canvas.min.js')
with open(xlsx_path, encoding='utf-8', errors='replace') as f:
    html = html.replace('##XLSX_JS##', f.read())
with open(h2c_path, encoding='utf-8', errors='replace') as f:
    html = html.replace('##H2C_JS##', f.read())

# ── Rodadas ───────────────────────────────────────────────────────
with open(os.path.join(BASE, 'RODADAS_BRASILEIRAO_2026.txt'), encoding='utf-8') as f:
    rodadas_txt = f.read()
html = html.replace('##RODADAS_TXT_JSON##', json.dumps(rodadas_txt, ensure_ascii=False))

# ── CSV Meias/Volantes ────────────────────────────────────────────
with open(os.path.join(BASE, 'classificacao_meias_volantes.csv'), encoding='utf-8-sig') as f:
    meias_vol_csv = f.read()
html = html.replace('##MEIAS_VOL_CSV_JSON##', json.dumps(meias_vol_csv, ensure_ascii=False))

# ── TXT Atacantes ─────────────────────────────────────────────────
with open(os.path.join(BASE, 'separação atacantes.txt'), encoding='utf-8') as f:
    atacantes_txt = f.read()
html = html.replace('##ATACANTES_TXT_JSON##', json.dumps(atacantes_txt, ensure_ascii=False))

# ── Logo TCC (URL relativa) ───────────────────────────────────────
logo_paths = (glob.glob(os.path.join(ASSETS, 'logos', 'logo_tcc_branco*')) +
              glob.glob(os.path.join(ASSETS, 'logos', 'logo_tcc*')) +
              glob.glob(os.path.join(ASSETS, 'logos', 'logo*')) +
              glob.glob(os.path.join(ASSETS, 'logos', '*.png')))
logo_b64 = b64_image(logo_paths[0]) if logo_paths else ''
html = html.replace('##LOGO_TCC##', logo_b64)

# ── Background (URL — background é texture opcional, cor base fica no CSS) ─
bg_paths = (glob.glob(os.path.join(ASSETS, 'logos', 'background*')) +
            glob.glob(os.path.join(ASSETS, 'logos', 'bg*')))
bg_url = './assets/logos/' + os.path.basename(bg_paths[0]) if bg_paths else ''
html = html.replace('##BG_B64_JSON##', json.dumps(bg_url))

# ── Escudos dos times (URL relativa) ─────────────────────────────
TIMES_MAP = {
    'athletico_pr': ['athleticoPR', 'Athletico-PR', 'athletico', 'cap'],
    'atletico_mg':  ['atleticoMG', 'Atletico', 'atletico_mg', 'galo'],
    'bahia':        ['bahia', 'ECBahia'],
    'botafogo':     ['botafogo', 'Botafogo'],
    'chapecoense':  ['chapecoense'],
    'corinthians':  ['corinthians', 'Corinthians'],
    'coritiba':     ['coritiba', 'Coritiba'],
    'cruzeiro':     ['cruzeiro', 'Cruzeiro'],
    'flamengo':     ['flamengo', 'Flamengo'],
    'fluminense':   ['fluminense', 'Fluminense'],
    'gremio':       ['gremio', 'Gremio'],
    'internacional':['internacional', 'Internacional'],
    'mirassol':     ['mirassol', 'Mirassol'],
    'palmeiras':    ['palmeiras', 'Palmeiras'],
    'red_bull_bragantino': ['bragantino', 'red_bull', 'Bragantino', 'RBB'],
    'remo':         ['remo', 'Remo'],
    'santos':       ['santos', 'Santos'],
    'sao_paulo':    ['saoPaulo', 'sao_paulo', 'spfc'],
    'vasco':        ['vasco', 'Vasco'],
    'vitoria':      ['vitoria', 'Vitoria'],
}

team_images = {}
teams_dir = os.path.join(ASSETS, 'teams')
if os.path.exists(teams_dir):
    all_files = os.listdir(teams_dir)
    for chave, aliases in TIMES_MAP.items():
        found = None
        for alias in aliases:
            for fn in all_files:
                if alias.lower() in fn.lower() and fn.lower().endswith(('.png','.jpg','.jpeg','.webp')):
                    found = fn
                    break
            if found: break
        if not found:
            for fn in all_files:
                if chave.lower() in fn.lower() and fn.lower().endswith(('.png','.jpg','.jpeg','.webp')):
                    found = fn
                    break
        if found:
            team_images[chave] = b64_image(os.path.join(teams_dir, found))

html = html.replace('##TEAM_IMAGES_JSON##', json.dumps(team_images))

# ── Rodada options ────────────────────────────────────────────────
rodada_opts = '\n'.join('<option value="{r}">{r}</option>'.format(r=i) for i in range(1, 39))
html = html.replace('##RODADA_OPTIONS##', rodada_opts)

# ── N options ─────────────────────────────────────────────────────
n_opts = '\n'.join('<option value="{n}"{sel}>{n} jogos</option>'.format(n=i, sel=' selected' if i == 5 else '') for i in range(1, 11))
html = html.replace('##N_OPTIONS##', n_opts)

with open(OUT, 'w', encoding='utf-8') as f:
    f.write(html)

size_mb = os.path.getsize(OUT) / 1024 / 1024
print('index.html gerado com sucesso!')
print('Tamanho: {:.2f} MB'.format(size_mb))
placeholders_restantes = html.count('##')
if placeholders_restantes > 0:
    print('AVISO: {} placeholders nao substituidos!'.format(placeholders_restantes // 2))
else:
    print('Todos os placeholders substituidos corretamente.')
