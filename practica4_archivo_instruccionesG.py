# practica4_archivo_instruccionesG.py
import turtle as t
import math



# Configuración ventana 600x600
t.bgcolor("lightgray")
t.setup(600, 600)
t.title("Práctica 4 - Dibujante desde archivo")
t.speed(0)        # rapidez máxima para dibujar
t.hideturtle()

def teleport(x: float, y: float) -> None:
    t.penup()
    t.goto(x, y)
    t.pendown()

def cuadrado(lado: float) -> None:
    for _ in range(4):
        t.forward(lado)
        t.left(90)

def triangulo(lado: float) -> None:
    for _ in range(3):
        t.forward(lado)
        t.left(120)

def circulo(radio: float) -> None:
    # Aproximación poligonal como en tu práctica 1
    num_lados = 360
    avance = (2 * math.pi * radio) / num_lados
    angulo = 360 / num_lados
    for _ in range(num_lados):
        t.forward(avance)
        t.left(angulo)

def linea(longitud: float) -> None:
    t.forward(longitud)

def setheading(angle: float) -> None:
    t.setheading(angle)

# Validación: instrucción -> (número_de_parametros_necesarios, función)
VALID = {
    "CUADRADO": (1, cuadrado),
    "TRIANGULO": (1, triangulo),
    "CIRCULO": (1, circulo),
    "TELEPORT": (2, teleport),
    "LINEA": (1, linea),
    "SETHEADING": (1, setheading),
}

def parse_number(s: str) -> float:
    try:
        return float(s)
    except ValueError:
        raise ValueError(f"'{s}' no es un número válido")

archivo = "dibujante.txt"
with open(archivo, "r", encoding="utf-8") as f:
    lines = [ln.rstrip("\n") for ln in f]

# Si la primera instrucción real NO es TELEPORT, replicamos tu acomodo inicial
first_instr = None
for ln in lines:
    s = ln.strip()
    if not s or s.startswith("#"):
        continue
    first_instr = s.split()[0].upper()
    break

if first_instr != "TELEPORT":
    teleport(-300, 0)

# Ejecutar líneas
for lineno, ln in enumerate(lines, start=1):
    raw = ln.strip()
    if not raw or raw.startswith("#"):
        continue
    parts = raw.split()
    instr = parts[0].upper()

    if instr not in VALID:
        print(f"⚠️ Línea {lineno}: instrucción inválida -> {raw}")
        continue

    expected_args, func = VALID[instr]

    # detectar color opcional: si hay al menos expected_args + 2 tokens, último es color
    color = None
    if len(parts) >= expected_args + 2:
        color = parts[-1]

    if len(parts) - 1 < expected_args:
        print(f"⚠️ Línea {lineno}: faltan parámetros -> {raw}")
        continue

    # aplicar color temporalmente si se dio
    old_color = t.pencolor()
    if color:
        try:
            t.pencolor(color)
        except Exception as e:
            print(f"⚠️ Línea {lineno}: color inválido '{color}' ({e}). Manteniendo color anterior.")

    try:
        if instr == "TELEPORT":
            x = parse_number(parts[1])
            y = parse_number(parts[2])
            func(x, y)
        else:
            val = parse_number(parts[1])
            func(val)
    except Exception as e:
        print(f"⚠️ Línea {lineno}: error ejecutando '{instr}' -> {e}")

    # restaurar color anterior
    t.pencolor(old_color)

t.done()
