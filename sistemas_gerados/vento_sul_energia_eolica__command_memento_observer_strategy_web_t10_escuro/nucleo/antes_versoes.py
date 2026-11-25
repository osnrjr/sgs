"""ANTES — o smell do Memento: copiar o interior (_campos) na mão para poder voltar atrás."""


def salvar_antigo(item):
    return {"_operador": item._operador, "_torre": item._torre, "_megawatts": item._megawatts, "_preco_mwh": item._preco_mwh, "_geoloc": item._geoloc, "_parametros_json": item._parametros_json, "observacao": item.observacao}


def restaurar_antigo(item, copia):
    for campo, valor in copia.items():
        setattr(item, campo, valor)
