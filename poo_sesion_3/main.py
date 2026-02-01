# main.py
from services.banco_service import BancoService
from ui.consola import ConsolaBanco


def main() -> None:
    banco = BancoService()

    # Semilla didáctica
    banco.abrir_ahorros("Ana", 100000, 0.01)                 # 1% mensual
    banco.abrir_corriente("Carlos", 20000, 50000, 5000)      # cupo 50k, cuota 5k

    app = ConsolaBanco(banco)
    app.ejecutar()


if __name__ == "__main__":
    main()
