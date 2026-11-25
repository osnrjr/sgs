"""
Biblioteca Municipal — entidade principal `Emprestimo` (ENCAPSULAMENTO com @property).

Gerado por gerar_sistema.py (determinístico, sem IA). Regras dos atributos:
  - leitor: texto obrigatório (não pode ser vazio)
  - exemplar: inteiro maior ou igual a 1
  - dias: inteiro entre 1 e 30
  - taxa_dia: número maior ou igual a 0
  - data_devolucao: data e hora válidas no formato AAAA-MM-DDTHH:MM (ex.: 2026-01-10T09:30)
  - observacao: texto livre, sem regra (atributo simples — proteger seria cerimônia)

Ideias das Aulas 02 e 03:
  * o objeto controla o acesso ao próprio estado (encapsulamento);
  * @property + setter = a "fechadura": valida ANTES de gravar no atributo interno (_nome);
  * no __init__, `self.x = x` passa pelo setter → o objeto já nasce válido;
  * `total` é property CALCULADA (sem setter): nunca fica desatualizada;
  * atributo sem regra fica simples — @property sem problema que a justifique é cerimônia;
  * no model Django a mesma regra vai em validators (setter em campo quebra form/admin/ORM).
"""
from datetime import datetime


class Emprestimo:
    """Emprestimo do sistema Biblioteca Municipal: total = dias × taxa_dia."""

    def __init__(self, leitor, exemplar, dias, taxa_dia, data_devolucao, observacao=""):
        self.leitor = leitor  # passa pelo setter → validado já na criação
        self.exemplar = exemplar  # passa pelo setter → validado já na criação
        self.dias = dias  # passa pelo setter → validado já na criação
        self.taxa_dia = taxa_dia  # passa pelo setter → validado já na criação
        self.data_devolucao = data_devolucao  # passa pelo setter → validado já na criação
        self.observacao = observacao  # sem regra → atributo simples (antifachada)

    @property
    def leitor(self):
        """Getter: lê `leitor` (o valor de verdade fica no atributo interno `_leitor`)."""
        return self._leitor

    @leitor.setter
    def leitor(self, valor):
        """Setter (a "fechadura"): só grava se a regra for respeitada — leitor: texto obrigatório (não pode ser vazio)."""
        if not isinstance(valor, str) or not valor.strip():
            raise ValueError("leitor é obrigatório (texto não vazio)")
        valor = valor.strip()  # guarda sem espaços nas pontas
        self._leitor = valor

    @property
    def exemplar(self):
        """Getter: lê `exemplar` (o valor de verdade fica no atributo interno `_exemplar`)."""
        return self._exemplar

    @exemplar.setter
    def exemplar(self, valor):
        """Setter (a "fechadura"): só grava se a regra for respeitada — exemplar: inteiro maior ou igual a 1."""
        # bool é subclasse de int em Python (True == 1): por isso é recusado explicitamente.
        if isinstance(valor, bool) or not isinstance(valor, int):
            raise ValueError("exemplar deve ser um número inteiro")
        if valor < 1:
            raise ValueError("exemplar deve ser no mínimo 1")
        self._exemplar = valor

    @property
    def dias(self):
        """Getter: lê `dias` (o valor de verdade fica no atributo interno `_dias`)."""
        return self._dias

    @dias.setter
    def dias(self, valor):
        """Setter (a "fechadura"): só grava se a regra for respeitada — dias: inteiro entre 1 e 30."""
        # bool é subclasse de int em Python (True == 1): por isso é recusado explicitamente.
        if isinstance(valor, bool) or not isinstance(valor, int):
            raise ValueError("dias deve ser um número inteiro")
        if not 1 <= valor <= 30:
            raise ValueError("dias deve estar entre 1 e 30")
        self._dias = valor

    @property
    def taxa_dia(self):
        """Getter: lê `taxa_dia` (o valor de verdade fica no atributo interno `_taxa_dia`)."""
        return self._taxa_dia

    @taxa_dia.setter
    def taxa_dia(self, valor):
        """Setter (a "fechadura"): só grava se a regra for respeitada — taxa_dia: número maior ou igual a 0."""
        if isinstance(valor, bool) or not isinstance(valor, (int, float)):
            raise ValueError("taxa_dia deve ser um número")
        if valor < 0:
            raise ValueError("taxa_dia deve ser no mínimo 0")
        self._taxa_dia = valor

    @property
    def data_devolucao(self):
        """Getter: lê `data_devolucao` (o valor de verdade fica no atributo interno `_data_devolucao`)."""
        return self._data_devolucao

    @data_devolucao.setter
    def data_devolucao(self, valor):
        """Setter (a "fechadura"): só grava se a regra for respeitada — data_devolucao: data e hora válidas no formato AAAA-MM-DDTHH:MM (ex.: 2026-01-10T09:30)."""
        # Data e hora ISO (AAAA-MM-DDTHH:MM): o mesmo formato do <input type="datetime-local"> e do DateTimeField.
        try:
            valida = isinstance(valor, str) and ("T" in valor or " " in valor) and len(valor) >= 16 and bool(datetime.fromisoformat(valor))
        except ValueError:
            valida = False
        if not valida:
            raise ValueError("data_devolucao deve ser uma data e hora válida (AAAA-MM-DDTHH:MM)")
        self._data_devolucao = valor

    @property
    def total(self):
        """Valor total = dias × taxa_dia (2 casas).

        Property CALCULADA e SÓ LEITURA: sem setter, `obj.total = 1` levanta AttributeError.
        Calculada na hora, acompanha qualquer mudança em dias ou taxa_dia.
        """
        return round(self.dias * self.taxa_dia, 2)

    def __repr__(self):
        return f"Emprestimo(leitor={self.leitor!r}, total={self.total})"
