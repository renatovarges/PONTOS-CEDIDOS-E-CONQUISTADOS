
# -*- coding: utf-8 -*-
"""Atualiza a funcao gerarArte para usar async/await com lerPlanilha()"""

with open(r'c:\Users\User\.gemini\antigravity\scratch\PONTOS CEDIDOS E CONQUISTADOS\gerar_site.py', encoding='utf-8') as f:
    content = f.read()

OLD = r"""function gerarArte() {{
  if (dadosPlanilha.length === 0) {{
    setStatus('❌ Faça o upload da planilha primeiro!');
    return;
  }}
  rodadaAlvo = parseInt(document.getElementById('sel-rodada').value);
  nJogos = parseInt(document.getElementById('sel-n').value);
  filtroMando = document.getElementById('chk-mando').checked;

  jogosRodadaAtual = rodadasMap[rodadaAlvo] || [];
  if (jogosRodadaAtual.length === 0) {{
    setStatus(`❌ Nenhum jogo encontrado para a Rodada ${{rodadaAlvo}}`);
    return;
  }}

  jogoIdx = 0;
  renderJogo();
  document.getElementById('nav-jogos').style.display = 'flex';
  document.getElementById('arte-container').classList.remove('hidden');
  document.getElementById('btn-download').style.display = 'inline-block';
  document.getElementById('arte-bg').style.backgroundImage = `url(${{BG_B64}})`;
  setStatus('');
}}"""

NEW = r"""async function gerarArte() {{
  const fileInput = document.getElementById('upload-xlsx');
  const file = fileInput.files[0];

  // Se não tem dados na memória, lê o arquivo agora
  if (dadosPlanilha.length === 0) {{
    if (!file) {{
      setStatus('❌ Selecione a planilha antes de gerar a arte!');
      return;
    }}
    setStatus('⏳ Lendo planilha...');
    try {{
      dadosPlanilha = await lerPlanilha(file);
      setStatus(`✅ ${{dadosPlanilha.length}} registros carregados. Gerando arte...`);
    }} catch(err) {{
      setStatus('❌ Erro ao ler planilha: ' + err);
      console.error(err);
      return;
    }}
  }} else if (file && file.name !== dadosPlanilhaArquivo) {{
    // Arquivo diferente foi selecionado – recarrega
    setStatus('⏳ Carregando nova planilha...');
    try {{
      dadosPlanilha = await lerPlanilha(file);
      dadosPlanilhaArquivo = file.name;
      setStatus(`✅ ${{dadosPlanilha.length}} registros carregados. Gerando arte...`);
    }} catch(err) {{
      setStatus('❌ Erro ao ler planilha: ' + err);
      return;
    }}
  }}
  if (file) dadosPlanilhaArquivo = file.name;

  rodadaAlvo = parseInt(document.getElementById('sel-rodada').value);
  nJogos = parseInt(document.getElementById('sel-n').value);
  filtroMando = document.getElementById('chk-mando').checked;

  jogosRodadaAtual = rodadasMap[rodadaAlvo] || [];
  if (jogosRodadaAtual.length === 0) {{
    setStatus(`❌ Nenhum jogo encontrado para a Rodada ${{rodadaAlvo}}`);
    return;
  }}

  jogoIdx = 0;
  renderJogo();
  document.getElementById('nav-jogos').style.display = 'flex';
  document.getElementById('arte-container').classList.remove('hidden');
  document.getElementById('btn-download').style.display = 'inline-block';
  document.getElementById('arte-bg').style.backgroundImage = `url(${{BG_B64}})`;
  setStatus('');
}}"""

if OLD in content:
    content = content.replace(OLD, NEW)
    # Também adiciona a variável de controle do arquivo
    content = content.replace(
        "window.DEBUG_JOGOS = []; // debug da regra de ouro",
        "window.DEBUG_JOGOS = [];\nlet dadosPlanilhaArquivo = ''; // controle de qual arquivo foi carregado"
    )
    with open(r'c:\Users\User\.gemini\antigravity\scratch\PONTOS CEDIDOS E CONQUISTADOS\gerar_site.py', 'w', encoding='utf-8') as f:
        f.write(content)
    print("OK - gerarArte() atualizado para async/await!")
else:
    print("ERRO: padrao nao encontrado")
    # Debug: show what's near gerarArte
    idx = content.find('gerarArte')
    print("Contexto em gerarArte:")
    print(content[idx:idx+400])
