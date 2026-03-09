
# -*- coding: utf-8 -*-
"""Substitui os scripts CDN por inline no gerar_site.py"""
import re

with open(r'c:\Users\User\.gemini\antigravity\scratch\PONTOS CEDIDOS E CONQUISTADOS\gerar_site.py', encoding='utf-8') as f:
    content = f.read()

# Encontra e substitui as tags de CDN
pattern = r'<!-- SheetJS para leitura do xlsx -->\n<script src="https://cdn\.jsdelivr\.net/npm/xlsx@[^"]+"></script>\n<!-- html2canvas para exportação PNG -->\n<script src="https://cdn\.jsdelivr\.net/npm/html2canvas@[^"]+"></script>'

replacement = '''<!-- SheetJS (embutido, sem CDN) -->
<script>{xlsx_js}</script>
<!-- html2canvas (embutido, sem CDN) -->
<script>{h2c_js}</script>'''

new_content = re.sub(pattern, replacement, content)
if new_content == content:
    print("ERRO: padrao nao encontrado!")
    # Mostra o que existe perto de cdn.jsdelivr
    idx = content.find('cdn.jsdelivr')
    if idx >= 0:
        print("Encontrado em:", idx)
        print(repr(content[idx-100:idx+300]))
    else:
        print("cdn.jsdelivr nao encontrado no arquivo!")
else:
    with open(r'c:\Users\User\.gemini\antigravity\scratch\PONTOS CEDIDOS E CONQUISTADOS\gerar_site.py', 'w', encoding='utf-8') as f:
        f.write(new_content)
    print("OK - substituicao feita com sucesso!")
