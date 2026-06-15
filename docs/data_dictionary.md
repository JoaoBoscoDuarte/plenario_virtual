# Dicionário de Dados (resumo) — STF Plenário Virtual

Extraído e adaptado do notebook 01_etl/01_limpeza_preprocessing.ipynb (células de documentação).

## Tabela principal: `processos.parquet` (6.620 registros)

| Coluna | Descrição |
|--------|-----------|
| `incidente` | ID numérico único do processo |
| `classe` | ADI / ADC / ADO / ADPF |
| `nome_processo`, `classe_extenso` | Nome resumido e completo da classe |
| `tipo_processo` | Físico / Eletrônico |
| `relator` | Ministro relator |
| `data_protocolo` | Data de entrada (datetime) |
| `origem`, `origem_orgao`, `autor1` | Metadados de origem e partes |
| `liminar_lista`, `tem_liminar` | Tutelas de urgência requeridas |
| `assuntos_lista`, `assunto_principal` | Temas/assuntos do processo |
| `partes_total` (JSON string) | Lista completa de partes |
| `status_processo` | Finalizado / Em andamento |
| `len(andamentos_lista)` etc. (originais removidos) | Contagens pré-calculadas |

## Tabelas explodidas

- `andamentos.parquet`: cada linha = um andamento. Colunas prefixadas `and_*` + `and_is_virtual` (derivado de termos em nome/complemento).
- `decisoes.parquet`: cada linha = uma decisão. `dec_virtual`, `dec_unanime`, `dec_maioria`, `dec_tipo_orgao` (pleno/turma/monocratica).
- `deslocamentos.parquet`: tramitações físicas/eletrônicas entre unidades. Colunas de data derivadas `*_dt`.

Consulte o notebook ou `src/cleaning.py` + `src/json_transforme.py` para a lógica exata de derivação (TERMOS_VIRTUAL etc.).

## Observações
- Dados públicos do portal do STF.
- Período: ~1988 até dados recentes (datas futuras podem ser programadas).
- Formato: Parquet (pyarrow) para desempenho e fidelidade de tipos.
