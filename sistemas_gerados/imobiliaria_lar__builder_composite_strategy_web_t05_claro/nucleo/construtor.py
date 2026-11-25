"""
Imobiliária Lar — BUILDER (GoF · criação): montar a Contrato PASSO A PASSO, com nomes.

ANTES (nucleo/antes_construtor.py): nova_contrato_antiga(...) com todos os argumentos na ORDEM —
dois números trocados de lugar passam despercebidos e não há receitas prontas.
DEPOIS (aqui):
  * ContratoBuilder tem um com_<campo>() por atributo; cada um devolve o próprio builder
    (interface FLUENTE: b.com_x(...).com_y(...));
  * construir() confere o que falta e só então cria a Contrato (os setters validam cada valor);
  * DiretorDeContrato guarda "receitas" de montagem que se repetem.
Quando NÃO usar: poucos campos — em Python, argumentos NOMEADOS já resolvem a ordem.
"""
from nucleo.entidades import Contrato

OBRIGATORIOS = ['locatario', 'imovel', 'meses', 'valor_aluguel', 'descricao_completa', 'foto_capa']


class ContratoBuilder:
    """BUILDER: junta os valores aos poucos e cria a Contrato no final."""

    def __init__(self):
        self._valores = {}

    def com_locatario(self, valor):
        """Informa locatario e devolve o PRÓPRIO builder (para encadear)."""
        self._valores["locatario"] = valor
        return self


    def com_imovel(self, valor):
        """Informa imovel e devolve o PRÓPRIO builder (para encadear)."""
        self._valores["imovel"] = valor
        return self


    def com_meses(self, valor):
        """Informa meses e devolve o PRÓPRIO builder (para encadear)."""
        self._valores["meses"] = valor
        return self


    def com_valor_aluguel(self, valor):
        """Informa valor_aluguel e devolve o PRÓPRIO builder (para encadear)."""
        self._valores["valor_aluguel"] = valor
        return self


    def com_descricao_completa(self, valor):
        """Informa descricao_completa e devolve o PRÓPRIO builder (para encadear)."""
        self._valores["descricao_completa"] = valor
        return self


    def com_foto_capa(self, valor):
        """Informa foto_capa e devolve o PRÓPRIO builder (para encadear)."""
        self._valores["foto_capa"] = valor
        return self


    def com_observacao(self, valor):
        """Informa observacao e devolve o PRÓPRIO builder (para encadear)."""
        self._valores["observacao"] = valor
        return self

    def faltando(self):
        """Campos obrigatórios que ainda não foram informados."""
        return [campo for campo in OBRIGATORIOS if campo not in self._valores]

    def construir(self):
        """Cria a Contrato. Faltou campo → ValueError dizendo QUAL; valor inválido → o setter barra."""
        falta = self.faltando()
        if falta:
            raise ValueError(f"faltam campos: {', '.join(falta)}")
        return Contrato(**self._valores)


class DiretorDeContrato:
    """DIRETOR: receitas de montagem que se repetem (o passo a passo fica num lugar só)."""

    PADRAO = {'imovel': 101, 'meses': 2, 'valor_aluguel': 1800.0, 'descricao_completa': 'Descrição detalhada de descricao completa 1.', 'foto_capa': 'imagens/foto_1.png'}

    def basico(self, locatario):
        builder = ContratoBuilder().com_locatario(locatario)
        for campo, valor in self.PADRAO.items():
            getattr(builder, f"com_{campo}")(valor)
        return builder.construir()
