def unpack(diccionario: dict, *keys):
    out = []
    for k in keys:
        out.append(diccionario.get(k))
    return out
