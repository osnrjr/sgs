"""
Hotel Resort — entidade principal `Reserva` (ENCAPSULAMENTO com @property).

Gerado por gerar_sistema.py (determinístico, sem IA). Regras dos atributos:
  - hospede: texto obrigatório (não pode ser vazio)
  - quarto: inteiro maior ou igual a 1
  - diarias: inteiro entre 1 e 30
  - valor_diaria: número maior ou igual a 0
  - agendado_em: data e hora válidas no formato AAAA-MM-DDTHH:MM (ex.: 2026-01-10T09:30)
  - email_hospede: endereço de e-mail válido (ex.: nome@dominio.com)
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
from datetime import datetime


class Reserva:
    """Reserva do sistema Hotel Resort: total = diarias × valor_diaria."""

    def __init__(self, hospede, quarto, diarias, valor_diaria, agendado_em, email_hospede, observacao=""):
        self.hospede = hospede  # passa pelo setter → validado já na criação
        self.quarto = quarto  # passa pelo setter → validado já na criação
        self.diarias = diarias  # passa pelo setter → validado já na criação
        self.valor_diaria = valor_diaria  # passa pelo setter → validado já na criação
        self.agendado_em = agendado_em  # passa pelo setter → validado já na criação
        self.email_hospede = email_hospede  # passa pelo setter → validado já na criação
        self.observacao = observacao  # sem regra → atributo simples (antifachada)

    @property
    def hospede(self):
        """Getter: lê `hospede` (o valor de verdade fica no atributo interno `_hospede`)."""
        return self._hospede

    @hospede.setter
    def hospede(self, valor):
        """Setter (a "fechadura"): só grava se a regra for respeitada — hospede: texto obrigatório (não pode ser vazio)."""
        if not isinstance(valor, str) or not valor.strip():
            raise ValueError("hospede é obrigatório (texto não vazio)")
        valor = valor.strip()  # guarda sem espaços nas pontas
        self._hospede = valor

    @property
    def quarto(self):
        """Getter: lê `quarto` (o valor de verdade fica no atributo interno `_quarto`)."""
        return self._quarto

    @quarto.setter
    def quarto(self, valor):
        """Setter (a "fechadura"): só grava se a regra for respeitada — quarto: inteiro maior ou igual a 1."""
        # bool é subclasse de int em Python (True == 1): por isso é recusado explicitamente.
        if isinstance(valor, bool) or not isinstance(valor, int):
            raise ValueError("quarto deve ser um número inteiro")
        if valor < 1:
            raise ValueError("quarto deve ser no mínimo 1")
        self._quarto = valor

    @property
    def diarias(self):
        """Getter: lê `diarias` (o valor de verdade fica no atributo interno `_diarias`)."""
        return self._diarias

    @diarias.setter
    def diarias(self, valor):
        """Setter (a "fechadura"): só grava se a regra for respeitada — diarias: inteiro entre 1 e 30."""
        # bool é subclasse de int em Python (True == 1): por isso é recusado explicitamente.
        if isinstance(valor, bool) or not isinstance(valor, int):
            raise ValueError("diarias deve ser um número inteiro")
        if not 1 <= valor <= 30:
            raise ValueError("diarias deve estar entre 1 e 30")
        self._diarias = valor

    @property
    def valor_diaria(self):
        """Getter: lê `valor_diaria` (o valor de verdade fica no atributo interno `_valor_diaria`)."""
        return self._valor_diaria

    @valor_diaria.setter
    def valor_diaria(self, valor):
        """Setter (a "fechadura"): só grava se a regra for respeitada — valor_diaria: número maior ou igual a 0."""
        if isinstance(valor, bool) or not isinstance(valor, (int, float)):
            raise ValueError("valor_diaria deve ser um número")
        if valor < 0:
            raise ValueError("valor_diaria deve ser no mínimo 0")
        self._valor_diaria = valor

    @property
    def agendado_em(self):
        """Getter: lê `agendado_em` (o valor de verdade fica no atributo interno `_agendado_em`)."""
        return self._agendado_em

    @agendado_em.setter
    def agendado_em(self, valor):
        """Setter (a "fechadura"): só grava se a regra for respeitada — agendado_em: data e hora válidas no formato AAAA-MM-DDTHH:MM (ex.: 2026-01-10T09:30)."""
        # Data e hora ISO (AAAA-MM-DDTHH:MM): o mesmo formato do <input type="datetime-local"> e do DateTimeField.
        try:
            valida = isinstance(valor, str) and ("T" in valor or " " in valor) and len(valor) >= 16 and bool(datetime.fromisoformat(valor))
        except ValueError:
            valida = False
        if not valida:
            raise ValueError("agendado_em deve ser uma data e hora válida (AAAA-MM-DDTHH:MM)")
        self._agendado_em = valor

    @property
    def email_hospede(self):
        """Getter: lê `email_hospede` (o valor de verdade fica no atributo interno `_email_hospede`)."""
        return self._email_hospede

    @email_hospede.setter
    def email_hospede(self, valor):
        """Setter (a "fechadura"): só grava se a regra for respeitada — email_hospede: endereço de e-mail válido (ex.: nome@dominio.com)."""
        if not isinstance(valor, str) or not valor.strip():
            raise ValueError("email_hospede é obrigatório (texto não vazio)")
        valor = valor.strip()  # guarda sem espaços nas pontas
        if not re.fullmatch(r"[^@\s]+@[^@\s]+\.[^@\s]+", valor):
            raise ValueError("email_hospede deve ser um e-mail válido")
        self._email_hospede = valor

    @property
    def total(self):
        """Valor total = diarias × valor_diaria (2 casas).

        Property CALCULADA e SÓ LEITURA: sem setter, `obj.total = 1` levanta AttributeError.
        Calculada na hora, acompanha qualquer mudança em diarias ou valor_diaria.
        """
        return round(self.diarias * self.valor_diaria, 2)

    def __repr__(self):
        return f"Reserva(hospede={self.hospede!r}, total={self.total})"
