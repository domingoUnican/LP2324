import os
import re
import sys
import io
import traceback
from contextlib import redirect_stdout
# ¡from Base_clases import *

DIRECTORIO = os.path.expanduser("./")
sys.path.append(DIRECTORIO)

from Lexer import CoolLexer

PRACTICA = "04"  # Practica que hay que evaluar
DEBUG = True   # Decir si se lanzan mensajes de debug
NUMLINEAS = 3   # Numero de lineas que se muestran antes y después de la no coincidencia
sys.path.append(DIRECTORIO)
CALIFICACION = "grading"  # Para un reto mayor cambiar a "grading"
# CALIFICACION = "grading"
DIR = os.path.join(DIRECTORIO, PRACTICA, CALIFICACION)
FICHEROS = os.listdir(DIR)
TESTS = [fich for fich in FICHEROS
         if os.path.isfile(os.path.join(DIR, fich)) and
         re.search(r"^[a-zA-Z].*\.(cool|test|cl)$", fich)]
TESTS.sort()


if True:
    contador = len(TESTS)
    for fich in TESTS:
        lexer = CoolLexer()
        f = open(os.path.join(DIR, fich), 'r', newline='')
        g = open(os.path.join(DIR, fich + '.out'), 'r', newline='')
        if os.path.isfile(os.path.join(DIR, fich)+'.nuestro'):
            os.remove(os.path.join(DIR, fich)+'.nuestro')
        if os.path.isfile(os.path.join(DIR, fich)+'.bien'):
            os.remove(os.path.join(DIR, fich)+'.bien')
        if os.path.isfile(os.path.join(DIR, fich) + '.gen.py'):
            os.remove(os.path.join(DIR, fich) + '.gen.py')
        texto = ''
        entrada = f.read()
        f.close()
        if PRACTICA == '01':
            texto = '\n'.join(lexer.salida(entrada))
            texto = f'#name "{fich}"\n' + texto
            resultado = g.read()
            texto = re.sub(r'#\d+\b', '', texto)
            resultado = re.sub(r'#\d+\b', '', resultado)
            texto = re.sub(r'\s+\n', '\n', texto)
            resultado = re.sub(r'\s+\n', '\n', resultado)
            g.close()
            if texto.strip().split() != resultado.strip().split():
                print(f"Revisa el fichero {fich}")
                if DEBUG:
                    nuestro = [linea for linea in texto.split('\n') if linea]
                    bien = [linea for linea in resultado.split('\n') if linea]
                    linea = 0
                    f = open(os.path.join(DIR, fich)+'.nuestro', 'w')
                    g = open(os.path.join(DIR, fich)+'.bien', 'w')
                    f.write(texto.strip())
                    g.write(resultado.strip())
                    f.close()
                    g.close()
                    contador -= 1
        elif PRACTICA in ('02', '03'):
            from Parser import CoolParser
            parser = CoolParser()
            parser.nombre_fichero = fich
            parser.errores = []
            bien = ''.join([c for c in g.readlines() if c and '#' not in c])
            g.close()
            j = parser.parse(lexer.tokenize(entrada))
            try:
                if j and not parser.errores:
                    resultado = '\n'.join([c for c in j.str(0).split('\n')
                                           if c and '#' not in c])
                else:
                    resultado = '\n'.join(parser.errores)
                    resultado += '\n' + "Compilation halted due to lex and parse errors"
                if resultado.lower().strip().split() != bien.lower().strip().split():
                    print(f"Revisa el fichero {fich}")
                    if DEBUG:
                        f = open(os.path.join(DIR, fich)+'.nuestro', 'w')
                        g = open(os.path.join(DIR, fich)+'.bien', 'w')
                        f.write(resultado.strip())
                        g.write(bien.strip())
                        f.close()
                        g.close()
                        contador -= 1
            except Exception as e:
                print(f"Lanza excepción en {fich} con el texto {e}")
                contador -= 1
        elif PRACTICA == '04':
            from Parser import CoolParser
            parser = CoolParser()
            parser.nombre_fichero = fich
            parser.errores = []
            bien = g.read()
            g.close()
            j = parser.parse(lexer.tokenize(entrada))
            try:
                codigo = j.genera_codigo()
                if DEBUG:
                    with open(os.path.join(DIR, fich + '.gen.py'), 'w+') as d:
                        d.write(codigo)
                    with open(os.path.join(DIR, fich + '.parser.out'), 'w+') as pd:
                        pd.write(j.str(0))
                else:
                    os.remove(os.path.join(DIR, fich + '.gen.py'))
                    os.remove(os.path.join(DIR, fich + '.parser.out'))
                resultado = io.StringIO()
                print(f"Executing code for {fich}:")
                sys.stdout.flush()
                with redirect_stdout(resultado):
                    exec(codigo)
                resultado = resultado.getvalue()
                print(f"Result: \n{resultado}")
                if resultado.lower().strip().split() != bien.lower().strip().split():
                    print(f"✗ Revisa el fichero {fich}")
                    if DEBUG:
                        f = open(os.path.join(DIR, fich)+'.nuestro', 'w')
                        g = open(os.path.join(DIR, fich)+'.bien', 'w')
                        f.write(resultado.strip())
                        g.write(bien.strip())
                        f.close()
                        g.close()
                        contador -= 1
                else:
                    print(f"✓ Fichero correcto: {fich}")
            except Exception as e:
                print(f"✗ Lanza excepción en {fich} con el texto {e}")
                traceback.print_exception(e, file=sys.stdout)
                contador -= 1
    print(f'Ficheros correctos: {contador}/{len(TESTS)}')
