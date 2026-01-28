# models/cuenta.py
from __future__ import annotations


class CuentaBancaria:
    """
    Cuenta bancaria simplificada con encapsulación y propiedades.

    Invariantes (reglas que siempre deben cumplirse):
    - saldo >= 0
    - titular no vacío
    - si la cuenta está cerrada, no se puede consignar/retirar
    """

    _next_id: int = 1  # contador didáctico para IDs

    def __init__(self, titular: str, saldo_inicial: float = 0.0) -> None:
        self._id: int = CuentaBancaria._next_id
        CuentaBancaria._next_id += 1

        # titular validado por property setter
        self._titular: str = ""
        self.titular = titular

        # saldo interno; se valida al asignar el saldo inicial
        self._saldo: float = 0.0
        self._set_saldo_inicial(saldo_inicial)

        self._activa: bool = True

    # -------------------------
    # Propiedades (API pública)
    # -------------------------
    @property
    def id(self) -> int:
        """ID de la cuenta (solo lectura)."""
        return self._id

    @property
    def titular(self) -> str:
        """Titular (lectura)."""
        return self._titular

    @titular.setter
    def titular(self, value: str) -> None:
        """Titular (escritura controlada) con validación."""
        if value is None:
            raise ValueError("El titular no puede ser None.")
        value = str(value).strip()
        if not value:
            raise ValueError("El titular no puede estar vacío.")
        self._titular = value

    @property
    def saldo(self) -> float:
        """
        Saldo (solo lectura desde fuera).
        La modificación debe pasar por consignar/retirar para proteger invariantes.
        """
        return self._saldo

    @property
    def activa(self) -> bool:
        """Indica si la cuenta está activa."""
        return self._activa

    # -------------------------
    # Métodos de negocio
    # -------------------------
    def consignar(self, monto: float) -> None:
        """Aumenta el saldo si la cuenta está activa y el monto es válido."""
        self._asegurar_activa()
        monto = self._normalizar_monto(monto)
        self._saldo += monto

    def retirar(self, monto: float) -> None:
        """Disminuye el saldo si hay fondos suficientes."""
        self._asegurar_activa()
        monto = self._normalizar_monto(monto)

        if monto > self._saldo:
            raise ValueError("Fondos insuficientes para realizar el retiro.")
        self._saldo -= monto

    def cerrar(self) -> None:
        """Cierra la cuenta. Una cuenta cerrada no permite operaciones."""
        self._activa = False

    # -------------------------
    # Internos (detalle)
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

    def __str__(self) -> str:
        estado = "activa" if self._activa else "cerrada"
        return (
            f"CuentaBancaria(id={self._id}, titular='{self._titular}', "
            f"saldo={self._saldo:.2f}, estado={estado})"
        )
