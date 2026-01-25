# convenciones para el name mangling.

#publico:

# cuenta.consignar(50000)
# print(cuenta.titular)


#proteccion por convencion.
#self._saldo
#aqui podemos acceder, pero no se recomienda.

# privado por name mangling.

# py los renombra internamente...

# __saldo -> _NombreClase__saldo

class Demo:
    def __init__(self):
        self.__x = 10

d = Demo()
print([x for x in dir(d) if "x" in x])
print(d._Demo__x)

# __ no es seguridad: es una herramienta para evitar choques (especialmente con herencia) y desalentar acceso directo.


# @property: acceso “bonito” con control real

# Guardas el valor real en _saldo

# Expones saldo como propiedad solo lectura

# Modificas saldo únicamente con métodos consignar() / retirar()
