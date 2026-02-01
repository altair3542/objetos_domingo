# services/banco_service.py
from __future__ import annotations

from typing import List, Optional

from models.cuentas import CuentaBase, CuentaAhorros, CuentaCorriente


class BancoService:
    """
    Servicio de aplicación:
    - Mantiene una colección heterogénea: List[CuentaBase]
    - Usa polimorfismo: llama métodos comunes sin preguntar el tipo
    """

    def __init__(self) -> None:
        self._cuentas: List[CuentaBase] = []

    # -------------------------
    # Creación de cuentas
    # -------------------------
    def abrir_ahorros(self, titular: str, saldo_inicial: float = 0.0, tasa_interes: float = 0.01) -> CuentaAhorros:
        cuenta = CuentaAhorros(titular=titular, saldo_inicial=saldo_inicial, tasa_interes=tasa_interes)
        self._cuentas.append(cuenta)
        return cuenta

    def abrir_corriente(
        self,
        titular: str,
        saldo_inicial: float = 0.0,
        cupo_sobregiro: float = 0.0,
        cuota_manejo: float = 0.0,
    ) -> CuentaCorriente:
        cuenta = CuentaCorriente(
            titular=titular,
            saldo_inicial=saldo_inicial,
            cupo_sobregiro=cupo_sobregiro,
            cuota_manejo=cuota_manejo,
        )
        self._cuentas.append(cuenta)
        return cuenta

    # -------------------------
    # Consultas / CRUD
    # -------------------------
    def listar_cuentas(self) -> List[CuentaBase]:
        return list(self._cuentas)

    def buscar_por_id(self, cuenta_id: int) -> Optional[CuentaBase]:
        return next((c for c in self._cuentas if c.id == cuenta_id), None)

    def buscar_por_titular(self, texto: str) -> List[CuentaBase]:
        texto = str(texto).strip().lower()
        if not texto:
            return []
        return [c for c in self._cuentas if texto in c.titular.lower()]

    def cambiar_titular(self, cuenta_id: int, nuevo_titular: str) -> None:
        cuenta = self._obtener_o_fallar(cuenta_id)
        cuenta.titular = nuevo_titular

    def cerrar_cuenta(self, cuenta_id: int) -> None:
        cuenta = self._obtener_o_fallar(cuenta_id)
        cuenta.cerrar()

    def eliminar_cuenta(self, cuenta_id: int) -> None:
        cuenta = self._obtener_o_fallar(cuenta_id)
        self._cuentas.remove(cuenta)

    # -------------------------
    # Operaciones
    # -------------------------
    def consignar(self, cuenta_id: int, monto: float) -> None:
        cuenta = self._obtener_o_fallar(cuenta_id)
        cuenta.consignar(monto)

    def retirar(self, cuenta_id: int, monto: float) -> None:
        cuenta = self._obtener_o_fallar(cuenta_id)
        # Polimorfismo: si es Ahorros usa retirar base; si es Corriente usa override
        cuenta.retirar(monto)

    def aplicar_corte_mensual_a_todas(self) -> None:
        """
        Polimorfismo puro: mismo mensaje, distintas implementaciones.
        """
        for cuenta in self._cuentas:
            cuenta.aplicar_corte_mensual()

    # -------------------------
    # Duck typing (demostración)
    # -------------------------
    def retirar_generico(self, objeto_con_retirar, monto: float) -> None:
        """
        Duck typing:
        - No exigimos que sea CuentaBase.
        - Solo exigimos que tenga un método retirar(monto).
        """
        if not hasattr(objeto_con_retirar, "retirar"):
            raise ValueError("El objeto no soporta retirar(monto).")
        objeto_con_retirar.retirar(monto)

    # -------------------------
    # Internos
    # -------------------------
    def _obtener_o_fallar(self, cuenta_id: int) -> CuentaBase:
        cuenta = self.buscar_por_id(cuenta_id)
        if cuenta is None:
            raise ValueError(f"No existe una cuenta con id={cuenta_id}.")
        return cuenta
