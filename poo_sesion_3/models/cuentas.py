# models/cuentas.py
from __future__ import annotations


class CuentaBase:
    """
    Clase base para cuentas bancarias.

    Invariantes comunes:
    - titular no vacío
    - monto de operación > 0
    - si la cuenta está cerrada, no se puede operar

    Nota pedagógica:
    - Esta clase define la "interfaz" de lo que una cuenta sabe hacer.
    - Las subclases sobrescriben lo que cambie (polimorfismo).
    """

    _next_id: int = 1

    def __init__(self, titular: str, saldo_inicial: float = 0.0) -> None:
        self._id: int = CuentaBase._next_id
        CuentaBase._next_id += 1

        self._titular: str = ""
        self.titular = titular

        self._saldo: float = 0.0
        self._set_saldo_inicial(saldo_inicial)

        self._activa: bool = True

    # -------------------------
    # Propiedades
    # -------------------------
    @property
    def id(self) -> int:
        return self._id

    @property
    def titular(self) -> str:
        return self._titular

    @titular.setter
    def titular(self, value: str) -> None:
        if value is None:
            raise ValueError("El titular no puede ser None.")
        value = str(value).strip()
        if not value:
            raise ValueError("El titular no puede estar vacío.")
        self._titular = value

    @property
    def saldo(self) -> float:
        # Solo lectura: se modifica por consignar/retirar/corte mensual
        return self._saldo

    @property
    def activa(self) -> bool:
        return self._activa

    # -------------------------
    # Métodos de negocio comunes
    # -------------------------
    def consignar(self, monto: float) -> None:
        self._asegurar_activa()
        monto = self._normalizar_monto(monto)
        self._saldo += monto

    def retirar(self, monto: float) -> None:
        """
        Retiro por defecto (CuentaBase):
        - NO permite saldo negativo.
        Subclases pueden sobrescribir si cambian reglas.
        """
        self._asegurar_activa()
        monto = self._normalizar_monto(monto)

        if monto > self._saldo:
            raise ValueError("Fondos insuficientes para realizar el retiro.")
        self._saldo -= monto

    def cerrar(self) -> None:
        self._activa = False

    def aplicar_corte_mensual(self) -> None:
        """
        Polimorfismo:
        - Por defecto no hace nada.
        - Subclases (Ahorros/Corriente) implementan su lógica.
        """
        self._asegurar_activa()

    # -------------------------
    # Internos
    # -------------------------
    def _set_saldo_inicial(self, saldo_inicial: float) -> None:
        saldo_inicial = float(saldo_inicial)
        if saldo_inicial < 0:
            raise ValueError("El saldo inicial no puede ser negativo.")
        self._saldo = saldo_inicial

    def _normalizar_monto(self, monto: float) -> float:
        monto = float(monto)
        if monto <= 0:
            raise ValueError("El monto debe ser mayor que 0.")
        return monto

    def _asegurar_activa(self) -> None:
        if not self._activa:
            raise ValueError("No se puede operar sobre una cuenta cerrada.")

    def tipo(self) -> str:
        """Nombre amigable del tipo de cuenta."""
        return self.__class__.__name__

    def __str__(self) -> str:
        estado = "activa" if self._activa else "cerrada"
        return (
            f"{self.tipo()}(id={self._id}, titular='{self._titular}', "
            f"saldo={self._saldo:.2f}, estado={estado})"
        )


class CuentaAhorros(CuentaBase):
    """
    Cuenta de ahorros:
    - No permite sobregiro (usa retirar del padre)
    - Gana intereses en el corte mensual
    """

    def __init__(self, titular: str, saldo_inicial: float = 0.0, tasa_interes: float = 0.01) -> None:
        # super() reusa inicialización base
        super().__init__(titular=titular, saldo_inicial=saldo_inicial)
        self._tasa_interes: float = float(tasa_interes)
        if self._tasa_interes < 0:
            raise ValueError("La tasa de interés no puede ser negativa.")

    @property
    def tasa_interes(self) -> float:
        return self._tasa_interes

    def aplicar_corte_mensual(self) -> None:
        """
        Interés simple: saldo += saldo * tasa
        Nota: en sistemas reales hay más reglas, aquí es didáctico.
        """
        super().aplicar_corte_mensual()  # valida cuenta activa
        interes = self._saldo * self._tasa_interes
        if interes > 0:
            self._saldo += interes


class CuentaCorriente(CuentaBase):
    """
    Cuenta corriente:
    - Permite sobregiro hasta un cupo: saldo puede quedar negativo, >= -cupo
    - Puede cobrar cuota de manejo en el corte mensual
    """

    def __init__(self, titular: str, saldo_inicial: float = 0.0, cupo_sobregiro: float = 0.0, cuota_manejo: float = 0.0) -> None:
        super().__init__(titular=titular, saldo_inicial=saldo_inicial)

        self._cupo_sobregiro: float = float(cupo_sobregiro)
        if self._cupo_sobregiro < 0:
            raise ValueError("El cupo de sobregiro no puede ser negativo.")

        self._cuota_manejo: float = float(cuota_manejo)
        if self._cuota_manejo < 0:
            raise ValueError("La cuota de manejo no puede ser negativa.")

    @property
    def cupo_sobregiro(self) -> float:
        return self._cupo_sobregiro

    @property
    def cuota_manejo(self) -> float:
        return self._cuota_manejo

    def retirar(self, monto: float) -> None:
        """
        Override (sobrescritura):
        - Reusa validaciones comunes con super() (activa + monto>0)
        - Cambia la regla de fondos: permite saldo negativo hasta -cupo_sobregiro
        """
        self._asegurar_activa()
        monto = self._normalizar_monto(monto)

        nuevo_saldo = self._saldo - monto
        if nuevo_saldo < -self._cupo_sobregiro:
            raise ValueError("Excede el cupo de sobregiro permitido.")

        self._saldo = nuevo_saldo

    def aplicar_corte_mensual(self) -> None:
        """
        Cobra cuota de manejo si está activa.
        Si la cuota deja el saldo por debajo del cupo, se rechaza.
        """
        super().aplicar_corte_mensual()  # valida activa

        if self._cuota_manejo <= 0:
            return

        nuevo_saldo = self._saldo - self._cuota_manejo
        if nuevo_saldo < -self._cupo_sobregiro:
            raise ValueError("La cuota de manejo excede el cupo de sobregiro.")
        self._saldo = nuevo_saldo
