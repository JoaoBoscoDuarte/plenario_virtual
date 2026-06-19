# Lista de Gráficos — Controle de Implementação

Este documento é o controle oficial de implementação dos gráficos listados em `LISTA DE GRÁFICOS.docx`.

**Colunas:**
- # (número original)
- BLOCO
- GRÁFICO A SER PRODUZIDO
- OBSERVAÇÕES (resumo)
- Implementado (Sim / Não / Parcial)
- Pagina (nome da página ou seção no app/, ex: `acervo.py`, `inclusoes.py`)
- Notebook de processamento (caminho do notebook que gerou os dados para comprovação)

> **Importante:** Só devem ser implementados os gráficos que aparecem nesta lista. Nenhum gráfico adicional.

| # | BLOCO | GRÁFICO A SER PRODUZIDO | OBSERVAÇÕES (resumo) | Implementado | Pagina | Notebook de processamento |
|---|-------|--------------------------|----------------------|--------------|--------|---------------------------|
| 1 | ACERVO | Evolução anual do acervo – geral | 1988 a 2025. Excluir processos com baixa definitiva ao longo do ano (ou usar critério de "processos ativos"). Snapshot 31/12. | Parcial | `acervo.py` (Gráfico Geral) | (a definir) |
| 2 | ACERVO | Evolução anual do acervo – por classe | Idem ao anterior, separado por classe (ADI, ADC, ADO, ADPF). | Parcial | `acervo.py` (Gráfico por Classe + Geral) | (a definir) |
| 3 | BAIXA | Número de processos que tiveram baixa, por classe | 1988 a 2025, anual, 31/12. | Não | | |
| 4 | DISTRIBUIÇÃO | Número de processos distribuídos, por classe | 1988 a 2025, anual, 31/12. | Não | | |
| 5 | INCLUSÕES EM PAUTA | Geral. Anual PV e PP | 2020-2025 anual. PV e PP (comparação). Unidade: inclusão em pauta. | Não | | |
| 6 | INCLUSÕES EM PAUTA | Por classe. Anual PV | 2020-2025 anual, por classe, PV. | Não | | |
| 7 | INCLUSÕES EM PAUTA | Por classe. Anual PP | 2020-2025 anual, por classe, PP. | Não | | |
| 8 | INCLUSÕES EM PAUTA | Geral. Período. Concluídos e Não Concluídos. PV | 2020-2025. Separar concluídos / não. | Não | | |
| 9 | INCLUSÕES EM PAUTA | Geral. Período. Concluídos e Não Concluídos. PP | Idem no PP. | Não | | |
| 10 | INCLUSÕES EM PAUTA | Geral. Anual. Concluídos e Não. PV | Anual, PV. | Não | | |
| 11 | INCLUSÕES EM PAUTA | Geral. Anual. Concluídos e Não. PP | Anual, PP. | Não | | |
| 12 | INCLUSÕES EM PAUTA | Geral. Concluídos. PV | Excluindo não concluídos. | Não | | |
| 13 | INCLUSÕES EM PAUTA | Geral. Concluídos. PP | Idem PP. | Não | | |
| 14 | INCLUSÕES EM PAUTA | Por classe. Não Concluídos. PV | Por classe. | Não | | |
| 15 | INCLUSÕES EM PAUTA | Por classe. Não Concluídos. PP | Por classe, PP. | Não | | |
| 16 | INCLUSÕES EM PAUTA | Por classe. Concluídos. PV | Por classe. | Não | | |
| 17 | INCLUSÕES EM PAUTA | Por classe. Concluídos. PP | Por classe, PP. | Não | | |
| 18 | TIPO DE QUESTÃO | Geral. Não Concluídos. PV | Por tipo de questão (PR, RC ou IJ). | Não | | |
| 19 | TIPO DE QUESTÃO | Geral. Não Concluídos. PP | Idem PP. | Não | | |
| 20 | TIPO DE QUESTÃO | Geral. Concluídos. PV | Por tipo de questão. | Não | | |
| 21 | TIPO DE QUESTÃO | Geral. Concluídos. PP | Idem PP. | Não | | |
| 22 | DESFECHO CONCLUÍDO | por CATEGORIA. Período. PV | Categorias: unânime, maioria com relator, maioria vencido relator + bloco não concluído. | Não | | |
| 23 | DESFECHO CONCLUÍDO | por CATEGORIA. Período. PP | Idem PP. | Não | | |
| 24 | DESFECHO CONCLUÍDO | por CATEGORIA. Por Ano. PV | Por ano. | Não | | |
| 25 | DESFECHO CONCLUÍDO | por CATEGORIA. Por Ano. PP | Por ano, PP. | Não | | |
| 26 | DESFECHO CONCLUÍDO | por CATEGORIA e TIPO DE QUESTÃO. Período. PV | + tipo de questão. | Não | | |
| 27 | DESFECHO CONCLUÍDO | por CATEGORIA e TIPO DE QUESTÃO. Período. PP | + tipo de questão, PP. | Não | | |
| 28 | DESFECHO CONCLUÍDO | por CATEGORIA e TIPO DE QUESTÃO. Por Ano. PV | Por ano. | Não | | |
| 29 | DESFECHO CONCLUÍDO | por CATEGORIA e TIPO DE QUESTÃO. Por Ano. PP | Por ano, PP. | Não | | |
| 30 | DESFECHO NÃO CONCLUÍDO | por CATEGORIA. Anual. PV | Categorias: pedido de vista, destaque, motivos diversos. | Não | | |
| 31 | DESFECHO NÃO CONCLUÍDO | por CATEGORIA. Anual. PP | Idem PP (destaque = 0). | Não | | |
| 32 | DESFECHO NÃO CONCLUÍDO | por CATEGORIA. Anual. Por Classe. PV | Por classe. | Não | | |
| 33 | DESFECHO NÃO CONCLUÍDO | por CATEGORIA. Anual. Por Classe. PP | Por classe, PP. | Não | | |
| 34 | DESFECHO NÃO CONCLUÍDO | por CATEGORIA. Anual. Tipo de Questão. PV | + tipo de questão. | Não | | |
| 35 | DESFECHO NÃO CONCLUÍDO | por CATEGORIA. Anual. Tipo de Questão. PP | + tipo de questão, PP. | Não | | |
| - | DESTAQUES CANCELADOS | Geral. Período | Processos com andamento “destaque cancelado”. 2020-2025. | Não | | |
| - | REAJUSTE DE VOTO | Geral. Período. PV | Expressões específicas + menção a ministro/relator. | Não | | |
| - | REAJUSTE DE VOTO | Geral. Período. PP | Idem PP. | Não | | |
| - | REAJUSTE DE VOTO | Geral. Ano. PV | Anual. | Não | | |
| - | REAJUSTE DE VOTO | Geral. Ano. PP | Anual, PP. | Não | | |
| - | REAJUSTE DE VOTO | Anual. Classe. PV | Por classe. | Não | | |
| - | REAJUSTE DE VOTO | Anual. Classe. PP | Por classe, PP. | Não | | |
| - | TRAMITAÇÃO NOS 2 AMBIENTES | Geral. Período | Processos que tramitaram nos dois ambientes. | Não | | |
| - | TRAMITAÇÃO NOS 2 AMBIENTES | Geral. Período. Tipo de Questão | + tipo de questão. | Não | | |
| - | SUSTENTAÇÃO ORAL | Período. PV | 2020-2025. | Não | | |
| - | SUSTENTAÇÃO ORAL | Período. PP | Idem PP. | Não | | |
| - | SUSTENTAÇÃO ORAL | Anual. PV | Anual. | Não | | |
| - | SUSTENTAÇÃO ORAL | Anual. PP | Anual, PP. | Não | | |

**Notas de preenchimento:**
- Atualizar "Implementado" para "Sim" quando o gráfico estiver funcionando com os filtros globais e regras aplicáveis.
- "Pagina": nome do arquivo em `app/pages/` ou seção (ex: "acervo.py - Gráfico 2", "inclusoes_pauta.py").
- "Notebook de processamento": caminho relativo ao notebook que gerou o dado (ex: `notebooks/gerar_acervo.ipynb`).

---

**Regras Globais a serem aplicadas (quando fizer sentido):**
- Toggle "Exibir valores nos gráficos"
- Filtro de intervalo de anos (gráficos com "ano" no eixo X)
- Seletor de classe + "Geral (todas as classes)" (agregado)
- Para o gráfico de evolução do acervo: radio Linha/Barras + checkbox de rótulos
- Valores absolutos + percentual no hover
- Descrição do critério/caminho visível para cada gráfico

**Status geral:** Em planejamento / início de implementação.