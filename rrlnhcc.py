import sympy as sp
import re
from sympy import Function, rsolve, Symbol


def sol_rrlnhcc(input_str):

    # Define la función f(n) simbólicamente
    f = Function('f')
    n = Symbol('n')

    try:
        # Divide la entrada y extrae los componentes de la recurrencia
        input_parts = input_str.replace(" ", "").split(",")
        indices_ant = [int(i) for i in re.findall(r"f\(n-(\d+)", input_parts[0][5:])]
        indices_ant.sort()  # Índices de los antecesores en f(n), orden ascendente
        
        # Crea un diccionario con las condiciones iniciales que se encuentran a partir de la posición 1 en la lista input_parts
        ci = {}
        for el in input_parts[1:]:
            ci[int(el[2:el.index(")")])] = sp.Rational(el[el.index("=")+1:])
        
        # Almacena f(n) recurrente en g
        g = sp.parse_expr(input_parts[0][5:] + "- f(n)")
        
        # rsolve() retorna la versión no recurrente de f(n)
        sol = rsolve(g, f(n), ci)
        
        # Construye la respuesta
        response = "La expresión cerrada para la secuencia no recurrente es: " + str(sol)
        
        # Calcula algunos términos de la secuencia
        sequence_values = [f"f({i}) = {sol.subs(n, i)}" for i in range(min(ci.keys()), max(ci.keys()) + 10)]
        
        return response, sequence_values
    except Exception as e:
        return str(e), None