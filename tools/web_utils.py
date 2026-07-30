from tavily import TavilyClient

API_KEY = "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"

client = TavilyClient(api_key=API_KEY)


def buscar_web(query):

    respuesta = client.search(
        query=query,
        search_depth="advanced",
        max_results=5
    )

    resultados = []

    for r in respuesta["results"]:

        contenido = r.get("content", "")

        resultados.append(contenido)

    return "\n".join(resultados)

