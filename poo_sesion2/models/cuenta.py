from __future__ import annotations

class CuentaBancaria:
    #Cuenta bancaria simplificada con encapsulación y propiedades.

    # Invariantes (reglas que siempre deben cumplirse):
    # - saldo >= 0
    # - titular no vacío
    # - si la cuenta está cerrada, no se puede consignar/retirar

    _next_id int = 1 #esto es didactico...

    def __init__(self, titular: str, saldo_inicial: float = 0.0) -> None:
        self._id: int = CuentaBancaria._next_id
        CuentaBancaria._next_id += 1

        # titular validado con una property de tipo setter.
        self._titular: str = ""
        self.titular = titular

        # saldo interno; se valida al asignar el saldo inicial

        self._saldo: float = 0.0
        self._set_saldo_incial(saldo_inicial)

        self._activa: bool = True
