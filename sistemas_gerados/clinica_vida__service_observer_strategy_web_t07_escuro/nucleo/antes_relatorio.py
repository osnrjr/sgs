"""ANTES — a "view" que faz tudo: regra de negócio + apresentação no mesmo laço."""


def relatorio_view(registros, request=None):
    linhas = []
    total_geral = 0
    for r in registros:
        base = r["quantidade"] * r["preco"]
        # ↓ regra de negócio presa na view
        if r["tipo"] == "convenio_ouro":
            total = base * 0.6
        elif r["tipo"] == "convenio_prata":
            total = base * 0.75
        else:
            total = base
        total_geral += total
        linhas.append(f"{r['nome']}: R$ {total:.2f}")  # ← apresentação
    corpo = "\n".join(linhas)
    return f"RELATORIO - Clínica Vida\n{corpo}\nTOTAL: R$ {total_geral:.2f}"
