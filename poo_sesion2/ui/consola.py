# ui/consola.py
from __future__ import annotations

from services.banco_service import BancoService


class ConsolaBanco:
    """
    UI de consola:
    - No debe contener lógica de negocio compleja
    - Solo leer entradas, llamar al servicio, mostrar resultados
    """

    def __init__(self, banco: BancoService) -> None:
        self._banco = banco

    def ejecutar(self) -> None:
        while True:
            self._menu()
            opcion = input("Opción: ").strip()

            try:
                if opcion == "1":
                    self._abrir()
                elif opcion == "2":
                    self._listar()
                elif opcion == "3":
                    self._buscar()
                elif opcion == "4":
                    self._consignar()
                elif opcion == "5":
                    self._retirar()
                elif opcion == "6":
                    self._cambiar_titular()
                elif opcion == "7":
                    self._cerrar()
                elif opcion == "8":
                    self._eliminar()
                elif opcion == "0":
                    print("Saliendo...")
                    break
                else:
                    print("Opción inválida.")
            except ValueError as e:
                print(f"Error: {e}")

            print()

    def _menu(self) -> None:
        print("=== Banco - POO (Sesión 2) ===")
        print("1) Abrir cuenta")
        print("2) Listar cuentas")
        print("3) Buscar por titular")
        print("4) Consignar")
        print("5) Retirar")
        print("6) Cambiar titular")
        print("7) Cerrar cuenta")
        print("8) Eliminar cuenta")
        print("0) Salir")

    def _abrir(self) -> None:
        titular = input("Titular: ")
        saldo = float(input("Saldo inicial: "))
        cuenta = self._banco.abrir_cuenta(titular, saldo)
        print("Cuenta creada:", cuenta)

    def _listar(self) -> None:
        cuentas = self._banco.listar_cuentas()
        if not cuentas:
            print("No hay cuentas.")
            return
        for c in cuentas:
            print(c)

    def _buscar(self) -> None:
        texto = input("Texto a buscar (titular): ")
        resultados = self._banco.buscar_por_titular(texto)
        if not resultados:
            print("Sin resultados.")
            return
        for c in resultados:
            print(c)

    def _consignar(self) -> None:
        cuenta_id = int(input("ID cuenta: "))
        monto = float(input("Monto: "))
        self._banco.consignar(cuenta_id, monto)
        print("Consignación OK.")

    def _retirar(self) -> None:
        cuenta_id = int(input("ID cuenta: "))
        monto = float(input("Monto: "))
        self._banco.retirar(cuenta_id, monto)
        print("Retiro OK.")

    def _cambiar_titular(self) -> None:
        cuenta_id = int(input("ID cuenta: "))
        nuevo = input("Nuevo titular: ")
        self._banco.cambiar_titular(cuenta_id, nuevo)
        print("Titular actualizado.")

    def _cerrar(self) -> None:
        cuenta_id = int(input("ID cuenta: "))
        self._banco.cerrar_cuenta(cuenta_id)
        print("Cuenta cerrada.")

    def _eliminar(self) -> None:
        cuenta_id = int(input("ID cuenta: "))
        self._banco.eliminar_cuenta(cuenta_id)
        print("Cuenta eliminada.")
