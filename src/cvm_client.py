import requests
from typing import Dict, Any, List


BASE_URL = "https://web.cvm.gov.br/sre-publico-cvm/rest"

HEADERS = {
    "User-Agent": "Mozilla/5.0",
    "Accept": "application/json, text/plain, */*",
    "Content-Type": "application/json;charset=UTF-8",
}


def pesquisar_ofertas(payload: Dict[str, Any]) -> List[Dict[str, Any]]:
    """
    Busca a lista de ofertas públicas no portal SRE da CVM.
    Usa o endpoint que você encontrou no DevTools:
    POST /rest/sitePublico/pesquisar/detalhado
    """

    url = f"{BASE_URL}/sitePublico/pesquisar/detalhado"

    response = requests.post(
        url,
        json=payload,
        headers=HEADERS,
        timeout=30
    )

    response.raise_for_status()

    data = response.json()

    # Caso a CVM retorne uma lista diretamente
    if isinstance(data, list):
        return data

    # Caso a CVM retorne um dicionário com os dados dentro
    if isinstance(data, dict):
        for chave in ["dados", "content", "resultado", "registros", "data"]:
            if chave in data and isinstance(data[chave], list):
                return data[chave]

    print("Formato inesperado retornado pela CVM:")
    print(data)

    return []


def buscar_requerimento(id_requerimento: int) -> Dict[str, Any]:
    """
    Busca os detalhes completos de uma oferta específica.
    Usa:
    GET /rest/sitePublico/pesquisar/requerimento/{id}
    """

    url = f"{BASE_URL}/sitePublico/pesquisar/requerimento/{id_requerimento}"

    response = requests.get(
        url,
        headers=HEADERS,
        timeout=30
    )

    response.raise_for_status()

    return response.json()


def buscar_participantes(id_requerimento: int) -> Dict[str, Any]:
    """
    Busca coordenadores, distribuidores e participantes da oferta.
    Usa:
    GET /rest/sitePublico/pesquisar/participantes/{id}
    """

    url = f"{BASE_URL}/sitePublico/pesquisar/participantes/{id_requerimento}"

    response = requests.get(
        url,
        headers=HEADERS,
        timeout=30
    )

    response.raise_for_status()

    return response.json()


def buscar_info_oferta(id_requerimento: int) -> Dict[str, Any]:
    """
    Busca informações operacionais da oferta, como taxa final,
    demanda, bookbuilding e alocação, quando disponíveis.
    Usa:
    GET /rest/sitePublico/pesquisar/infOferta/{id}
    """

    url = f"{BASE_URL}/sitePublico/pesquisar/infOferta/{id_requerimento}"

    response = requests.get(
        url,
        headers=HEADERS,
        timeout=30
    )

    response.raise_for_status()

    return response.json()


def baixar_pdf(uuid: str, output_path: str) -> None:
    """
    Baixa um PDF da CVM usando o UUID do documento.
    Usa:
    GET /rest/download/{uuid}
    """

    url = f"{BASE_URL}/download/{uuid}"

    response = requests.get(
        url,
        headers=HEADERS,
        timeout=60
    )

    response.raise_for_status()

    with open(output_path, "wb") as arquivo:
        arquivo.write(response.content)