import pandas as pd


def resumo_mercado(df: pd.DataFrame) -> dict:
    return {
        "total_ofertas": len(df),
        "volume_total": df["volume_num"].sum() if "volume_num" in df else None,
        "principais_tipos": df["tipo_ativo"].value_counts(dropna=True).head(5).to_dict(),
        "principais_coordenadores": df["coordenador_lider"].value_counts(dropna=True).head(10).to_dict(),
        "status": df["status"].value_counts(dropna=True).to_dict(),
    }


def detectar_discrepancias(df: pd.DataFrame) -> pd.DataFrame:
    """
    Encontra ofertas com volume muito acima da mediana do mesmo tipo de ativo.
    """
    if "volume_num" not in df.columns or "tipo_ativo" not in df.columns:
        return pd.DataFrame()

    base = df.dropna(subset=["volume_num", "tipo_ativo"]).copy()

    base["mediana_tipo"] = base.groupby("tipo_ativo")["volume_num"].transform("median")
    base["multiplo_mediana"] = base["volume_num"] / base["mediana_tipo"]

    return base.sort_values("multiplo_mediana", ascending=False).head(10)


def filtrar_btg(df: pd.DataFrame) -> pd.DataFrame:
    """
    Busca ofertas em que BTG aparece como coordenador ou participante,
    caso essa informação esteja na base.
    """
    texto = df.astype(str).agg(" ".join, axis=1).str.upper()
    return df[texto.str.contains("BTG", na=False)]