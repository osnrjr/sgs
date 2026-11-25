"""
Vento Sul Energia Eólica — entidade principal `ParqueAerogerador` (ENCAPSULAMENTO com @property).

Gerado por gerar_sistema.py (determinístico, sem IA). Regras dos atributos:
  - operador: texto obrigatório (não pode ser vazio)
  - torre: inteiro maior ou igual a 1
  - megawatts: inteiro entre 1 e 50
  - preco_mwh: número maior ou igual a 0
  - geoloc: coordenadas latitude,longitude (-90..90, -180..180)
  - parametros_json: objeto ou lista JSON estruturada (dict ou list)
  - observacao: texto livre, sem regra (atributo simples — proteger seria cerimônia)

Ideias das Aulas 02 e 03:
  * o objeto controla o acesso ao próprio estado (encapsulamento);
  * @property + setter = a "fechadura": valida ANTES de gravar no atributo interno (_nome);
  * no __init__, `self.x = x` passa pelo setter → o objeto já nasce válido;
  * `total` é property CALCULADA (sem setter): nunca fica desatualizada;
  * atributo sem regra fica simples — @property sem problema que a justifique é cerimônia;
  * no model Django a mesma regra vai em validators (setter em campo quebra form/admin/ORM).
"""


class ParqueAerogerador:
    """ParqueAerogerador do sistema Vento Sul Energia Eólica: total = megawatts × preco_mwh."""

    def __init__(self, operador, torre, megawatts, preco_mwh, geoloc, parametros_json, observacao=""):
        self.operador = operador  # passa pelo setter → validado já na criação
        self.torre = torre  # passa pelo setter → validado já na criação
        self.megawatts = megawatts  # passa pelo setter → validado já na criação
        self.preco_mwh = preco_mwh  # passa pelo setter → validado já na criação
        self.geoloc = geoloc  # passa pelo setter → validado já na criação
        self.parametros_json = parametros_json  # passa pelo setter → validado já na criação
        self.observacao = observacao  # sem regra → atributo simples (antifachada)

    @property
    def operador(self):
        """Getter: lê `operador` (o valor de verdade fica no atributo interno `_operador`)."""
        return self._operador

    @operador.setter
    def operador(self, valor):
        """Setter (a "fechadura"): só grava se a regra for respeitada — operador: texto obrigatório (não pode ser vazio)."""
        if not isinstance(valor, str) or not valor.strip():
            raise ValueError("operador é obrigatório (texto não vazio)")
        valor = valor.strip()  # guarda sem espaços nas pontas
        self._operador = valor

    @property
    def torre(self):
        """Getter: lê `torre` (o valor de verdade fica no atributo interno `_torre`)."""
        return self._torre

    @torre.setter
    def torre(self, valor):
        """Setter (a "fechadura"): só grava se a regra for respeitada — torre: inteiro maior ou igual a 1."""
        # bool é subclasse de int em Python (True == 1): por isso é recusado explicitamente.
        if isinstance(valor, bool) or not isinstance(valor, int):
            raise ValueError("torre deve ser um número inteiro")
        if valor < 1:
            raise ValueError("torre deve ser no mínimo 1")
        self._torre = valor

    @property
    def megawatts(self):
        """Getter: lê `megawatts` (o valor de verdade fica no atributo interno `_megawatts`)."""
        return self._megawatts

    @megawatts.setter
    def megawatts(self, valor):
        """Setter (a "fechadura"): só grava se a regra for respeitada — megawatts: inteiro entre 1 e 50."""
        # bool é subclasse de int em Python (True == 1): por isso é recusado explicitamente.
        if isinstance(valor, bool) or not isinstance(valor, int):
            raise ValueError("megawatts deve ser um número inteiro")
        if not 1 <= valor <= 50:
            raise ValueError("megawatts deve estar entre 1 e 50")
        self._megawatts = valor

    @property
    def preco_mwh(self):
        """Getter: lê `preco_mwh` (o valor de verdade fica no atributo interno `_preco_mwh`)."""
        return self._preco_mwh

    @preco_mwh.setter
    def preco_mwh(self, valor):
        """Setter (a "fechadura"): só grava se a regra for respeitada — preco_mwh: número maior ou igual a 0."""
        if isinstance(valor, bool) or not isinstance(valor, (int, float)):
            raise ValueError("preco_mwh deve ser um número")
        if valor < 0:
            raise ValueError("preco_mwh deve ser no mínimo 0")
        self._preco_mwh = valor

    @property
    def geoloc(self):
        """Getter: lê `geoloc` (o valor de verdade fica no atributo interno `_geoloc`)."""
        return self._geoloc

    @geoloc.setter
    def geoloc(self, valor):
        """Setter (a "fechadura"): só grava se a regra for respeitada — geoloc: coordenadas latitude,longitude (-90..90, -180..180)."""
        if not isinstance(valor, str) or not valor.strip():
            raise ValueError("geoloc é obrigatório (texto não vazio)")
        valor = valor.strip()  # guarda sem espaços nas pontas
        partes = [p.strip() for p in valor.split(",")]
        try:
            lat, lng = (float(partes[0]), float(partes[1])) if len(partes) == 2 else (999.0, 999.0)
        except ValueError:
            lat, lng = 999.0, 999.0
        if not (-90.0 <= lat <= 90.0 and -180.0 <= lng <= 180.0):
            raise ValueError("geoloc deve ser latitude,longitude válida (-90..90, -180..180)")
        self._geoloc = valor

    @property
    def parametros_json(self):
        """Getter: lê `parametros_json` (o valor de verdade fica no atributo interno `_parametros_json`)."""
        return self._parametros_json

    @parametros_json.setter
    def parametros_json(self, valor):
        """Setter (a "fechadura"): só grava se a regra for respeitada — parametros_json: objeto ou lista JSON estruturada (dict ou list)."""
        # Objeto ou lista estruturada (equivalente ao JSONField do Django).
        if not isinstance(valor, (dict, list)):
            raise ValueError("parametros_json deve ser um objeto JSON (dict ou list)")
        self._parametros_json = valor

    @property
    def total(self):
        """Valor total = megawatts × preco_mwh (2 casas).

        Property CALCULADA e SÓ LEITURA: sem setter, `obj.total = 1` levanta AttributeError.
        Calculada na hora, acompanha qualquer mudança em megawatts ou preco_mwh.
        """
        return round(self.megawatts * self.preco_mwh, 2)

    def __repr__(self):
        return f"ParqueAerogerador(operador={self.operador!r}, total={self.total})"
