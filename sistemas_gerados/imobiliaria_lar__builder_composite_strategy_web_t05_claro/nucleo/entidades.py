"""
Imobiliária Lar — entidade principal `Contrato` (ENCAPSULAMENTO com @property).

Gerado por gerar_sistema.py (determinístico, sem IA). Regras dos atributos:
  - locatario: texto obrigatório (não pode ser vazio)
  - imovel: inteiro maior ou igual a 1
  - meses: inteiro entre 1 e 36
  - valor_aluguel: número maior ou igual a 0
  - descricao_completa: texto longo obrigatório (descrição/memo)
  - foto_capa: caminho ou URL de imagem (.png, .jpg, .jpeg, .webp, .gif, .svg)
  - observacao: texto livre, sem regra (atributo simples — proteger seria cerimônia)

Ideias das Aulas 02 e 03:
  * o objeto controla o acesso ao próprio estado (encapsulamento);
  * @property + setter = a "fechadura": valida ANTES de gravar no atributo interno (_nome);
  * no __init__, `self.x = x` passa pelo setter → o objeto já nasce válido;
  * `total` é property CALCULADA (sem setter): nunca fica desatualizada;
  * atributo sem regra fica simples — @property sem problema que a justifique é cerimônia;
  * no model Django a mesma regra vai em validators (setter em campo quebra form/admin/ORM).
"""
import re


class Contrato:
    """Contrato do sistema Imobiliária Lar: total = meses × valor_aluguel."""

    def __init__(self, locatario, imovel, meses, valor_aluguel, descricao_completa, foto_capa, observacao=""):
        self.locatario = locatario  # passa pelo setter → validado já na criação
        self.imovel = imovel  # passa pelo setter → validado já na criação
        self.meses = meses  # passa pelo setter → validado já na criação
        self.valor_aluguel = valor_aluguel  # passa pelo setter → validado já na criação
        self.descricao_completa = descricao_completa  # passa pelo setter → validado já na criação
        self.foto_capa = foto_capa  # passa pelo setter → validado já na criação
        self.observacao = observacao  # sem regra → atributo simples (antifachada)

    @property
    def locatario(self):
        """Getter: lê `locatario` (o valor de verdade fica no atributo interno `_locatario`)."""
        return self._locatario

    @locatario.setter
    def locatario(self, valor):
        """Setter (a "fechadura"): só grava se a regra for respeitada — locatario: texto obrigatório (não pode ser vazio)."""
        if not isinstance(valor, str) or not valor.strip():
            raise ValueError("locatario é obrigatório (texto não vazio)")
        valor = valor.strip()  # guarda sem espaços nas pontas
        self._locatario = valor

    @property
    def imovel(self):
        """Getter: lê `imovel` (o valor de verdade fica no atributo interno `_imovel`)."""
        return self._imovel

    @imovel.setter
    def imovel(self, valor):
        """Setter (a "fechadura"): só grava se a regra for respeitada — imovel: inteiro maior ou igual a 1."""
        # bool é subclasse de int em Python (True == 1): por isso é recusado explicitamente.
        if isinstance(valor, bool) or not isinstance(valor, int):
            raise ValueError("imovel deve ser um número inteiro")
        if valor < 1:
            raise ValueError("imovel deve ser no mínimo 1")
        self._imovel = valor

    @property
    def meses(self):
        """Getter: lê `meses` (o valor de verdade fica no atributo interno `_meses`)."""
        return self._meses

    @meses.setter
    def meses(self, valor):
        """Setter (a "fechadura"): só grava se a regra for respeitada — meses: inteiro entre 1 e 36."""
        # bool é subclasse de int em Python (True == 1): por isso é recusado explicitamente.
        if isinstance(valor, bool) or not isinstance(valor, int):
            raise ValueError("meses deve ser um número inteiro")
        if not 1 <= valor <= 36:
            raise ValueError("meses deve estar entre 1 e 36")
        self._meses = valor

    @property
    def valor_aluguel(self):
        """Getter: lê `valor_aluguel` (o valor de verdade fica no atributo interno `_valor_aluguel`)."""
        return self._valor_aluguel

    @valor_aluguel.setter
    def valor_aluguel(self, valor):
        """Setter (a "fechadura"): só grava se a regra for respeitada — valor_aluguel: número maior ou igual a 0."""
        if isinstance(valor, bool) or not isinstance(valor, (int, float)):
            raise ValueError("valor_aluguel deve ser um número")
        if valor < 0:
            raise ValueError("valor_aluguel deve ser no mínimo 0")
        self._valor_aluguel = valor

    @property
    def descricao_completa(self):
        """Getter: lê `descricao_completa` (o valor de verdade fica no atributo interno `_descricao_completa`)."""
        return self._descricao_completa

    @descricao_completa.setter
    def descricao_completa(self, valor):
        """Setter (a "fechadura"): só grava se a regra for respeitada — descricao_completa: texto longo obrigatório (descrição/memo)."""
        if not isinstance(valor, str) or not valor.strip():
            raise ValueError("descricao_completa é obrigatório (texto não vazio)")
        valor = valor.strip()  # guarda sem espaços nas pontas
        self._descricao_completa = valor

    @property
    def foto_capa(self):
        """Getter: lê `foto_capa` (o valor de verdade fica no atributo interno `_foto_capa`)."""
        return self._foto_capa

    @foto_capa.setter
    def foto_capa(self, valor):
        """Setter (a "fechadura"): só grava se a regra for respeitada — foto_capa: caminho ou URL de imagem (.png, .jpg, .jpeg, .webp, .gif, .svg)."""
        if not isinstance(valor, str) or not valor.strip():
            raise ValueError("foto_capa é obrigatório (texto não vazio)")
        valor = valor.strip()  # guarda sem espaços nas pontas
        if not re.fullmatch(r"(?:https?://[^\s]+|[\w./-]+)\.(?:png|jpe?g|webp|gif|svg)", valor, re.IGNORECASE):
            raise ValueError("foto_capa deve ser um caminho ou URL de imagem (.png, .jpg, .webp, .gif, .svg)")
        self._foto_capa = valor

    @property
    def total(self):
        """Valor total = meses × valor_aluguel (2 casas).

        Property CALCULADA e SÓ LEITURA: sem setter, `obj.total = 1` levanta AttributeError.
        Calculada na hora, acompanha qualquer mudança em meses ou valor_aluguel.
        """
        return round(self.meses * self.valor_aluguel, 2)

    def __repr__(self):
        return f"Contrato(locatario={self.locatario!r}, total={self.total})"
