# utils.py

# Categorias de unidades
CATEGORIAS = {
    "g": "peso",
    "mg": "peso",
    "mcg": "peso",
    "ml": "volume",
    "l": "volume"
}

# Fatores para conversão dentro da mesma categoria
# Cada unidade é convertida para a unidade base da categoria (g para peso, ml para volume)
FATORES = {
    "peso": {
        "g": 1,
        "mg": 0.001,
        "mcg": 0.000001
    },
    "volume": {
        "ml": 1,
        "l": 1000
    }
}

def converter_unidades(valor, origem, destino):
    """
    Converte valor de origem para destino.
    Só permite conversão dentro da mesma categoria (peso ou volume).
    """
    # Verifica se as unidades existem
    if origem not in CATEGORIAS or destino not in CATEGORIAS:
        raise ValueError(f"Unidade inválida: {origem} ou {destino}")

    # Verifica se são da mesma categoria
    if CATEGORIAS[origem] != CATEGORIAS[destino]:
        raise ValueError(f"Não é possível converter essas unidades (Tipos de Unidades diferentes)")

    categoria = CATEGORIAS[origem]
    valor_base = valor * FATORES[categoria][origem]  # converte para unidade base
    resultado = valor_base / FATORES[categoria][destino]  # converte para unidade de destino
    return resultado

def para_mg(valor, unidade):
    if unidade == "g":
        return valor * 1000
    elif unidade == "mg":
        return valor
    elif unidade == "mcg":
        return valor / 1000
    else:
        return valor
