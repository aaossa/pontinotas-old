from html2text import HTML2Text


def generador_lineas(text):
    s = ''
    text = text + '\n'
    for char in text:
        if char == "\n":
            if len(s) > 1:
                yield s
            s = ''
        else:
            s = s + char
    yield None


class FichaAcademica:

    def __init__(self):
        """ La idea es poder ir organizando la informacion
        de una forma ordenada para retornarla como diccionario
        y facilitar su paso a json """
        # Carrera
        self.Programa = ''
        self.Escuela = ''
        self.Carrera = ''
        # Alumno
        self.Datos = []
        # Tiempo
        self.Tiempo = None
        # Semestres
        self.Semestres = []
        self.Pendientes = []
        # Totales
        self.Totales_periodo = {}
        self.Totales_acumulado = {}
        self.Totales_hist_acad = {}


def getDict(respuesta):

    # Aqui se obtiene el html y se obtiene el texto plano
    N = respuesta.text
    H = HTML2Text()
    clean_text = H.handle(N)

    # Se instancia el generador de lineas de texto
    lineas = generador_lineas(clean_text)
    Ficha = FichaAcademica()
    in_cursos_en_progreso = False

    while True:
        linea = next(lineas)

        # Fin de generador
        if not linea:
            break

        # Nombre, rut y  tiempo
        elif linea.startswith("|  ;  |"):
            Ficha.Datos = next(lineas).replace("|", " ").split(" ", 1)
            Ficha.Tiempo = next(lineas)

        # Programa, escuela y carrera
        elif linea == "Carrera Principal  ":
            Ficha.Programa = next(lineas).split(" | ")[1]
            Ficha.Escuela = next(lineas).split(" | ")[1]
            Ficha.Carrera = next(lineas).split(" | ")[1]

        # Detectar barrera de cursos en progreso
        elif linea.startswith("CURSOS EN PROGRESO"):
            in_cursos_en_progreso = True

        # Semestres completados
        elif linea.startswith("Periodo: ") and not in_cursos_en_progreso:

            # Se inicia un nuevo semestre
            Ficha.Semestres.append({linea: []})

            next(lineas)
            next(lineas)

            # Se guardan cursos hasta encontrar la tabla de totales del periodo
            sub_linea = next(lineas)[:-2]
            while not sub_linea.startswith("Totales") and not sub_linea.startswith("!"):
                if sub_linea[0].isdigit():
                    Ficha.Semestres[-1][linea][-
                                               1].append(sub_linea[:sub_linea.find(" ")])
                    Ficha.Semestres[-1][linea][-
                                               1].extend(next(lineas)[:-2].split("|")[:2])
                else:
                    Ficha.Semestres[-1][linea].append(sub_linea.split(" | "))
                sub_linea = next(lineas)[:-2]

            next(lineas)
            next(lineas)
            next(lineas)

            # Totales periodo
            Ficha.Totales_periodo[linea] = []
            for l in range(6):
                Ficha.Totales_periodo[linea].append(
                    next(lineas).replace("|", "").replace(" ", ""))

            next(lineas)

            # Totales acumulado
            Ficha.Totales_acumulado[linea] = []
            for l in range(6):
                Ficha.Totales_acumulado[linea].append(
                    next(lineas).replace("|", "").replace(" ", ""))

        # Cursos en progreso
        elif linea.startswith("Periodo: ") and in_cursos_en_progreso:

            # Iniciamos un nuevo semestre
            Ficha.Pendientes.append({linea: []})

            next(lineas)

            # Guardamos los cursos en su semestre correspondiente
            sub_linea = next(lineas)[:-2]
            while not sub_linea.startswith("Totales") and not sub_linea.startswith("!") and not len(sub_linea) == 0:
                try: 
                    if sub_linea[0].isdigit():
                        Ficha.Pendientes[-1][linea][-
                                                    1].append(sub_linea[:sub_linea.find(" ")])
                    else:
                        Ficha.Pendientes[-1][linea].append(sub_linea.split(" | "))
                    sub_linea = next(lineas)[:-2]
                except:
                    pass

        # Totales historial academico
        elif linea.startswith("TOTALES HIST ACAD (PREGRADO)"):
            next(lineas)
            next(lineas)
            for i in range(3):
                sub_linea = next(lineas).replace(": |", "")
                Ficha.Totales_hist_acad[sub_linea] = []
                for i in range(6):
                    Ficha.Totales_hist_acad[sub_linea].append(
                        next(lineas).replace("|", "").replace(" ", ""))

        # Queda pendiente el historial academico para posgrado

    return Ficha.__dict__
