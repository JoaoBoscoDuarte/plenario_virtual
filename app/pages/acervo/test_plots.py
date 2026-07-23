"""Smoke test do modelo visual de plotar_grafico_stf (padrão 1.b2)."""
import pandas as pd

from pages.acervo.plots import plotar_grafico_stf, _CORES_CLASSE


def _df_fake() -> pd.DataFrame:
    anos = list(range(2016, 2026))
    rows = []
    for ano in anos:
        for classe, base in [("ADI", 100), ("ADPF", 40), ("ADC", 10), ("ADO", 5)]:
            rows.append({"ano": ano, "classe": classe, "quantidade_ativos": base + ano - 2016})
    return pd.DataFrame(rows)


def test_total_usa_azul_e_tem_er_espin():
    df = _df_fake()
    fig = plotar_grafico_stf(df, "TOTAL", "quantidade_ativos", "Processos Ativos", show_values=True)
    assert fig.layout.height == 650
    assert fig.layout.margin.t == 150 and fig.layout.margin.b == 70
    assert fig.data[0].marker.color == "#2563EB"
    # eixo categórico por ano (igual 1.b2), não numérico contínuo
    assert list(fig.data[0].x) == [str(a) for a in range(2016, 2026)]
    # linhas ER (51/52/53) + vrect ESPIN + anotações "ER" e "ESPIN"
    shape_colors = {s.line.color for s in fig.layout.shapes if s.type == "line"}
    assert "#000000" in shape_colors  # ER
    assert "#C00000" in shape_colors  # ESPIN
    ann_texts = " ".join(a.text for a in fig.layout.annotations)
    assert "ER" in ann_texts and "ESPIN" in ann_texts
    assert fig.layout.legend.y == 0.95
    assert fig.layout.xaxis.tickfont.size == 22


def test_classe_usa_cor_do_bloco1_e_titulo_dinamico():
    df = _df_fake()
    fig = plotar_grafico_stf(df, "ADPF", "quantidade_ativos", "Processos Ativos", show_values=False)
    assert fig.data[0].marker.color == _CORES_CLASSE["ADPF"]
    # título deve conter o nome da classe (história calculada a partir dos dados reais, não fixa)
    assert "ADPF" in fig.layout.title.text


if __name__ == "__main__":
    test_total_usa_azul_e_tem_er_espin()
    test_classe_usa_cor_do_bloco1_e_titulo_dinamico()
    print("ok")
