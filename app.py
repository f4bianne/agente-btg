import re
import unicodedata

import pandas as pd
import plotly.express as px
import streamlit as st


# =========================================================
# CONFIGURAÇÃO DA PÁGINA
# =========================================================

st.set_page_config(
    page_title="Ofertas Primárias | BTG Pactual",
    page_icon="📊",
    layout="wide"
)


# =========================================================
# CORES
# =========================================================

BG = "#050B18"
BG_2 = "#08111F"
CARD = "#101B2D"
CARD_2 = "#13243A"
BORDER = "#22324A"
BLUE = "#2F80ED"
CYAN = "#56CCF2"
TEXT = "#F8FAFC"
MUTED = "#B8C2D6"
SOFT = "#8EA4C8"


# =========================================================
# CSS
# =========================================================

st.markdown(
    f"""
    <style>
        .stApp {{
            background: linear-gradient(135deg, {BG} 0%, {BG_2} 60%, #0B1730 100%);
            color: {TEXT};
        }}

        .block-container {{
            padding-top: 1.4rem;
            padding-bottom: 2rem;
            max-width: 1450px;
        }}

        section[data-testid="stSidebar"] {{
            background-color: #050B18;
            border-right: 1px solid {BORDER};
        }}

        section[data-testid="stSidebar"] * {{
            color: {TEXT} !important;
        }}

        .hero {{
            background: linear-gradient(120deg, #071B3A, #0A2A5C);
            border: 1px solid {BORDER};
            border-radius: 22px;
            padding: 28px 32px;
            margin-bottom: 22px;
            box-shadow: 0 14px 32px rgba(0,0,0,0.35);
        }}

        .eyebrow {{
            color: {CYAN};
            font-size: 0.8rem;
            letter-spacing: 0.12em;
            font-weight: 800;
            text-transform: uppercase;
            margin-bottom: 8px;
        }}

        .title {{
            color: {TEXT};
            font-size: 2.25rem;
            font-weight: 850;
            line-height: 1.15;
            margin-bottom: 8px;
        }}

        .subtitle {{
            color: {MUTED};
            font-size: 1rem;
            line-height: 1.55;
            max-width: 980px;
        }}

        .metric-card {{
            background: {CARD};
            border: 1px solid {BORDER};
            border-radius: 18px;
            padding: 20px;
            min-height: 125px;
            box-shadow: 0 10px 26px rgba(0,0,0,0.26);
        }}

        .metric-label {{
            color: {SOFT};
            font-size: 0.86rem;
            font-weight: 700;
            margin-bottom: 10px;
        }}

        .metric-value {{
            color: {TEXT};
            font-size: 1.75rem;
            font-weight: 850;
            margin-bottom: 6px;
        }}

        .metric-help {{
            color: {MUTED};
            font-size: 0.8rem;
            line-height: 1.35;
        }}

        .section-card {{
            background: {CARD};
            border: 1px solid {BORDER};
            border-radius: 18px;
            padding: 22px 24px;
            margin-bottom: 18px;
            box-shadow: 0 10px 26px rgba(0,0,0,0.22);
        }}

        .section-title {{
            color: {TEXT};
            font-size: 1.25rem;
            font-weight: 850;
            margin-bottom: 6px;
        }}

        .section-desc {{
            color: {MUTED};
            font-size: 0.93rem;
            line-height: 1.5;
        }}

        .mini-card {{
            background: {CARD_2};
            border: 1px solid {BORDER};
            border-radius: 16px;
            padding: 18px;
            height: 100%;
        }}

        .mini-title {{
            color: {TEXT};
            font-weight: 800;
            font-size: 1rem;
            margin-bottom: 8px;
        }}

        .mini-text {{
            color: {MUTED};
            font-size: 0.9rem;
            line-height: 1.45;
        }}

        .insight {{
            background: rgba(47,128,237,0.14);
            border: 1px solid rgba(86,204,242,0.32);
            border-left: 5px solid {CYAN};
            border-radius: 16px;
            padding: 16px 18px;
            margin-top: 16px;
            color: {TEXT};
            line-height: 1.55;
        }}

        .warning {{
            background: rgba(255,193,7,0.12);
            border: 1px solid rgba(255,193,7,0.35);
            border-left: 5px solid #FFC107;
            border-radius: 16px;
            padding: 16px 18px;
            margin-top: 16px;
            color: {TEXT};
            line-height: 1.55;
        }}

        h1, h2, h3, h4, h5, h6 {{
            color: {TEXT} !important;
        }}

        div[data-testid="stDataFrame"] {{
            border: 1px solid {BORDER};
            border-radius: 14px;
            overflow: hidden;
        }}

        .stDownloadButton > button {{
            background-color: {BLUE};
            color: white;
            border: none;
            border-radius: 12px;
            padding: 0.65rem 1rem;
            font-weight: 800;
        }}

        .stDownloadButton > button:hover {{
            background-color: #1B5FC7;
            color: white;
            border: none;
        }}

        .stTextInput input {{
            background-color: {CARD_2};
            color: {TEXT};
            border: 1px solid {BORDER};
            border-radius: 12px;
        }}

        .stSelectbox div {{
            color: {TEXT};
        }}

        div[role="radiogroup"] label {{
            padding: 8px 4px;
            border-radius: 10px;
        }}
    </style>
    """,
    unsafe_allow_html=True
)


# =========================================================
# FUNÇÕES DE LIMPEZA E NORMALIZAÇÃO
# =========================================================

def remover_acentos(texto):
    texto = str(texto)
    texto = unicodedata.normalize("NFKD", texto)
    return "".join([c for c in texto if not unicodedata.combining(c)])


def limpar_nome_coluna(coluna):
    coluna = remover_acentos(coluna)
    coluna = coluna.lower()
    coluna = re.sub(r"[^a-z0-9]", "", coluna)
    return coluna


def encontrar_coluna(df, possibilidades):
    colunas_normalizadas = {
        limpar_nome_coluna(col): col
        for col in df.columns
    }

    possibilidades_normalizadas = [
        limpar_nome_coluna(p)
        for p in possibilidades
    ]

    for possibilidade in possibilidades_normalizadas:
        for col_normalizada, col_original in colunas_normalizadas.items():
            if possibilidade in col_normalizada:
                return col_original

    return None


def limpar_texto_serie(serie):
    return (
        serie.fillna("Não informado")
        .astype(str)
        .str.strip()
        .replace(["", "nan", "None", "NaN", "null"], "Não informado")
    )


def tratar_volume(serie):
    def converter(valor):
        if pd.isna(valor):
            return pd.NA

        if isinstance(valor, (int, float)):
            return valor

        texto = str(valor)
        texto = texto.replace("R$", "")
        texto = texto.replace(" ", "")

        if texto in ["", "nan", "None", "Não informado"]:
            return pd.NA

        texto = texto.replace(".", "")
        texto = texto.replace(",", ".")
        texto = re.sub(r"[^0-9.]", "", texto)

        try:
            return float(texto)
        except Exception:
            return pd.NA

    return pd.to_numeric(serie.apply(converter), errors="coerce")


def carregar_dados():
    try:
        return pd.read_csv("data/ofertas_cvm.csv")
    except FileNotFoundError:
        st.error("Arquivo `data/ofertas_cvm.csv` não encontrado. Rode primeiro `python coletar_dados.py`.")
        st.stop()


def normalizar_dados(df):
    col_id = encontrar_coluna(df, ["idRequerimento", "id"])
    col_emissor = encontrar_coluna(df, ["emissor", "nomeEmissor", "ofertante", "companhia"])
    col_coord = encontrar_coluna(df, ["coordenadorLider", "coordenador", "lider", "instituicaoIntermediaria"])
    col_tipo = encontrar_coluna(df, ["valorMobiliario", "tipoValor", "tipoAtivo", "produto", "modalidade"])
    col_status = encontrar_coluna(df, ["status", "situacao", "situacaoOferta"])
    col_volume = encontrar_coluna(df, ["valorTotalOferta", "valorTotal", "volume", "montante"])
    col_data = encontrar_coluna(df, ["data", "dataRegistro", "dataInicio", "dataCriacao", "dt"])

    novo = pd.DataFrame()

    novo["ID"] = limpar_texto_serie(df[col_id]) if col_id else "Não informado"
    novo["Emissor"] = limpar_texto_serie(df[col_emissor]) if col_emissor else "Não informado"
    novo["Coordenador Líder"] = limpar_texto_serie(df[col_coord]) if col_coord else "Não informado"
    novo["Tipo de Ativo"] = limpar_texto_serie(df[col_tipo]) if col_tipo else "Não informado"
    novo["Status"] = limpar_texto_serie(df[col_status]) if col_status else "Não informado"
    novo["Volume"] = limpar_texto_serie(df[col_volume]) if col_volume else "Não informado"
    novo["Data"] = limpar_texto_serie(df[col_data]) if col_data else "Não informado"

    if col_volume:
        novo["Volume Numérico"] = tratar_volume(df[col_volume])
    else:
        novo["Volume Numérico"] = pd.NA

    return novo


# =========================================================
# FUNÇÕES DE FILTRO E ANÁLISE
# =========================================================

def opcoes_filtro(serie):
    valores = (
        serie.dropna()
        .astype(str)
        .str.strip()
    )

    valores = valores[
        ~valores.isin(["", "nan", "None", "Não informado"])
    ]

    return ["Todos"] + sorted(valores.unique().tolist())


def aplicar_filtros(df, tipo, status, coordenador, busca):
    filtrado = df.copy()

    if tipo != "Todos":
        filtrado = filtrado[filtrado["Tipo de Ativo"] == tipo]

    if status != "Todos":
        filtrado = filtrado[filtrado["Status"] == status]

    if coordenador != "Todos":
        filtrado = filtrado[filtrado["Coordenador Líder"] == coordenador]

    if busca:
        texto_busca = busca.lower().strip()
        texto_linha = filtrado.fillna("").astype(str).apply(
            lambda linha: " ".join(linha.values),
            axis=1
        ).str.lower()
        filtrado = filtrado[texto_linha.str.contains(texto_busca, na=False)]

    return filtrado


def formatar_dinheiro(valor):
    if pd.isna(valor) or valor == 0:
        return "N/D"

    if valor >= 1_000_000_000:
        return f"R$ {valor / 1_000_000_000:.2f} bi"

    if valor >= 1_000_000:
        return f"R$ {valor / 1_000_000:.2f} mi"

    return f"R$ {valor:,.2f}"


def detectar_btg(df):
    if df.empty:
        return df

    texto = df.fillna("").astype(str).apply(
        lambda linha: " ".join(linha.values),
        axis=1
    ).str.upper()

    return df[texto.str.contains("BTG", na=False, regex=False)]


def card_metrica(label, valor, ajuda):
    st.markdown(
        f"""
        <div class="metric-card">
            <div class="metric-label">{label}</div>
            <div class="metric-value">{valor}</div>
            <div class="metric-help">{ajuda}</div>
        </div>
        """,
        unsafe_allow_html=True
    )


def card_explicativo(titulo, texto):
    st.markdown(
        f"""
        <div class="mini-card">
            <div class="mini-title">{titulo}</div>
            <div class="mini-text">{texto}</div>
        </div>
        """,
        unsafe_allow_html=True
    )


def grafico_barra_horizontal(df_plot, x, y, titulo, altura=420):
    fig = px.bar(
        df_plot,
        x=x,
        y=y,
        orientation="h",
        text=x,
        color_discrete_sequence=[BLUE]
    )

    fig.update_traces(
        textposition="outside",
        marker_line_width=0,
        cliponaxis=False
    )

    fig.update_layout(
        title=titulo,
        height=altura,
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(color=TEXT, size=14),
        title_font=dict(color=TEXT, size=18),
        xaxis=dict(
            title="Quantidade",
            gridcolor="rgba(255,255,255,0.08)",
            zerolinecolor="rgba(255,255,255,0.15)"
        ),
        yaxis=dict(
            title="",
            autorange="reversed"
        ),
        margin=dict(l=20, r=60, t=55, b=30)
    )

    return fig

def identificar_mencao_btg(df):
    if df.empty:
        return pd.Series([], index=df.index, dtype=bool)

    texto = df.fillna("").astype(str).apply(
        lambda linha: " ".join(linha.values),
        axis=1
    ).str.upper()

    return texto.str.contains("BTG", na=False, regex=False)


def calcular_score_comparacao(df):
    """
    Cria uma pontuação simples para comparar ofertas.

    O score não define a 'melhor oferta' de forma absoluta.
    Ele cria um ranking inicial com base nos dados disponíveis no MVP.
    """
    base = df.copy()

    volume = pd.to_numeric(base["Volume Numérico"], errors="coerce")

    if volume.notna().sum() > 0 and volume.max() != volume.min():
        base["Score Volume"] = ((volume - volume.min()) / (volume.max() - volume.min())) * 40
    elif volume.notna().sum() > 0:
        base["Score Volume"] = 40
    else:
        base["Score Volume"] = 0

    status_texto = base["Status"].astype(str).str.upper()

    base["Score Status"] = 0
    base.loc[status_texto.str.contains("REGISTRADA|ATIVA|EM ANDAMENTO|ANÁLISE|ANALISE", na=False), "Score Status"] = 25
    base.loc[status_texto.str.contains("ENCERRADA|CONCLUÍDA|CONCLUIDA", na=False), "Score Status"] = 15
    base.loc[status_texto.str.contains("CANCELADA|INDEFERIDA", na=False), "Score Status"] = 0

    base["Menção BTG"] = identificar_mencao_btg(base)
    base["Score BTG"] = base["Menção BTG"].apply(lambda x: 15 if x else 0)

    base["Score Dados"] = 0
    base.loc[base["Emissor"].ne("Não informado"), "Score Dados"] += 5
    base.loc[base["Coordenador Líder"].ne("Não informado"), "Score Dados"] += 5
    base.loc[base["Tipo de Ativo"].ne("Não informado"), "Score Dados"] += 5
    base.loc[base["Volume"].ne("Não informado"), "Score Dados"] += 5

    base["Score Comparativo"] = (
        base["Score Volume"].fillna(0)
        + base["Score Status"].fillna(0)
        + base["Score BTG"].fillna(0)
        + base["Score Dados"].fillna(0)
    )

    base["Score Comparativo"] = base["Score Comparativo"].round(1)

    return base.sort_values("Score Comparativo", ascending=False)

def gerar_relatorio(df_filtrado):
    total = len(df_filtrado)
    volume_total = pd.to_numeric(df_filtrado["Volume Numérico"], errors="coerce").sum()
    ofertas_btg = detectar_btg(df_filtrado)

    principal_tipo = (
        df_filtrado["Tipo de Ativo"].value_counts().idxmax()
        if not df_filtrado.empty
        else "não identificado"
    )

    principal_coord = (
        df_filtrado["Coordenador Líder"].value_counts().idxmax()
        if not df_filtrado.empty
        else "não identificado"
    )

    return f"""
## Relatório Analítico

A base filtrada contém **{total} ofertas públicas** coletadas no portal SRE da CVM.

O volume financeiro identificado na amostra é de aproximadamente **{formatar_dinheiro(volume_total)}**.

O tipo de ativo mais recorrente é **{principal_tipo}**.

O coordenador líder com maior presença é **{principal_coord}**.

### Destaques da base

- **{len(ofertas_btg)} registro(s)** possuem menção ao BTG.
- A análise considera ofertas públicas disponíveis na CVM.
- Os dados podem ser filtrados por tipo de ativo, status, coordenador líder e busca textual.

### Observações

- Nem todos os registros possuem volume, taxa final ou informações operacionais padronizadas.
- A base reflete informações públicas disponíveis no período coletado.
- A análise pode ser expandida com documentos da oferta, indicadores ANBIMA, Banco Central e dados proprietários.

### Próximas evoluções

- Extração automática de prospectos e documentos PDF.
- Identificação de taxa final, bookbuilding, demanda e alocação.
- Comparação histórica por emissor, coordenador e tipo de ativo.
- Alertas para novas ofertas relevantes.
"""


# =========================================================
# CARREGAMENTO DA BASE
# =========================================================

df_original = carregar_dados()
df = normalizar_dados(df_original)


# =========================================================
# SIDEBAR
# =========================================================

st.sidebar.markdown("## BTG Pactual")
st.sidebar.markdown("### Ofertas Primárias")
st.sidebar.markdown("---")

pagina = st.sidebar.radio(
    "Navegação",
    [
        "1. Panorama",
        "2. Instituições",
        "3. Base de ofertas",
        "4. Comparação de ofertas",
        "5. Relatório"
    ]
)

st.sidebar.markdown("---")
st.sidebar.markdown("### Filtros")

tipo_filtro = st.sidebar.selectbox(
    "Tipo de ativo",
    opcoes_filtro(df["Tipo de Ativo"])
)

status_filtro = st.sidebar.selectbox(
    "Status",
    opcoes_filtro(df["Status"])
)

coordenador_filtro = st.sidebar.selectbox(
    "Coordenador líder",
    opcoes_filtro(df["Coordenador Líder"])
)

busca_global = st.sidebar.text_input(
    "Busca textual",
    placeholder="Ex: BTG, FII, emissor..."
)


df_filtrado = aplicar_filtros(
    df=df,
    tipo=tipo_filtro,
    status=status_filtro,
    coordenador=coordenador_filtro,
    busca=busca_global
)


# =========================================================
# CABEÇALHO
# =========================================================

st.markdown(
    """
    <div class="hero">
        <div class="eyebrow">BTG Pactual • Market Intelligence</div>
        <div class="title">Ofertas Primárias</div>
        <div class="subtitle">
            Monitoramento de ofertas públicas, instituições coordenadoras, emissores, volumes e status regulatório.
        </div>
    </div>
    """,
    unsafe_allow_html=True
)


# =========================================================
# MÉTRICAS
# =========================================================

total_ofertas = len(df_filtrado)
volume_total = pd.to_numeric(df_filtrado["Volume Numérico"], errors="coerce").sum()
qtd_tipos = df_filtrado["Tipo de Ativo"].nunique()
qtd_coordenadores = df_filtrado["Coordenador Líder"].nunique()
ofertas_btg = detectar_btg(df_filtrado)

c1, c2, c3, c4 = st.columns(4)

with c1:
    card_metrica(
        "Ofertas analisadas",
        total_ofertas,
        "Registros após aplicação dos filtros"
    )

with c2:
    card_metrica(
        "Volume identificado",
        formatar_dinheiro(volume_total),
        "Soma dos volumes disponíveis"
    )

with c3:
    card_metrica(
        "Tipos de ativos",
        qtd_tipos,
        "Categorias presentes na base"
    )

with c4:
    card_metrica(
        "Menções ao BTG",
        len(ofertas_btg),
        "Registros com referência ao banco"
    )


st.markdown("<br>", unsafe_allow_html=True)


# =========================================================
# PÁGINA 1: PANORAMA
# =========================================================

if pagina == "1. Panorama":
    st.markdown(
        """
        <div class="section-card">
            <div class="section-title">Panorama da base</div>
            <div class="section-desc">
                Visão consolidada das ofertas coletadas, com distribuição por tipo de ativo e status.
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    a, b, c = st.columns(3)

    with a:
        card_explicativo(
            "Base CVM SRE",
            "Ofertas públicas registradas no período analisado."
        )

    with b:
        card_explicativo(
            "Instituições",
            "Leitura por coordenador líder e menções institucionais."
        )

    with c:
        card_explicativo(
            "Relatório",
            "Síntese automática com os principais recortes da base filtrada."
        )

    st.markdown("<br>", unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    with col1:
        base_tipo = (
            df_filtrado["Tipo de Ativo"]
            .value_counts()
            .head(8)
            .reset_index()
        )
        base_tipo.columns = ["Tipo de Ativo", "Quantidade"]

        if not base_tipo.empty:
            fig_tipo = grafico_barra_horizontal(
                base_tipo,
                x="Quantidade",
                y="Tipo de Ativo",
                titulo="Principais tipos de ativos"
            )
            st.plotly_chart(fig_tipo, use_container_width=True)
        else:
            st.info("Não há dados para exibir com os filtros atuais.")

    with col2:
        base_status = (
            df_filtrado["Status"]
            .value_counts()
            .head(8)
            .reset_index()
        )
        base_status.columns = ["Status", "Quantidade"]

        if not base_status.empty:
            fig_status = grafico_barra_horizontal(
                base_status,
                x="Quantidade",
                y="Status",
                titulo="Status das ofertas"
            )
            st.plotly_chart(fig_status, use_container_width=True)
        else:
            st.info("Não há dados para exibir com os filtros atuais.")

    st.markdown(
        """
        <div class="insight">
            <strong>Nota analítica:</strong> os filtros laterais atualizam automaticamente os indicadores, gráficos e relatório.
            Isso permite alternar rapidamente entre tipos de ativo, status e instituições.
        </div>
        """,
        unsafe_allow_html=True
    )


# =========================================================
# PÁGINA 2: INSTITUIÇÕES
# =========================================================

elif pagina == "2. Instituições":
    st.markdown(
        """
        <div class="section-card">
            <div class="section-title">Instituições coordenadoras</div>
            <div class="section-desc">
                Ranking de coordenadores líderes com maior presença na base filtrada.
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    base_coord = (
        df_filtrado["Coordenador Líder"]
        .value_counts()
        .head(12)
        .reset_index()
    )
    base_coord.columns = ["Coordenador Líder", "Quantidade"]

    if not base_coord.empty:
        fig_coord = grafico_barra_horizontal(
            base_coord,
            x="Quantidade",
            y="Coordenador Líder",
            titulo="Top coordenadores líderes",
            altura=560
        )
        st.plotly_chart(fig_coord, use_container_width=True)
    else:
        st.info("Nenhum coordenador encontrado com os filtros atuais.")

    st.markdown(
        f"""
        <div class="insight">
            <strong>BTG na base filtrada:</strong> <strong>{len(ofertas_btg)}</strong> registro(s) com menção ao BTG.
        </div>
        """,
        unsafe_allow_html=True
    )

    st.subheader("Registros com menção ao BTG")

    if ofertas_btg.empty:
        st.info("Nenhum registro com menção ao BTG nos filtros atuais.")
    else:
        st.dataframe(
            ofertas_btg[
                ["ID", "Emissor", "Coordenador Líder", "Tipo de Ativo", "Status", "Volume", "Data"]
            ],
            use_container_width=True,
            height=320
        )


# =========================================================
# PÁGINA 3: BASE DE OFERTAS
# =========================================================

elif pagina == "3. Base de ofertas":
    st.markdown(
        """
        <div class="section-card">
            <div class="section-title">Base de ofertas</div>
            <div class="section-desc">
                Consulta detalhada dos registros coletados e normalizados.
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.dataframe(
        df_filtrado[
            ["ID", "Emissor", "Coordenador Líder", "Tipo de Ativo", "Status", "Volume", "Data"]
        ],
        use_container_width=True,
        height=560
    )

    csv = df_filtrado.to_csv(index=False, encoding="utf-8-sig")

    st.download_button(
        label="Baixar CSV filtrado",
        data=csv,
        file_name="ofertas_primarias_filtradas.csv",
        mime="text/csv"
    )


# =========================================================
# PÁGINA 4: COMPARAÇÃO DE OFERTAS
# =========================================================

elif pagina == "4. Comparação de ofertas":
    st.markdown(
        """
        <div class="section-card">
            <div class="section-title">Comparador de ofertas</div>
            <div class="section-desc">
                Ranking comparativo das ofertas filtradas com base em volume, status, dados disponíveis e menção institucional.
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    if df_filtrado.empty:
        st.info("Nenhuma oferta disponível com os filtros atuais.")
    else:
        st.markdown("### Critérios de comparação")

        col_a, col_b, col_c = st.columns(3)

        with col_a:
            criterio_principal = st.selectbox(
                "Critério principal",
                [
                    "Score comparativo",
                    "Maior volume",
                    "Menção ao BTG",
                    "Coordenador líder"
                ]
            )

        with col_b:
            quantidade_ranking = st.slider(
                "Quantidade de ofertas no ranking",
                min_value=3,
                max_value=20,
                value=10
            )

        with col_c:
            apenas_mesmo_tipo = st.checkbox(
                "Comparar apenas mesmo tipo de ativo",
                value=False
            )

        base_comparacao = df_filtrado.copy()

        if apenas_mesmo_tipo:
            tipos_disponiveis = sorted(base_comparacao["Tipo de Ativo"].dropna().unique())

            tipo_comparado = st.selectbox(
                "Tipo de ativo para comparação",
                tipos_disponiveis
            )

            base_comparacao = base_comparacao[
                base_comparacao["Tipo de Ativo"] == tipo_comparado
            ]

        base_rankeada = calcular_score_comparacao(base_comparacao)

        if criterio_principal == "Maior volume":
            base_rankeada = base_rankeada.sort_values(
                "Volume Numérico",
                ascending=False
            )

        elif criterio_principal == "Menção ao BTG":
            base_rankeada = base_rankeada.sort_values(
                ["Menção BTG", "Score Comparativo"],
                ascending=[False, False]
            )

        elif criterio_principal == "Coordenador líder":
            base_rankeada = base_rankeada.sort_values(
                ["Coordenador Líder", "Score Comparativo"],
                ascending=[True, False]
            )

        else:
            base_rankeada = base_rankeada.sort_values(
                "Score Comparativo",
                ascending=False
            )

        ranking = base_rankeada.head(quantidade_ranking)

        st.markdown("### Ranking de ofertas")

        st.dataframe(
            ranking[
                [
                    "Score Comparativo",
                    "Emissor",
                    "Tipo de Ativo",
                    "Coordenador Líder",
                    "Status",
                    "Volume",
                    "Data",
                    "Menção BTG"
                ]
            ],
            use_container_width=True,
            height=420
        )

        st.markdown("### Comparação visual")

        grafico_ranking = ranking.copy()

        grafico_ranking["Oferta"] = (
            grafico_ranking["Emissor"].astype(str).str.slice(0, 45)
            + " | "
            + grafico_ranking["Tipo de Ativo"].astype(str).str.slice(0, 25)
        )

        fig_comparador = px.bar(
            grafico_ranking.sort_values("Score Comparativo", ascending=True),
            x="Score Comparativo",
            y="Oferta",
            orientation="h",
            text="Score Comparativo",
            color_discrete_sequence=[BLUE]
        )

        fig_comparador.update_traces(
            textposition="outside",
            marker_line_width=0,
            cliponaxis=False
        )

        fig_comparador.update_layout(
            height=520,
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            font=dict(color=TEXT, size=14),
            title_font=dict(color=TEXT, size=18),
            xaxis=dict(
                title="Score comparativo",
                gridcolor="rgba(255,255,255,0.08)",
                zerolinecolor="rgba(255,255,255,0.15)"
            ),
            yaxis=dict(title=""),
            margin=dict(l=20, r=70, t=40, b=30)
        )

        st.plotly_chart(fig_comparador, use_container_width=True)

        melhor_oferta = ranking.iloc[0]

        st.markdown(
            f"""
            <div class="insight">
                <strong>Oferta melhor posicionada no recorte atual:</strong><br>
                <strong>{melhor_oferta["Emissor"]}</strong><br>
                Tipo de ativo: <strong>{melhor_oferta["Tipo de Ativo"]}</strong><br>
                Coordenador líder: <strong>{melhor_oferta["Coordenador Líder"]}</strong><br>
                Status: <strong>{melhor_oferta["Status"]}</strong><br>
                Volume: <strong>{melhor_oferta["Volume"]}</strong><br>
                Score comparativo: <strong>{melhor_oferta["Score Comparativo"]}</strong>
            </div>
            """,
            unsafe_allow_html=True
        )

        st.markdown(
            """
            <div class="warning">
                <strong>Nota:</strong> o score é um ranking inicial baseado nos campos disponíveis no MVP.
                Para uma recomendação financeira mais precisa, a próxima etapa deve incluir taxa final,
                demanda, bookbuilding, prazo, risco, indexador e histórico de rentabilidade.
            </div>
            """,
            unsafe_allow_html=True
        )

# =========================================================
# PÁGINA 5: RELATÓRIO
# =========================================================

elif pagina == "5. Relatório":
    st.markdown(
        """
        <div class="section-card">
            <div class="section-title">Relatório analítico</div>
            <div class="section-desc">
                Síntese gerada a partir dos filtros aplicados no dashboard.
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    relatorio = gerar_relatorio(df_filtrado)

    st.markdown(relatorio)

    st.download_button(
        label="Baixar relatório",
        data=relatorio,
        file_name="relatorio_agente_ofertas.md",
        mime="text/markdown"
    )

    st.markdown(
        """
        <div class="warning">
            <strong>Escopo:</strong> base construída a partir de dados públicos da CVM SRE.
            Fontes privadas ou proprietárias podem ser integradas em uma etapa posterior.
        </div>
        """,
        unsafe_allow_html=True
    )