from __future__ import annotations

from typing import List, Optional
from models.cuenta import CuentaBancaria

class BancoService:
    #   Capa de servicios:
    # - Mantiene colecciones de objetos (cuentas)
    # - Orquesta operaciones de aplicación (búsqueda, CRUD, movimientos)
    # - Evita que la UI manipule listas o reglas directamente

    def __init__(self) -> None:
        self._cuentas: List[CuentaBancaria] = []

    # CRUD / Consultas...
    def abrir_cuenta(self, titular: str, saldo_inicial: float = 0.0) -> CuentaBancaria:
        cuenta = CuentaBancaria(titular=titular, saldo_inicial=saldo_inicial)
        self._cuentas.append(cuenta)
        return cuenta

    def listar_cuentas(self) -> List[CuentaBancaria]:
        # devuelve una copia del arreglo para no exponer la lista interna real
        return list(self._cuentas)

    def buscar_por_id(self, cuenta_id: int) ->Optional[CuentaBancaria]:
        return next((c for c in self._cuentas if c.id == cuenta_id), None)


    def buscar_por_titular(self, texto:str) -> List[CuentaBancaria]:
        texto = str(texto).strip().lower()
        if not texto:
            return []
        return [c for c in self._cuentas if texto in c.titular.lower()]

    def cambiar_titular(self, cuenta_id: int, nuevo_titular: str) -> None:
        cuenta = self.obtener_o_fallar(cuenta_id)
        cuenta.titular = nuevo_titular #setter con validacion

    
