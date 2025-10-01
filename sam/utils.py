def converter_unidades(valor, origem, destino):
    #Conversão por unidades de massa:
    if origem == "g" and destino == "mg":
        return valor * 1000
    elif origem == "mg" and destino == "g":
        return valor / 1000
    elif origem == "g" and destino == "mcg":
        return valor * 1000000
    elif origem == "mcg" and destino == "mg":
        return valor / 1000000
