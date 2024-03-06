print("\\n is a newline character")
print("\\\n is a newline character")

import re

texto = r"Esto es una barra invertida seguida de una nueva línea: \\ \n Esto está en la siguiente línea."
patron = r'\\\n'
coincidencias = re.findall(patron, texto)

print(coincidencias)
