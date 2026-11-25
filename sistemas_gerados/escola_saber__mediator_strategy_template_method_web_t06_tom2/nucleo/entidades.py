"""
Escola Saber — entidade principal `Turma` (ENCAPSULAMENTO com @property).

Gerado por gerar_sistema.py (determinístico, sem IA). Regras dos atributos:
  - aluno: texto obrigatório (não pode ser vazio)
  - sala: inteiro maior ou igual a 1
  - meses: inteiro entre 1 e 12
  - mensalidade: número maior ou igual a 0
  - portal_url: URL válida começando com http:// ou https://
  - comprovante: caminho ou URL de arquivo/anexo com extensão (ex.: relatorio.pdf)
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


class Turma:
    """Turma do sistema Escola Saber: total = meses × mensalidade."""

    def __init__(self, aluno, sala, meses, mensalidade, portal_url, comprovante, observacao=""):
        self.aluno = aluno  # passa pelo setter → validado já na criação
        self.sala = sala  # passa pelo setter → validado já na criação
        self.meses = meses  # passa pelo setter → validado já na criação
        self.mensalidade = mensalidade  # passa pelo setter → validado já na criação
        self.portal_url = portal_url  # passa pelo setter → validado já na criação
        self.comprovante = comprovante  # passa pelo setter → validado já na criação
        self.observacao = observacao  # sem regra → atributo simples (antifachada)

    @property
    def aluno(self):
        """Getter: lê `aluno` (o valor de verdade fica no atributo interno `_aluno`)."""
        return self._aluno

    @aluno.setter
    def aluno(self, valor):
        """Setter (a "fechadura"): só grava se a regra for respeitada — aluno: texto obrigatório (não pode ser vazio)."""
        if not isinstance(valor, str) or not valor.strip():
            raise ValueError("aluno é obrigatório (texto não vazio)")
        valor = valor.strip()  # guarda sem espaços nas pontas
        self._aluno = valor

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
    def meses(self):
        """Getter: lê `meses` (o valor de verdade fica no atributo interno `_meses`)."""
        return self._meses

    @meses.setter
    def meses(self, valor):
        """Setter (a "fechadura"): só grava se a regra for respeitada — meses: inteiro entre 1 e 12."""
        # bool é subclasse de int em Python (True == 1): por isso é recusado explicitamente.
        if isinstance(valor, bool) or not isinstance(valor, int):
            raise ValueError("meses deve ser um número inteiro")
        if not 1 <= valor <= 12:
            raise ValueError("meses deve estar entre 1 e 12")
        self._meses = valor

    @property
    def mensalidade(self):
        """Getter: lê `mensalidade` (o valor de verdade fica no atributo interno `_mensalidade`)."""
        return self._mensalidade

    @mensalidade.setter
    def mensalidade(self, valor):
        """Setter (a "fechadura"): só grava se a regra for respeitada — mensalidade: número maior ou igual a 0."""
        if isinstance(valor, bool) or not isinstance(valor, (int, float)):
            raise ValueError("mensalidade deve ser um número")
        if valor < 0:
            raise ValueError("mensalidade deve ser no mínimo 0")
        self._mensalidade = valor

    @property
    def portal_url(self):
        """Getter: lê `portal_url` (o valor de verdade fica no atributo interno `_portal_url`)."""
        return self._portal_url

    @portal_url.setter
    def portal_url(self, valor):
        """Setter (a "fechadura"): só grava se a regra for respeitada — portal_url: URL válida começando com http:// ou https://."""
        if not isinstance(valor, str) or not valor.strip():
            raise ValueError("portal_url é obrigatório (texto não vazio)")
        valor = valor.strip()  # guarda sem espaços nas pontas
        if not re.fullmatch(r"https?://[^\s/$.?#].[^\s]*", valor):
            raise ValueError("portal_url deve ser uma URL válida começando com http:// ou https://")
        self._portal_url = valor

    @property
    def comprovante(self):
        """Getter: lê `comprovante` (o valor de verdade fica no atributo interno `_comprovante`)."""
        return self._comprovante

    @comprovante.setter
    def comprovante(self, valor):
        """Setter (a "fechadura"): só grava se a regra for respeitada — comprovante: caminho ou URL de arquivo/anexo com extensão (ex.: relatorio.pdf)."""
        if not isinstance(valor, str) or not valor.strip():
            raise ValueError("comprovante é obrigatório (texto não vazio)")
        valor = valor.strip()  # guarda sem espaços nas pontas
        if not re.fullmatch(r"(?:https?://[^\s]+|[\w./-]+)\.[A-Za-z0-9]{2,6}", valor):
            raise ValueError("comprovante deve ser um caminho ou URL de arquivo com extensão")
        self._comprovante = valor

    @property
    def total(self):
        """Valor total = meses × mensalidade (2 casas).

        Property CALCULADA e SÓ LEITURA: sem setter, `obj.total = 1` levanta AttributeError.
        Calculada na hora, acompanha qualquer mudança em meses ou mensalidade.
        """
        return round(self.meses * self.mensalidade, 2)

    def __repr__(self):
        return f"Turma(aluno={self.aluno!r}, total={self.total})"
