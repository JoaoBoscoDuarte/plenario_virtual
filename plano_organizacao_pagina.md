# Plano de Organização: Padronização das Páginas

## 1. Objetivo

Padronizar todas as páginas do app (tramitação, sustentação, acervo, geral) seguindo o modelo estabelecido nas páginas **inclusões** e **reajuste**. O padrão cobre:

- Catálogo de gráficos em `_CATALOGO` (lista de tuplas padronizadas)
- Merge de pares PV/PP → funções únicas com parâmetro `ambiente` + `st.selectbox("Âmbito", ...)`
- `show_values` checkbox para todo gráfico de barra/pizza
- `_render_tabela` com `_TABELA_SPECS` (tabela pivot por gráfico)
- Tabulador Interativo (R9/S9/T10) com `gt10_tabulador` + tabela de apoio
- `render_graficos` com `_SUMARIO` em expander, selectbox, per-chart rendering
- Remoção de `dados_brutos` e `tabela consolidada` pesadas → cada página só tem `_render_tabela` e/ou `_render_interactive_tabulador`

## 2. Arquitetura padrão por página

```
app/pages/<pagina>/
├── <pagina>.py          # entry point: carrega dados, chama render_graficos
├── plots.py             # funções que retornam go.Figure (nomes: gsX_*, grX_*, gtX_*, etc.)
└── layout.py            # _CATALOGO, _SUMARIO, _TABELA_SPECS, _build_tabela, _render_tabela, _render_interactive_tabulador, render_graficos
```

## 3. Padrões de código

### 3.1 `_CATALOGO` — catálogo de gráficos

```python
_CATALOGO = [
    (
        "R1/R2 — Rótulo visível no selectbox",
        "Subtítulo exibido acima do gráfico",
        "Descrição/caption exibida abaixo do subtítulo.",
        funcao_do_grafico,       # pode ser None para o tabulador interativo
    ),
    ...
]
_LABELS = [item[0] for item in _CATALOGO]
```

**Regras:**
- O último item do catálogo é SEMPRE o Tabulador Interativo com `fn=None`
- Pares PV/PP viram entrada única com notação `Rx/Ry` no label e `"Selecione o âmbito."` na descrição
- `fn` aceita `(df, show_values=..., **kwargs)` — nunca mais `proporcao` ou outros params obsoletos

### 3.2 `_SUMARIO` — sumário em expander

```python
_SUMARIO = {
    "Período total (R1/R2)": [
        "R1/R2 — proporção com/sem reajuste (Plenário Virtual e Plenário Presencial)",
    ],
    "Evolução anual (R3/R4)": [
        "R3/R4 — volume por ano (Plenário Virtual e Plenário Presencial)",
    ],
    "Livre (R9)": [
        "R9 — tabulador gráfico interativo",
    ],
}
```

### 3.3 `_TABELA_SPECS` + `_build_tabela` + `_render_tabela`

```python
_TABELA_SPECS: dict[int, tuple[str, str | None]] = {
    0: ("col_linha", "col_grupo"),
    1: ("ano", "col_grupo"),
    ...
}

def _build_tabela(df: pd.DataFrame, spec: tuple[str, str | None]) -> pd.DataFrame:
    col_linha, col_grupo = spec
    d = df.copy()
    # TODO: ajustes específicos da página (mapear bool, renomear IJ→QI, etc.)
    tab = d.groupby([col_linha, col_grupo], observed=True).size().reset_index(name="n")
    pvt = tab.pivot_table(index=col_linha, columns=col_grupo, values="n", fill_value=0)
    pvt["Total"] = pvt.sum(axis=1)
    pvt.loc["Total"] = pvt.sum()
    pvt = pvt.reset_index()
    pvt[pvt.columns[0]] = pvt[pvt.columns[0]].astype(str)  # ← previne erro Arrow mixed types
    return pvt

def _render_tabela(df: pd.DataFrame, idx: int) -> None:
    spec = _TABELA_SPECS.get(idx)
    if spec is None:
        return
    with st.expander("📊 Dados da tabulação"):
        tab = _build_tabela(df, spec)
        fmt = {c: "{:,.0f}" for c in tab.columns if c != tab.columns[0]}
        st.dataframe(tab.style.format(fmt, na_rep="—"), width="stretch", height=280)
```

### 3.4 Merge de pares PV/PP

**Antes (página sustentação, tramitação antiga):**
```python
gs1_pizza_pv(df)   → pizza PV
gs2_pizza_pp(df)   → pizza PP
```

**Depois (padrão reajuste/inclusões):**
```python
def gs1_sust_filtravel(df, show_values=True, ambiente="Plenário Virtual"):
    return _pizza_sust(df[df["ambiente"] == ambiente], ...)
```

No `render_graficos`, o seletor de âmbito aparece condicionalmente:
```python
if idx <= <indice_ultimo_merge>:
    ambiente = st.selectbox("Âmbito", ["Plenário Virtual", "Plenário Presencial"], key=f"...")
    fig = fn(df, show_values=show_values, ambiente=ambiente)
else:
    fig = fn(df, show_values=show_values)
```

### 3.5 Tabulador Interativo

Usa `gt10_tabulador` (definido em `tramitacao/plots.py`). Cada página define seus `_PREDEFINIDOS_TAB` com tuplas `(label, eixo_x, eixo_y, metrica, barmode)`.

A função `_render_interactive_tabulador` em `layout.py`:
- Selectbox de pré-definidos
- 5 colunas: Eixo X, Eixo Y (grupo), Métrica, Modo, Exibir valores
- Valida se eixos são diferentes
- Plota o gráfico
- **Embaixo do gráfico**: tabela pivot com mesmos eixos (igual inclusões)

```python
def _render_interactive_tabulador(df: pd.DataFrame) -> None:
    ...
    st.plotly_chart(gt10_tabulador(df, eixo_x, eixo_y, metrica, barmode, show_values_tab), width="stretch")
    st.markdown("---")
    st.subheader("Tabela — mesmos eixos")
    d = df.copy()
    # ajustes específicos da página
    if metrica == "processos":
        d = d.drop_duplicates("incidente")
    tab = d.groupby([eixo_x, eixo_y], observed=True).size().reset_index(name="n")
    if barmode == "100%":
        totais = tab.groupby(eixo_x)["n"].transform("sum")
        tab["n"] = (tab["n"] / totais * 100).round(1)
    pvt = tab.pivot_table(index=eixo_x, columns=eixo_y, values="n", fill_value=0)
    pvt["Total"] = pvt.sum(axis=1)
    pvt.loc["Total"] = pvt.sum()
    pvt = pvt.reset_index()
    pvt[pvt.columns[0]] = pvt[pvt.columns[0]].astype(str)
    fmt = {c: "{:,.0f}" for c in pvt.columns if pvt[c].dtype.kind in "iuf"}
    st.dataframe(pvt.style.format(fmt, na_rep="—"), width="stretch", height=280)
```

### 3.6 `render_graficos` — entry point

```python
def render_graficos(df: pd.DataFrame) -> None:
    with st.expander("Sumário — visualizações disponíveis", expanded=True):
        cols = st.columns(2)
        for i, (bloco, graficos) in enumerate(_SUMARIO.items()):
            with cols[i % 2]:
                st.markdown(f"**{bloco}**")
                for g in graficos:
                    st.markdown(f"- {g}")

    st.markdown("---")

    escolha = st.selectbox("Selecione a visualização", options=_LABELS, index=0, key="...")

    idx = _LABELS.index(escolha)
    _, subtitulo, descricao, fn = _CATALOGO[idx]

    if fn is None:
        _render_interactive_tabulador(df)
        return  # ← não renderiza tabela extra (já vem dentro do tabulador)

    st.subheader(subtitulo)
    st.caption(descricao)

    show_values = st.checkbox("Exibir valores", value=True, key=f"..._sv_{idx}")

    # Se for gráfico mergeado (PV/PP), mostra seletor de âmbito
    if idx <= <ultimo_indice_merge>:
        ambiente = st.selectbox(
            "Âmbito", ["Plenário Virtual", "Plenário Presencial"],
            key=f"..._amb_{idx}",
        )
        fig = fn(df, show_values=show_values, ambiente=ambiente)
    else:
        fig = fn(df, show_values=show_values)

    st.plotly_chart(fig, width="stretch")
    _render_tabela(df, idx)
```

**Checklist da função:**
- [ ] `_SUMARIO` em expander
- [ ] `st.selectbox` com `_LABELS`
- [ ] `fn is None` → `_render_interactive_tabulador` + `return`
- [ ] `show_values` checkbox para todo gráfico
- [ ] `st.selectbox("Âmbito")` para índices mergeados
- [ ] `fn(df, show_values=show_values, ambiente=ambiente)` ou `fn(df, show_values=show_values)`
- [ ] `st.plotly_chart(fig, ...)`
- [ ] `_render_tabela(df, idx)`

## 4. O que remover

- ❌ `_render_dados_brutos` — removido. Dados brutos não têm lugar numa página de visualização.
- ❌ `_render_tabela_consolidada` / `_build_tabulador` (a tabelona com Total por Ano/Ambiente/Classe) — substituída pelo `_render_tabela` por gráfico + Tabulador Interativo.
- ❌ Funções PV/PP separadas — viram funções únicas com param `ambiente`.
- ❌ Parâmetro `proporcao` — removido de todas as funções.
- ❌ Nomes de variáveis com typo (`_CATAlOGO_TEMP`, etc.) — corrigir.

## 5. Páginas a migrar (checklist)

### 5.1 Sustentação Oral (`sustentacao/`)
- [ ] Merge S1/S2 → `gs1_sust_filtravel` com `ambiente` param + `_pizza_sust` helper
- [ ] Merge S3/S4 → `gs3_sust_anual_filtravel` com `ambiente` param
- [ ] Merge S5/S6 → `gs5_sust_classe_filtravel` com `ambiente` param
- [ ] Adicionar `_TABELA_SPECS` + `_build_tabela` + `_render_tabela`
- [ ] Substituir `_render_tabela_consolidada` por `_render_tabela` (chamado após cada gráfico)
- [ ] Remover `_render_dados_brutos`
- [ ] Atualizar `render_graficos` para padrão
- [ ] Adicionar tabela no tabulador interativo (mesmos eixos)

### 5.2 Tramitação (`tramitacao/`)
- [ ] Adicionar `_SUMARIO` em expander
- [ ] Adicionar `_TABELA_SPECS` + `_build_tabela` + `_render_tabela` (substituir tabela consolidada fixa)
- [ ] Adicionar tabela no tabulador interativo (mesmos eixos)
- [ ] Garantir `show_values` checkbox para todos os gráficos
- [ ] Avaliar merge de charts PV/PP (T7, T8 são dicts de pizza, talvez manter como estão ou criar seletor sub-aba)

### 5.3 Acervo (`acervo/`)
- [ ] [Verificar estado atual e aplicar padrão]

### 5.4 Geral (`geral/`)
- [ ] [Verificar estado atual e aplicar padrão]

## 6. Testes

Após migrar cada página, verificar:
```bash
python3 -m py_compile app/pages/<pagina>/plots.py
python3 -m py_compile app/pages/<pagina>/layout.py
streamlit run app/app.py  # teste visual
```
