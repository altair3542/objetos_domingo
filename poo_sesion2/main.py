# main.py
from services.banco_service import BancoService
from ui.consola import ConsolaBanco


def main() -> None:
    banco = BancoService()

    # Datos semilla (para demo rápida en clase)
    banco.abrir_cuenta("Ana", 100000)
    banco.abrir_cuenta("Carlos", 50000)

    app = ConsolaBanco(banco)
    app.ejecutar()


if __name__ == "__main__":
    main()
