"""
Restaurante Sabor — entidade principal `Comanda` (ENCAPSULAMENTO com @property).

Gerado por gerar_sistema.py (determinístico, sem IA). Regras dos atributos:
  - cliente: texto obrigatório (não pode ser vazio)
  - mesa: inteiro maior ou igual a 1
  - pratos: inteiro entre 1 e 20
  - preco_prato: número maior ou igual a 0
  - horario_pedido: data e hora válidas no formato AAAA-MM-DDTHH:MM (ex.: 2026-01-10T09:30)
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


class Comanda:
    """Comanda do sistema Restaurante Sabor: total = pratos × preco_prato."""

    def __init__(self, cliente, mesa, pratos, preco_prato, horario_pedido, observacao=""):
        self.cliente = cliente  # passa pelo setter → validado já na criação
        self.mesa = mesa  # passa pelo setter → validado já na criação
        self.pratos = pratos  # passa pelo setter → validado já na criação
        self.preco_prato = preco_prato  # passa pelo setter → validado já na criação
        self.horario_pedido = horario_pedido  # passa pelo setter → validado já na criação
        self.observacao = observacao  # sem regra → atributo simples (antifachada)

    @property
    def cliente(self):
        """Getter: lê `cliente` (o valor de verdade fica no atributo interno `_cliente`)."""
        return self._cliente

    @cliente.setter
    def cliente(self, valor):
        """Setter (a "fechadura"): só grava se a regra for respeitada — cliente: texto obrigatório (não pode ser vazio)."""
        if not isinstance(valor, str) or not valor.strip():
            raise ValueError("cliente é obrigatório (texto não vazio)")
        valor = valor.strip()  # guarda sem espaços nas pontas
        self._cliente = valor

    @property
    def mesa(self):
        """Getter: lê `mesa` (o valor de verdade fica no atributo interno `_mesa`)."""
        return self._mesa

    @mesa.setter
    def mesa(self, valor):
        """Setter (a "fechadura"): só grava se a regra for respeitada — mesa: inteiro maior ou igual a 1."""
        # bool é subclasse de int em Python (True == 1): por isso é recusado explicitamente.
        if isinstance(valor, bool) or not isinstance(valor, int):
            raise ValueError("mesa deve ser um número inteiro")
        if valor < 1:
            raise ValueError("mesa deve ser no mínimo 1")
        self._mesa = valor

    @property
    def pratos(self):
        """Getter: lê `pratos` (o valor de verdade fica no atributo interno `_pratos`)."""
        return self._pratos

    @pratos.setter
    def pratos(self, valor):
        """Setter (a "fechadura"): só grava se a regra for respeitada — pratos: inteiro entre 1 e 20."""
        # bool é subclasse de int em Python (True == 1): por isso é recusado explicitamente.
        if isinstance(valor, bool) or not isinstance(valor, int):
            raise ValueError("pratos deve ser um número inteiro")
        if not 1 <= valor <= 20:
            raise ValueError("pratos deve estar entre 1 e 20")
        self._pratos = valor

    @property
    def preco_prato(self):
        """Getter: lê `preco_prato` (o valor de verdade fica no atributo interno `_preco_prato`)."""
        return self._preco_prato

    @preco_prato.setter
    def preco_prato(self, valor):
        """Setter (a "fechadura"): só grava se a regra for respeitada — preco_prato: número maior ou igual a 0."""
        if isinstance(valor, bool) or not isinstance(valor, (int, float)):
            raise ValueError("preco_prato deve ser um número")
        if valor < 0:
            raise ValueError("preco_prato deve ser no mínimo 0")
        self._preco_prato = valor

    @property
    def horario_pedido(self):
        """Getter: lê `horario_pedido` (o valor de verdade fica no atributo interno `_horario_pedido`)."""
        return self._horario_pedido

    @horario_pedido.setter
    def horario_pedido(self, valor):
        """Setter (a "fechadura"): só grava se a regra for respeitada — horario_pedido: data e hora válidas no formato AAAA-MM-DDTHH:MM (ex.: 2026-01-10T09:30)."""
        # Data e hora ISO (AAAA-MM-DDTHH:MM): o mesmo formato do <input type="datetime-local"> e do DateTimeField.
        try:
            valida = isinstance(valor, str) and ("T" in valor or " " in valor) and len(valor) >= 16 and bool(datetime.fromisoformat(valor))
        except ValueError:
            valida = False
        if not valida:
            raise ValueError("horario_pedido deve ser uma data e hora válida (AAAA-MM-DDTHH:MM)")
        self._horario_pedido = valor

    @property
    def total(self):
        """Valor total = pratos × preco_prato (2 casas).

        Property CALCULADA e SÓ LEITURA: sem setter, `obj.total = 1` levanta AttributeError.
        Calculada na hora, acompanha qualquer mudança em pratos ou preco_prato.
        """
        return round(self.pratos * self.preco_prato, 2)

    def __repr__(self):
        return f"Comanda(cliente={self.cliente!r}, total={self.total})"
