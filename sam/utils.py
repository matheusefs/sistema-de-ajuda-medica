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
    
def para_mg(valor, unidade):
    if unidade == "g":
        return valor * 1000
    elif unidade == "mg":
        return valor
    elif unidade == "mcg":
        return valor / 1000
    else:
        return valor

