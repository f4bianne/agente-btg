import pandas as pd
from src.analyzer import resumo_mercado, detectar_discrepancias, filtrar_btg


def gerar_relatorio_textual(df: pd.DataFrame, df_macro: pd.DataFrame | None = None) -> str:
    resumo = resumo_mercado(df)
    discrepancias = detectar_discrepancias(df)
    btg = filtrar_btg(df)

    texto = []

    texto.append("# Relatório Analítico de Ofertas Primárias\n")

    texto.append("## Visão geral do mercado\n")
    texto.append(f"Foram identificadas {resumo['total_ofertas']} ofertas na base analisada.\n")

    if resumo["volume_total"]:
        texto.append(f"O volume financeiro total identificado foi de aproximadamente R$ {resumo['volume_total']:,.2f}.\n")

    texto.append("\n## Principais tipos de ativos\n")
    for tipo, qtd in resumo["principais_tipos"].items():
        texto.append(f"- {tipo}: {qtd} oferta(s)")

    texto.append("\n\n## Principais coordenadores líderes\n")
    for coord, qtd in resumo["principais_coordenadores"].items():
        texto.append(f"- {coord}: {qtd} oferta(s)")

    texto.append("\n\n## Presença do BTG\n")
    texto.append(
        f"Foram encontradas {len(btg)} ofertas com menção ao BTG na base analisada. "
        "Esse ponto permite comparar a atuação do BTG com outros coordenadores e identificar ofertas relevantes em que o banco participa ou não."
    )

    texto.append("\n\n## Discrepâncias de volume\n")
    if discrepancias.empty:
        texto.append("Não foram encontradas discrepâncias relevantes de volume com os dados disponíveis.")
    else:
        for _, row in discrepancias.head(5).iterrows():
            texto.append(
                f"- {row.get('emissor', 'Emissor não identificado')} possui volume "
                f"{row.get('multiplo_mediana', 0):.2f}x acima da mediana do tipo {row.get('tipo_ativo', '')}."
            )

    texto.append("\n\n## Contextualização macroeconômica\n")
    if df_macro is not None and not df_macro.empty:
        ultimo = df_macro.sort_values("data").iloc[-1]
        texto.append(
            f"A última observação macroeconômica coletada para {ultimo['indicador']} "
            f"foi {ultimo['valor']} em {ultimo['data'].date()}. "
            "Mudanças em juros, inflação e expectativas afetam diretamente a atratividade relativa de ofertas primárias, "
            "especialmente em ativos de renda fixa e fundos com sensibilidade a custo de capital."
        )
    else:
        texto.append(
            "A análise macroeconômica ainda pode ser enriquecida com séries de Selic, IPCA, Focus e índices da ANBIMA."
        )

    texto.append("\n\n## Limitações\n")
    texto.append(
        "- O endpoint da CVM SRE é público, mas não documentado oficialmente.\n"
        "- Nem todas as ofertas possuem taxa final ou informações de bookbuilding disponíveis no mesmo formato.\n"
        "- A comparação com bancos concorrentes depende da qualidade dos campos de coordenador, participantes e documentos.\n"
        "- A análise de contexto ainda é interpretativa e deve ser validada por especialistas de mercado."
    )

    return "\n".join(texto)