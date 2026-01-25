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

    # metodos de negocio
    def consignar(self, monto: float) -> None:
        # aumentar el saldo de la cuenta si esta está activa y el monto es valido
        self._asegurar_activa()
        monto = self._normalizar_monto(monto)
        self._saldo += monto

    def retirar(self, monto: float) -> None:
        self._asegurar_activa()
        monto = self._normalizar_monto(monto)

        if monto > self._saldo:
            raise ValueError("paila, no tiene saldo")
        self._saldo -= monto


    def cerrar(self) -> None:
        #Cerrar la cuenta, no va a permitir mas operaciones.
        self._activa = False

    # metodos auxiliares de detalle.

    def _set_saldo_inicial(self, saldo_inicial: float) -> None:
        saldo_inicial = float(saldo_inicial)
        if saldo_inicial < 0:
            raise ValueError("usted que piensa de la vida?, el inicial no puede ser una deuda.")
        self._saldo = saldo_inicial

    def _normalizar_monto(self, monto: float) -> float:
        monto = float(monto)
        if monto <= 0:
            raise ValueError("el monto debe ser mayor que cero")
        return monto

    def _asegurar_activa(self) -> None:
        if not self._activa:
            raise ValueError("no podemos operar sobre una cuenta inactiva")

    def __str__(self) -> str:
        estado = "activa" if self._activa else "cerrada"
        return (
            f"CuentaBancaria(id={self._id}, titular='{self._titular}')"
            f"Saldo={self._saldo:.2f}, estado={estado}"
        )
