"""
Farmácia Saúde — entidade principal `Receita` (ENCAPSULAMENTO com @property).

Gerado por gerar_sistema.py (determinístico, sem IA). Regras dos atributos:
  - cliente: texto obrigatório (não pode ser vazio)
  - balcao: inteiro maior ou igual a 1
  - unidades: inteiro entre 1 e 20
  - preco_unitario: número maior ou igual a 0
  - cnpj_fornecedor: CNPJ válido com 14 dígitos e dígitos verificadores
  - metadados: objeto ou lista JSON estruturada (dict ou list)
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


class Receita:
    """Receita do sistema Farmácia Saúde: total = unidades × preco_unitario."""

    def __init__(self, cliente, balcao, unidades, preco_unitario, cnpj_fornecedor, metadados, observacao=""):
        self.cliente = cliente  # passa pelo setter → validado já na criação
        self.balcao = balcao  # passa pelo setter → validado já na criação
        self.unidades = unidades  # passa pelo setter → validado já na criação
        self.preco_unitario = preco_unitario  # passa pelo setter → validado já na criação
        self.cnpj_fornecedor = cnpj_fornecedor  # passa pelo setter → validado já na criação
        self.metadados = metadados  # passa pelo setter → validado já na criação
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
    def balcao(self):
        """Getter: lê `balcao` (o valor de verdade fica no atributo interno `_balcao`)."""
        return self._balcao

    @balcao.setter
    def balcao(self, valor):
        """Setter (a "fechadura"): só grava se a regra for respeitada — balcao: inteiro maior ou igual a 1."""
        # bool é subclasse de int em Python (True == 1): por isso é recusado explicitamente.
        if isinstance(valor, bool) or not isinstance(valor, int):
            raise ValueError("balcao deve ser um número inteiro")
        if valor < 1:
            raise ValueError("balcao deve ser no mínimo 1")
        self._balcao = valor

    @property
    def unidades(self):
        """Getter: lê `unidades` (o valor de verdade fica no atributo interno `_unidades`)."""
        return self._unidades

    @unidades.setter
    def unidades(self, valor):
        """Setter (a "fechadura"): só grava se a regra for respeitada — unidades: inteiro entre 1 e 20."""
        # bool é subclasse de int em Python (True == 1): por isso é recusado explicitamente.
        if isinstance(valor, bool) or not isinstance(valor, int):
            raise ValueError("unidades deve ser um número inteiro")
        if not 1 <= valor <= 20:
            raise ValueError("unidades deve estar entre 1 e 20")
        self._unidades = valor

    @property
    def preco_unitario(self):
        """Getter: lê `preco_unitario` (o valor de verdade fica no atributo interno `_preco_unitario`)."""
        return self._preco_unitario

    @preco_unitario.setter
    def preco_unitario(self, valor):
        """Setter (a "fechadura"): só grava se a regra for respeitada — preco_unitario: número maior ou igual a 0."""
        if isinstance(valor, bool) or not isinstance(valor, (int, float)):
            raise ValueError("preco_unitario deve ser um número")
        if valor < 0:
            raise ValueError("preco_unitario deve ser no mínimo 0")
        self._preco_unitario = valor

    @property
    def cnpj_fornecedor(self):
        """Getter: lê `cnpj_fornecedor` (o valor de verdade fica no atributo interno `_cnpj_fornecedor`)."""
        return self._cnpj_fornecedor

    @cnpj_fornecedor.setter
    def cnpj_fornecedor(self, valor):
        """Setter (a "fechadura"): só grava se a regra for respeitada — cnpj_fornecedor: CNPJ válido com 14 dígitos e dígitos verificadores."""
        if not isinstance(valor, str) or not valor.strip():
            raise ValueError("cnpj_fornecedor é obrigatório (texto não vazio)")
        valor = valor.strip()  # guarda sem espaços nas pontas
        digitos = re.sub(r"\D", "", valor)
        if len(digitos) != 14 or len(set(digitos)) == 1:
            raise ValueError("cnpj_fornecedor deve ser um CNPJ válido")
        nums = [int(d) for d in digitos]
        r1 = sum(nums[i] * p for i, p in enumerate((5, 4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2))) % 11
        dv1 = 0 if r1 < 2 else 11 - r1
        r2 = sum(nums[i] * p for i, p in enumerate((6, 5, 4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2))) % 11
        dv2 = 0 if r2 < 2 else 11 - r2
        if nums[12] != dv1 or nums[13] != dv2:
            raise ValueError("cnpj_fornecedor possui dígitos verificadores de CNPJ inválidos")
        self._cnpj_fornecedor = valor

    @property
    def metadados(self):
        """Getter: lê `metadados` (o valor de verdade fica no atributo interno `_metadados`)."""
        return self._metadados

    @metadados.setter
    def metadados(self, valor):
        """Setter (a "fechadura"): só grava se a regra for respeitada — metadados: objeto ou lista JSON estruturada (dict ou list)."""
        # Objeto ou lista estruturada (equivalente ao JSONField do Django).
        if not isinstance(valor, (dict, list)):
            raise ValueError("metadados deve ser um objeto JSON (dict ou list)")
        self._metadados = valor

    @property
    def total(self):
        """Valor total = unidades × preco_unitario (2 casas).

        Property CALCULADA e SÓ LEITURA: sem setter, `obj.total = 1` levanta AttributeError.
        Calculada na hora, acompanha qualquer mudança em unidades ou preco_unitario.
        """
        return round(self.unidades * self.preco_unitario, 2)

    def __repr__(self):
        return f"Receita(cliente={self.cliente!r}, total={self.total})"
