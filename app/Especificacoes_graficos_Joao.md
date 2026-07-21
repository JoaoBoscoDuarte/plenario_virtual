# ESPECIFICAÇÕES DOS GRÁFICOS — UM POR UM
### Documento para reprodução (acompanha `Codigos_graficos_completos.py`, que tem o código exato de cada peça)

## PADRÃO GERAL (vale para todos)
Fontes pretas sólidas (#000000), rótulos e anos em **negrito**; sem grade de
fundo; sem eixo secundário; sem linha de total; sem rodapé de fonte (a legenda
ABNT vai no documento); título afirma o achado; barras verticais quando o eixo
é tempo. Marcadores das emendas: linha tracejada preta na **fração exata do
mês** (ER 51 = 22/06/2016; ER 52 = 14/06/2019; ER 53 = 18/03/2020), rótulo
"ER" sobre o número, acima da linha, sem tocá-la. ESPIN: sombreado rosa suave
(#FCE7F3) + duas linhas vermelhas tracejadas nas frações exatas
(03/02/2020 e 22/04/2022) + seta ↔ e rótulo "ESPIN" rebaixados, SEM data.
Números negativos: rótulo em PRETO (barra vermelha #C00000). Pares comparativos
sempre com a MESMA escala. Cores base: azul #2563EB, azul-claro #93C5FD,
cinza #9CA3AF, verde #059669, roxo #7C3AED, vermelho #C00000.

---

## BLOCO 1

**1.a — Variação trienal do acervo, 1988-2025** (script: bloco1_final.py)
Barras verticais, 13 triênios ancorados em 1988 (último = biênio 2024-2025*).
Valores: +397 +377 +272 +286 +106 +201 −28 +222 +173 +351 −537 −540 −249.
Positivas cinza, negativas vermelhas, rótulo preto negrito sobre/sob cada
barra. SEM marcadores de emenda (escala trienal não comporta).

**1.b — Acervo por classe, vertical, 1988-2025** (b1b_v3.py)
38 colunas empilhadas ADI/ADPF/ADC/ADO; SEM rótulos de totais (silhueta; o
destrinchamento vem depois); marcadores ER e ESPIN no padrão; legenda das
classes no topo esquerdo. Fonte de dados: CSV do acervo, colunas "* Ativos".

**1.b2 — Acervo por classe, horizontal, 1988-2025** (b1b2.py) [candidato
alternativo ao 1.b — decisão editorial pendente]
Barras horizontais, 1988 no topo; COM totais anuais na ponta (preto, negrito);
ER como linhas horizontais na fração do mês, rótulo centralizado na altura da
linha, à direita; ESPIN com seta vertical e rótulo alinhado ao total 2.114;
legenda empilhada no canto superior direito.

**1.c — Distribuição e baixa espelhado, 1988-2025** (final_1c1d.py)
Colunas espelhadas: distribuição (azul) acima do zero, baixa (cinza) abaixo.
Escala única real −920 a +940, sem simetria forçada. Números citados no
texto: 572 (2021↑), 251 (2025↑), 336 (2023↑), 797 (2020↓), 608 (2023↓).
Marcadores ER/ESPIN elevados (linhas até ~800), ESPIN texto acima da seta.
Nota da legenda ABNT: colunas de baixo = quantidade de baixas, não negativos.

**1.d — Variação anual, 1988-2025** (final_1c1d.py)
Barras anuais, positivas cinza, negativas vermelhas. Rótulos (pretos):
+237 (1990), −294 (2020, fonte maior), −112 (2024) e −137 (2025) escalonados
para não se tocarem. Marcadores no padrão, ESPIN rebaixado, linhas curtas
(teto 520, linha até 390) proporcionais à parte de baixo.

---

## BLOCO 2 — série estendida (base: inclusoes_em_pauta 2016-2025 CORRIGIDA*)

*Correção obrigatória na base: 264 linhas de 2016-2019 têm o sufixo recursal
apenas no texto do complemento (formato histórico "Julgamento Virtual:
ADI-ED"); extrair por regex `\b(?:ADI|ADPF|ADC|ADO)-([A-Za-zÀ-ú\-]+)` onde
sufixo_extraido vazio; AgR/ED/Emb → RC; MC/Ref/QO → IJ. Sem isso, 2018
aparece com 32 falsos "principais".

**2.a — Participação % do PV por ano, 2016-2025** (antes.py)
Barras azuis; valores: 4,0 11,4 10,0 38,7 59,8 68,0 64,1 66,8 59,0 66,6.
Linha tracejada vermelha "fim da ESPIN" entre 2022 e 2023 (x=6,45) — MANTER,
é o argumento do Bloco 3. Título: "De 4% a dois terços da pauta: o degrau da
universalização" .

**2.b — Inclusões por ano e ambiente, 2016-2025** (antes.py)
Barras agrupadas PV (azul) × PP (cinza). PV: 12 46 84 473 954 882 758 927
638 648. PP: 287 359 758 749 641 416 424 461 443 325. Rótulos sobre todas.
Título: "O salto das inclusões no ambiente virtual".

**2.c — Composição do PV por tipo de questão, 2016-2019** (antes.py)
Colunas empilhadas RC (verde) / PR (azul) / IJ (cinza) por ano:
2016 = 12 RC; 2017 = 46 RC; 2018 = 84 RC; 2019 = 350 PR + 119 RC + 4 IJ.
Total sobre cada coluna; parcelas dentro quando couber. Título: "Em 2019, o
ambiente virtual deixa de ser exclusivamente recursal".

**2.e — Inclusões por classe e ano, PV, 2020-2025** (ef_final.py)
4 classes × 6 anos, escala 0-860 IGUAL ao 2.f; rótulos sobre barras >0.

**2.f — idem, Plenário Presencial** (ef_final.py). Mesma escala 0-860.

**2.h — Tramitação anual, 2020-2025** (tram_anual.py) [pode ser substituído
pelo 2.i no corpo]
Só Virtual: 651 580 554 486 391 375; Ambos: 94 61 40 111 44 53;
Só Presencial: 207 133 90 82 79 54. Título: "A tramitação exclusivamente
presencial torna-se residual". Subtítulo declara o critério anual.

**2.i — Tramitação anual, 2016-2025** (antes.py)
Estende o 2.h: 2016 = 12/0/262; 2017 = 34/4/234; 2018 = 58/17/489;
2019 = 292/88/318; 2020-2025 como no 2.h. Título: "O cruzamento: o virtual
ultrapassa o presencial em 2020".

**2.j — Destino dos recursos, 2020-2025** (bloco2b.py — aplicar padrão novo)
Barra única empilhada: PV 94,3% (1.048) × PP 5,7% (63).

**2.k1 — Tipo de questão × ambiente, 2016-2019** (antes.py)
Agrupado: PV 350 PR / 261 RC / 4 IJ; PP 1.924 / 108 / 121. Título: "Antes da
universalização, o mérito era do presencial; os recursos já migravam".

**2.k2 — idem, 2020-2025** (k2.py)
PV 3.383 / 1.048 / 376; PP 2.566 / 63 / 81. Título aprovado: "Especialização
dos ambientes: o presencial dedica-se aos processos principais e a atividade
recursal migrou para o virtual" [ou a versão curta em uso no PNG].

**2.l — Pauta × concluídos, 2020-2025** (bloco2b.py — aplicar padrão novo)
Duas barras: 63,9% e 91,3%.

**2.m / 2.n — Desfecho por categoria e ano, PV / PP, 2020-2025** (bloco2b.py
— aplicar padrão novo). Unânime/Maioria/Não concluído por ano; escala comum
0-600 nos dois.

**2.o / 2.p — Não concluídos por categoria e ano, PV / PP** (naoconcl.py —
aplicar padrão novo). Vista/Destaque/Retirado/Diversos; escala comum 0-450.

**2.q — Média de inclusões por processo** (bloco2b.py — padrão novo)
Duas barras: PV 1,8 × PP 4,3.

**2.r — % de processos com julgamento concluído** (bloco2b.py — padrão novo)
Duas barras: PV 86,0% × PP 39,2%.

**3.1 — Tramitação por período, 2016-2019** (antes.py)
3 barras horizontais: só virtual 277 (20,9%), ambos 214 (16,1%),
só presencial 837 (63,0%). ESCALA X 0-2600, PAREADA com o 3.2.

**3.2 — Tramitação por período, 2020-2025** (tram_par.py)
Só virtual 2.197 (77,5%), ambos 478 (16,9%), só presencial 159 (5,6%).
Escala X 0-2600.

**[OPCIONAL, decisão pendente] BORBOLETA 3.1+3.2 em peça única**
Categorias ao centro; asa esquerda 2016-2019 (cinza), asa direita 2020-2025
(azul); barras em PERCENTUAL (0-100 cada lado), rótulo "63,0% (837)";
cabeçalhos dos períodos em negrito; linha preta no zero. Se entrar, os 3.1 e
3.2 individuais saem do corpo.

---

## OBSERVAÇÃO FINAL
Os oito marcados "aplicar padrão novo" (2.j, 2.l, 2.m, 2.n, 2.o, 2.p, 2.q,
2.r) estão com o código funcional mas no acabamento antigo (fontes cinza,
rodapé de fonte); ao reproduzir, aplicar o PADRÃO GERAL do topo. Todos os
demais códigos já saem no padrão final.
