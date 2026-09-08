import unicodedata


def quitar_acentos(texto):
    texto = unicodedata.normalize('NFD', texto)
    texto = ''.join(
        c for c in texto
        if unicodedata.category(c) != 'Mn'
    )
    return texto