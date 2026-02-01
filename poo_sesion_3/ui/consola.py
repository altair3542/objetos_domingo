# ui/consola.py
from __future__ import annotations

from services.banco_service import BancoService


class ConsolaBanco:
    def __init__(self, banco: BancoService) -> None:
        self._banco = banco

    def ejecutar(self) -> None:
        while True:
            self._menu()
            opcion = input("Opción: ").strip()

            try:
                if opcion == "1":
                    self._abrir_ahorros()
                elif opcion == "2":
                    self._abrir_corriente()
                elif opcion == "3":
                    self._listar()
                elif opcion == "4":
                    self._buscar()
                elif opcion == "5":
                    self._consignar()
                elif opcion == "6":
                    self._retirar()
                elif opcion == "7":
                    self._aplicar_corte()
                elif opcion == "8":
                    self._cerrar()
                elif opcion == "9":
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
        print("=== Banco - POO (Sesión 3) ===")
        print("1) Abrir cuenta AHORROS")
        print("2) Abrir cuenta CORRIENTE")
        print("3) Listar cuentas")
        print("4) Buscar por titular")
        print("5) Consignar")
        print("6) Retirar")
        print("7) Aplicar corte mensual a todas")
        print("8) Cerrar cuenta")
        print("9) Eliminar cuenta")
        print("0) Salir")

    def _abrir_ahorros(self) -> None:
        titular = input("Titular: ")
        saldo = float(input("Saldo inicial: "))
        tasa = float(input("Tasa interés (ej 0.01 = 1%): "))
        cuenta = self._banco.abrir_ahorros(titular, saldo, tasa)
        print("Cuenta creada:", cuenta)

    def _abrir_corriente(self) -> None:
        titular = input("Titular: ")
        saldo = float(input("Saldo inicial: "))
        cupo = float(input("Cupo sobregiro: "))
        cuota = float(input("Cuota manejo mensual: "))
        cuenta = self._banco.abrir_corriente(titular, saldo, cupo, cuota)
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

    def _aplicar_corte(self) -> None:
        self._banco.aplicar_corte_mensual_a_todas()
        print("Corte mensual aplicado.")

    def _cerrar(self) -> None:
        cuenta_id = int(input("ID cuenta: "))
        self._banco.cerrar_cuenta(cuenta_id)
        print("Cuenta cerrada.")

    def _eliminar(self) -> None:
        cuenta_id = int(input("ID cuenta: "))
        self._banco.eliminar_cuenta(cuenta_id)
        print("Cuenta eliminada.")
