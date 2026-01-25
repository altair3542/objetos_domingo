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

        # Propiedades (API pública)

        @property
        # id de solo lectura
        def id(self) -> int:
            return self._id

        @property
        def titular(self) -> str:
            # titular de solo lectura
            return self._titular

        @titular.setter
        def titular(self, value: str) -> None:
            # escritura controlada del titular
            if value is None:
                raise ValueError("El titular no puede estar None")
            value = str(value).strip()
            if not value:
                raise ValueError("El titular no puede estar Vacio")
            self._titular = value

        @property
        def saldo(self) -> float:
            # saldo que solo sea de lectura desde fuera.
            #la modificacion debe pasar unicamente por las funciones de consignar y retirar para proteger las reglas de negocio

            return self._saldo

        @property
        def activa(self) -> bool:
            # indicamos si la cuenta esta activa.
            return self._activa

    
