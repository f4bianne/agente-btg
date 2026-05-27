import os
import json
import pandas as pd

from src.cvm_client import (
    pesquisar_ofertas,
    buscar_requerimento,
    buscar_participantes,
    buscar_info_oferta,
)


# =========================================================
# CONFIGURAÇÃO DA BUSCA
# =========================================================

# Este payload busca ofertas regulares criadas entre 01/01/2020 e 25/05/2026.
# Você pode mudar as datas conforme quiser.
PAYLOAD_BUSCA = {
    "periodoCriacaoProcesso": {
        "de": "01/01/2026",
        "ate": "25/05/2026"
    },
    "opa": False,
    "colunaOrdenacao": "data",
    "direcaoOrdenacao": "DESC",
    "modalidade": "TODAS",
    "pagina": 1,
    "tamanhoPagina": "10",
    "tipoOferta": "OFERTA_REGULAR"
}


# =========================================================
# FUNÇÕES AUXILIARES
# =========================================================

def salvar_json(objeto, caminho):
    """
    Salva objetos complexos em JSON.
    O JSON preserva melhor dados aninhados do que CSV.
    """
    with open(caminho, "w", encoding="utf-8") as arquivo:
        json.dump(objeto, arquivo, ensure_ascii=False, indent=2)


def coletar_todas_as_paginas(payload_base, limite_paginas=3):
    """
    Coleta várias páginas da busca da CVM.

    Exemplo:
    tamanhoPagina = 10
    limite_paginas = 3

    Total máximo aproximado:
    10 x 3 = 30 registros
    """
    todas_ofertas = []

    for pagina in range(1, limite_paginas + 1):
        payload = payload_base.copy()
        payload["periodoCriacaoProcesso"] = payload_base["periodoCriacaoProcesso"].copy()
        payload["pagina"] = pagina

        print(f"Buscando página {pagina}...")

        try:
            ofertas_pagina = pesquisar_ofertas(payload)
        except Exception as erro:
            print(f"Erro ao buscar página {pagina}: {erro}")
            break

        if not ofertas_pagina:
            print("Nenhuma oferta retornada nessa página. Encerrando coleta.")
            break

        print(f"{len(ofertas_pagina)} ofertas encontradas na página {pagina}.")
        todas_ofertas.extend(ofertas_pagina)

    return todas_ofertas


def obter_id_requerimento(oferta):
    """
    Tenta encontrar o idRequerimento mesmo se o nome do campo vier com pequena variação.
    """
    possibilidades = [
        "idRequerimento",
        "id_requerimento",
        "id",
        "codigoRequerimento"
    ]

    for campo in possibilidades:
        if campo in oferta and oferta[campo]:
            return oferta[campo]

    return None


# =========================================================
# FUNÇÃO PRINCIPAL
# =========================================================

def main():
    os.makedirs("data", exist_ok=True)

    print("Iniciando coleta de ofertas públicas na CVM...")
    print(
        f"Período: {PAYLOAD_BUSCA['periodoCriacaoProcesso']['de']} "
        f"até {PAYLOAD_BUSCA['periodoCriacaoProcesso']['ate']}"
    )

    ofertas = coletar_todas_as_paginas(
        PAYLOAD_BUSCA,
        limite_paginas=3
    )

    if not ofertas:
        print("Nenhuma oferta foi retornada.")
        print("Verifique o payload ou copie novamente a requisição pelo DevTools.")
        return

    print(f"Total de ofertas coletadas: {len(ofertas)}")

    # Remove duplicatas, caso alguma página repita registros
    df_ofertas = pd.DataFrame(ofertas)

    if "idRequerimento" in df_ofertas.columns:
        df_ofertas = df_ofertas.drop_duplicates(subset=["idRequerimento"])
    else:
        df_ofertas = df_ofertas.drop_duplicates()

    print(f"Total após remoção de duplicatas: {len(df_ofertas)}")

    # Salva base principal
    df_ofertas.to_csv(
        "data/ofertas_cvm.csv",
        index=False,
        encoding="utf-8-sig"
    )

    salvar_json(
        df_ofertas.to_dict(orient="records"),
        "data/ofertas_cvm.json"
    )

    detalhes_completos = []

    for _, oferta in df_ofertas.iterrows():
        oferta_dict = oferta.to_dict()
        id_requerimento = obter_id_requerimento(oferta_dict)

        if not id_requerimento:
            print("Oferta sem idRequerimento. Pulando...")
            continue

        print(f"Coletando detalhes da oferta {id_requerimento}...")

        registro = {
            "idRequerimento": id_requerimento,
            "oferta_basica": oferta_dict,
            "detalhes": None,
            "participantes": None,
            "info_oferta": None,
            "erro_detalhes": None,
            "erro_participantes": None,
            "erro_info_oferta": None,
        }

        try:
            registro["detalhes"] = buscar_requerimento(id_requerimento)
        except Exception as erro:
            registro["erro_detalhes"] = str(erro)
            print(f"Erro ao buscar detalhes da oferta {id_requerimento}: {erro}")

        try:
            registro["participantes"] = buscar_participantes(id_requerimento)
        except Exception as erro:
            registro["erro_participantes"] = str(erro)
            print(f"Erro ao buscar participantes da oferta {id_requerimento}: {erro}")

        try:
            registro["info_oferta"] = buscar_info_oferta(id_requerimento)
        except Exception as erro:
            registro["erro_info_oferta"] = str(erro)
            print(f"Erro ao buscar informações operacionais da oferta {id_requerimento}: {erro}")

        detalhes_completos.append(registro)

    # Salva detalhes completos em JSON
    salvar_json(
        detalhes_completos,
        "data/detalhes_cvm.json"
    )

    # Salva versão simplificada em CSV
    df_detalhes = pd.DataFrame(detalhes_completos)
    df_detalhes.to_csv(
        "data/detalhes_cvm.csv",
        index=False,
        encoding="utf-8-sig"
    )

    print("\nColeta finalizada com sucesso.")
    print("Arquivos gerados:")
    print("- data/ofertas_cvm.csv")
    print("- data/ofertas_cvm.json")
    print("- data/detalhes_cvm.csv")
    print("- data/detalhes_cvm.json")


if __name__ == "__main__":
    main()