class CuentaBancaria:


    def __init__(self, titular: str, saldo_inicial: float = 0.0) -> None:

        if saldo_inicial < 0:
            raise ValueError("El saldo inicial no puede ser negativo.")

        self.titular = titular
        self.saldo = float(saldo_inicial)

    def consignar(self, monto: float) -> None:

        monto = float(monto)
        if monto <= 0:
            raise ValueError("El monto a consignar debe ser mayor que 0.")

        self.saldo += monto

    def retirar(self, monto: float) -> None:

        monto = float(monto)
        if monto <= 0:
            raise ValueError("El monto a retirar debe ser mayor que 0.")

        if monto > self.saldo:
            raise ValueError("Fondos insuficientes para realizar el retiro.")

        self.saldo -= monto

    def __str__(self) -> str:
        """
        Representación legible del objeto (para humanos).
        Útil en depuración y salida en consola.
        """
        return f"CuentaBancaria(titular='{self.titular}', saldo={self.saldo:2f})"



###########################################################################

cuenta_ana = CuentaBancaria("Yolima, 100000")

print(cuenta_ana)

cuenta_ana.consignar(50000)
print("luego de consignar", cuenta_ana)

cuenta_ana.retirar(30000)
print("Luego de retirar:", cuenta_ana)

try:
    cuenta_ana.retirar(999999)
except ValueError as e:
    print("Error controlado:", e)
