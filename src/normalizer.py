import pandas as pd


def encontrar_coluna(df: pd.DataFrame, possibilidades: list[str]) -> str | None:
    """
    Procura uma coluna mesmo que o nome venha diferente da API.
    """
    colunas_lower = {col.lower(): col for col in df.columns}

    for possibilidade in possibilidades:
        for col_lower, col_original in colunas_lower.items():
            if possibilidade.lower() in col_lower:
                return col_original

    return None


def normalizar_ofertas(path: str = "data/ofertas_cvm.csv") -> pd.DataFrame:
    df = pd.read_csv(path)

    mapa = {
        "id": ["idRequerimento", "id"],
        "emissor": ["emissor", "nomeEmissor", "companhia"],
        "coordenador_lider": ["coordenador", "lider", "coordenadorLider"],
        "tipo_ativo": ["valorMobiliario", "tipo", "produto"],
        "status": ["status", "situacao"],
        "volume": ["volume", "valorTotal", "montante"],
        "data": ["data", "dataRegistro", "dataInicio"],
    }

    saida = pd.DataFrame()

    for nome_final, possibilidades in mapa.items():
        coluna = encontrar_coluna(df, possibilidades)
        saida[nome_final] = df[coluna] if coluna else None

    if "volume" in saida.columns:
        saida["volume_num"] = (
            saida["volume"]
            .astype(str)
            .str.replace("R$", "", regex=False)
            .str.replace(".", "", regex=False)
            .str.replace(",", ".", regex=False)
        )

        saida["volume_num"] = pd.to_numeric(saida["volume_num"], errors="coerce")

    return saida