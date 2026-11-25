"""
Clínica Vida — entidade principal `Consulta` (ENCAPSULAMENTO com @property).

Gerado por gerar_sistema.py (determinístico, sem IA). Regras dos atributos:
  - paciente: texto obrigatório (não pode ser vazio)
  - sala: inteiro maior ou igual a 1
  - sessoes: inteiro entre 1 e 12
  - valor_sessao: número maior ou igual a 0
  - cpf_paciente: CPF válido com 11 dígitos e dígitos verificadores
  - telefone_contato: telefone válido com 10 ou 11 dígitos (ex.: (11) 99999-8888)
  - anotacao: texto livre, sem regra (atributo simples — proteger seria cerimônia)

Ideias das Aulas 02 e 03:
  * o objeto controla o acesso ao próprio estado (encapsulamento);
  * @property + setter = a "fechadura": valida ANTES de gravar no atributo interno (_nome);
  * no __init__, `self.x = x` passa pelo setter → o objeto já nasce válido;
  * `total` é property CALCULADA (sem setter): nunca fica desatualizada;
  * atributo sem regra fica simples — @property sem problema que a justifique é cerimônia;
  * no model Django a mesma regra vai em validators (setter em campo quebra form/admin/ORM).
"""
import re


class Consulta:
    """Consulta do sistema Clínica Vida: total = sessoes × valor_sessao."""

    def __init__(self, paciente, sala, sessoes, valor_sessao, cpf_paciente, telefone_contato, anotacao=""):
        self.paciente = paciente  # passa pelo setter → validado já na criação
        self.sala = sala  # passa pelo setter → validado já na criação
        self.sessoes = sessoes  # passa pelo setter → validado já na criação
        self.valor_sessao = valor_sessao  # passa pelo setter → validado já na criação
        self.cpf_paciente = cpf_paciente  # passa pelo setter → validado já na criação
        self.telefone_contato = telefone_contato  # passa pelo setter → validado já na criação
        self.anotacao = anotacao  # sem regra → atributo simples (antifachada)

    @property
    def paciente(self):
        """Getter: lê `paciente` (o valor de verdade fica no atributo interno `_paciente`)."""
        return self._paciente

    @paciente.setter
    def paciente(self, valor):
        """Setter (a "fechadura"): só grava se a regra for respeitada — paciente: texto obrigatório (não pode ser vazio)."""
        if not isinstance(valor, str) or not valor.strip():
            raise ValueError("paciente é obrigatório (texto não vazio)")
        valor = valor.strip()  # guarda sem espaços nas pontas
        self._paciente = valor

    @property
    def sala(self):
        """Getter: lê `sala` (o valor de verdade fica no atributo interno `_sala`)."""
        return self._sala

    @sala.setter
    def sala(self, valor):
        """Setter (a "fechadura"): só grava se a regra for respeitada — sala: inteiro maior ou igual a 1."""
        # bool é subclasse de int em Python (True == 1): por isso é recusado explicitamente.
        if isinstance(valor, bool) or not isinstance(valor, int):
            raise ValueError("sala deve ser um número inteiro")
        if valor < 1:
            raise ValueError("sala deve ser no mínimo 1")
        self._sala = valor

    @property
    def sessoes(self):
        """Getter: lê `sessoes` (o valor de verdade fica no atributo interno `_sessoes`)."""
        return self._sessoes

    @sessoes.setter
    def sessoes(self, valor):
        """Setter (a "fechadura"): só grava se a regra for respeitada — sessoes: inteiro entre 1 e 12."""
        # bool é subclasse de int em Python (True == 1): por isso é recusado explicitamente.
        if isinstance(valor, bool) or not isinstance(valor, int):
            raise ValueError("sessoes deve ser um número inteiro")
        if not 1 <= valor <= 12:
            raise ValueError("sessoes deve estar entre 1 e 12")
        self._sessoes = valor

    @property
    def valor_sessao(self):
        """Getter: lê `valor_sessao` (o valor de verdade fica no atributo interno `_valor_sessao`)."""
        return self._valor_sessao

    @valor_sessao.setter
    def valor_sessao(self, valor):
        """Setter (a "fechadura"): só grava se a regra for respeitada — valor_sessao: número maior ou igual a 0."""
        if isinstance(valor, bool) or not isinstance(valor, (int, float)):
            raise ValueError("valor_sessao deve ser um número")
        if valor < 0:
            raise ValueError("valor_sessao deve ser no mínimo 0")
        self._valor_sessao = valor

    @property
    def cpf_paciente(self):
        """Getter: lê `cpf_paciente` (o valor de verdade fica no atributo interno `_cpf_paciente`)."""
        return self._cpf_paciente

    @cpf_paciente.setter
    def cpf_paciente(self, valor):
        """Setter (a "fechadura"): só grava se a regra for respeitada — cpf_paciente: CPF válido com 11 dígitos e dígitos verificadores."""
        if not isinstance(valor, str) or not valor.strip():
            raise ValueError("cpf_paciente é obrigatório (texto não vazio)")
        valor = valor.strip()  # guarda sem espaços nas pontas
        digitos = re.sub(r"\D", "", valor)
        if len(digitos) != 11 or len(set(digitos)) == 1:
            raise ValueError("cpf_paciente deve ser um CPF válido")
        nums = [int(d) for d in digitos]
        dv1 = (sum(nums[i] * (10 - i) for i in range(9)) * 10 % 11) % 10
        dv2 = (sum(nums[i] * (11 - i) for i in range(10)) * 10 % 11) % 10
        if nums[9] != dv1 or nums[10] != dv2:
            raise ValueError("cpf_paciente possui dígitos verificadores de CPF inválidos")
        self._cpf_paciente = valor

    @property
    def telefone_contato(self):
        """Getter: lê `telefone_contato` (o valor de verdade fica no atributo interno `_telefone_contato`)."""
        return self._telefone_contato

    @telefone_contato.setter
    def telefone_contato(self, valor):
        """Setter (a "fechadura"): só grava se a regra for respeitada — telefone_contato: telefone válido com 10 ou 11 dígitos (ex.: (11) 99999-8888)."""
        if not isinstance(valor, str) or not valor.strip():
            raise ValueError("telefone_contato é obrigatório (texto não vazio)")
        valor = valor.strip()  # guarda sem espaços nas pontas
        digitos = re.sub(r"\D", "", valor)
        if len(digitos) not in (10, 11):
            raise ValueError("telefone_contato deve ser um telefone válido (10 ou 11 dígitos)")
        self._telefone_contato = valor

    @property
    def total(self):
        """Valor total = sessoes × valor_sessao (2 casas).

        Property CALCULADA e SÓ LEITURA: sem setter, `obj.total = 1` levanta AttributeError.
        Calculada na hora, acompanha qualquer mudança em sessoes ou valor_sessao.
        """
        return round(self.sessoes * self.valor_sessao, 2)

    def __repr__(self):
        return f"Consulta(paciente={self.paciente!r}, total={self.total})"
