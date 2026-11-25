"""
TransLog Cargas — entidade principal `Frete` (ENCAPSULAMENTO com @property).

Gerado por gerar_sistema.py (determinístico, sem IA). Regras dos atributos:
  - cliente: texto obrigatório (não pode ser vazio)
  - caminhao: inteiro maior ou igual a 1
  - toneladas: inteiro entre 1 e 40
  - valor_tonelada: número maior ou igual a 0
  - coordenadas: coordenadas latitude,longitude (-90..90, -180..180)
  - etiquetas: múltipla escolha (separada por vírgula) entre fragil, urgente, refrigerado
  - observacao: texto livre, sem regra (atributo simples — proteger seria cerimônia)

Ideias das Aulas 02 e 03:
  * o objeto controla o acesso ao próprio estado (encapsulamento);
  * @property + setter = a "fechadura": valida ANTES de gravar no atributo interno (_nome);
  * no __init__, `self.x = x` passa pelo setter → o objeto já nasce válido;
  * `total` é property CALCULADA (sem setter): nunca fica desatualizada;
  * atributo sem regra fica simples — @property sem problema que a justifique é cerimônia;
  * no model Django a mesma regra vai em validators (setter em campo quebra form/admin/ORM).
"""


class Frete:
    """Frete do sistema TransLog Cargas: total = toneladas × valor_tonelada."""

    def __init__(self, cliente, caminhao, toneladas, valor_tonelada, coordenadas, etiquetas, observacao=""):
        self.cliente = cliente  # passa pelo setter → validado já na criação
        self.caminhao = caminhao  # passa pelo setter → validado já na criação
        self.toneladas = toneladas  # passa pelo setter → validado já na criação
        self.valor_tonelada = valor_tonelada  # passa pelo setter → validado já na criação
        self.coordenadas = coordenadas  # passa pelo setter → validado já na criação
        self.etiquetas = etiquetas  # passa pelo setter → validado já na criação
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
    def caminhao(self):
        """Getter: lê `caminhao` (o valor de verdade fica no atributo interno `_caminhao`)."""
        return self._caminhao

    @caminhao.setter
    def caminhao(self, valor):
        """Setter (a "fechadura"): só grava se a regra for respeitada — caminhao: inteiro maior ou igual a 1."""
        # bool é subclasse de int em Python (True == 1): por isso é recusado explicitamente.
        if isinstance(valor, bool) or not isinstance(valor, int):
            raise ValueError("caminhao deve ser um número inteiro")
        if valor < 1:
            raise ValueError("caminhao deve ser no mínimo 1")
        self._caminhao = valor

    @property
    def toneladas(self):
        """Getter: lê `toneladas` (o valor de verdade fica no atributo interno `_toneladas`)."""
        return self._toneladas

    @toneladas.setter
    def toneladas(self, valor):
        """Setter (a "fechadura"): só grava se a regra for respeitada — toneladas: inteiro entre 1 e 40."""
        # bool é subclasse de int em Python (True == 1): por isso é recusado explicitamente.
        if isinstance(valor, bool) or not isinstance(valor, int):
            raise ValueError("toneladas deve ser um número inteiro")
        if not 1 <= valor <= 40:
            raise ValueError("toneladas deve estar entre 1 e 40")
        self._toneladas = valor

    @property
    def valor_tonelada(self):
        """Getter: lê `valor_tonelada` (o valor de verdade fica no atributo interno `_valor_tonelada`)."""
        return self._valor_tonelada

    @valor_tonelada.setter
    def valor_tonelada(self, valor):
        """Setter (a "fechadura"): só grava se a regra for respeitada — valor_tonelada: número maior ou igual a 0."""
        if isinstance(valor, bool) or not isinstance(valor, (int, float)):
            raise ValueError("valor_tonelada deve ser um número")
        if valor < 0:
            raise ValueError("valor_tonelada deve ser no mínimo 0")
        self._valor_tonelada = valor

    @property
    def coordenadas(self):
        """Getter: lê `coordenadas` (o valor de verdade fica no atributo interno `_coordenadas`)."""
        return self._coordenadas

    @coordenadas.setter
    def coordenadas(self, valor):
        """Setter (a "fechadura"): só grava se a regra for respeitada — coordenadas: coordenadas latitude,longitude (-90..90, -180..180)."""
        if not isinstance(valor, str) or not valor.strip():
            raise ValueError("coordenadas é obrigatório (texto não vazio)")
        valor = valor.strip()  # guarda sem espaços nas pontas
        partes = [p.strip() for p in valor.split(",")]
        try:
            lat, lng = (float(partes[0]), float(partes[1])) if len(partes) == 2 else (999.0, 999.0)
        except ValueError:
            lat, lng = 999.0, 999.0
        if not (-90.0 <= lat <= 90.0 and -180.0 <= lng <= 180.0):
            raise ValueError("coordenadas deve ser latitude,longitude válida (-90..90, -180..180)")
        self._coordenadas = valor

    @property
    def etiquetas(self):
        """Getter: lê `etiquetas` (o valor de verdade fica no atributo interno `_etiquetas`)."""
        return self._etiquetas

    @etiquetas.setter
    def etiquetas(self, valor):
        """Setter (a "fechadura"): só grava se a regra for respeitada — etiquetas: múltipla escolha (separada por vírgula) entre fragil, urgente, refrigerado."""
        if not isinstance(valor, str) or not valor.strip():
            raise ValueError("etiquetas é obrigatório (texto não vazio)")
        valor = valor.strip()  # guarda sem espaços nas pontas
        # Múltipla escolha: lista separada por vírgula apenas com opções permitidas.
        itens = [p.strip() for p in valor.split(",") if p.strip()]
        permitidas = {'fragil', 'urgente', 'refrigerado'}
        if not itens or len(set(itens)) != len(itens) or any(p not in permitidas for p in itens):
            raise ValueError("etiquetas aceita apenas combinações de: fragil, urgente, refrigerado")
        valor = ",".join(itens)
        self._etiquetas = valor

    @property
    def total(self):
        """Valor total = toneladas × valor_tonelada (2 casas).

        Property CALCULADA e SÓ LEITURA: sem setter, `obj.total = 1` levanta AttributeError.
        Calculada na hora, acompanha qualquer mudança em toneladas ou valor_tonelada.
        """
        return round(self.toneladas * self.valor_tonelada, 2)

    def __repr__(self):
        return f"Frete(cliente={self.cliente!r}, total={self.total})"
