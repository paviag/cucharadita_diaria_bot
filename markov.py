import numpy as np
import re
import requests
import ssl
import nltk
from nltk.util import ngrams
from pandas import Series
from matplotlib.pyplot import subplots
from bs4 import BeautifulSoup
from bs4.element import Comment


try:
    _create_unverified_https_context = ssl._create_unverified_context
except AttributeError:
    pass
else:
    ssl._create_default_https_context = _create_unverified_https_context

nltk.download("punkt")

def get_hist(texto, K):
    """
    Retorna un histograma de las 10 K-tuplas más repetidas en el texto con sus
    frecuencias.
    
    Parámetros:
    texto (str): Texto de donde se extraen las K-tuplas.
    K (int): Grado del modelo de Markov.
    """
    
    token = [c for c in texto]
    top10 = nltk.FreqDist(dict(nltk.FreqDist(ngrams(token, K)).most_common(n=10)))
    top10 = Series(dict(top10))
    fig, ax = subplots(figsize=(10,10))
    top10.plot(
      kind="hist",
      title=f"Frecuencia de las {K}-tuplas",
      xlabel="Tuplas",
      ylabel="Frecuencia",
      ax=ax,
    )
    ax.set_xticklabels(["".join(k) for k in top10.keys()])
    fig.tight_layout()
    return fig

def tag_visible(element):
    """
    Tomado de https://stackoverflow.com/questions/1936466/how-to-scrape-only-visible-webpage-text-with-beautifulsoup
    Verifica si el elemento de la página corresponde a texto plano (True) o no (False)
    """

    if element.parent.name in ['style', 'script', 'head', 'title', 'meta', '[document]']:
        return False
    if isinstance(element, Comment):
        return False
    return True

def get_next_char(prev, text, K):
    """
    Obtiene el siguiente caractér usando un modelo de la cadena de Markov de orden
    K, tomando a prev como los K caractéres predecesores y text como el texto base.
    
    Parámetros:
    prev (str): Cadena anterior.
    text (str): Texto base.
    K (int): Orden del modelo.
    """

    # g contendrá todos los caracteres que le siguen a prev; los candidatos para siguiente caractér.
    # Los valores corresponderán a la probabilidad de que la respectiva llave
    # sea el siguiente caractér.
    g = {}
    t = text
    prev = prev.lower()

    if K > 0 and (prev in t.lower() and t.lower()[-K:]!=prev):
        while t:
            try:
                # Se obtiene la posición de prev en el texto t
                ind = t.lower().index(prev)
                if ind+K >= len(t):
                    break
            except:
                break
            # Se obtiene el caractér que le sigue a prev en el texto t
            char = t[ind+K]
            # Si el carácter no está en g, se añade con valor de 1. Si sí lo está, se
            # aumenta su valor en 1. Así se llevará cuenta del número de ocurrencias
            if char not in g:
                g[char] = 1
            else:
                g[char] += 1
            t = t[ind+1:]
    else:
        # En caso de K=0 o que prev no esté en el texto, el siguiente caractér es
        # escogido aleatoriamente de acuerdo a su probabilidad de estar en el texto
        for char in t:
            # Si el carácter no está en g, se añade con valor de 1. Si sí lo está, se
            # aumenta su valor en 1. Así se llevará cuenta del número de ocurrencias
            if char not in g:
                g[char] = 1
            else:
                g[char] += 1

    # Se obtiene la suma de los pesos de todas sus aristas
    total = sum([i for i in g.values()])
    # Se divide el peso de cada arista entre esta suma de modo que ahora
    # corresponda no al número de veces, sino al porcentaje de veces (probabilidad)
    for char in g:
        g[char] /= total

    choice_char = np.random.choice(list(g.keys()), 1, p=list(g.values()))[0]
    if prev[-1].isupper() or prev[-2:] in ['. ','! ','? '] or prev[-1] in "¿¡":
        return choice_char.upper()
    if prev[-1].islower():
        return choice_char.lower()
    return choice_char

def adjust_text(text):
    """
    Retorna el texto modificado, habiendo eliminado caractéres que pudieran
    dificultar la creación de un texto ficticio comprensible como signos mal
    espaciados, espacios contiguos, saltos de línea y comillas.
    
    Parámetros:
    text (str): Texto original.
    """

    text = re.sub(r'\s([?.!”](?:\s|$))', r'\1', text)
    text = re.sub(r'(¿|¡|#|“)(\s)([a-zA-Z0-9])', r'\1\3', text)
    text = re.sub(r'((\n)+\s(\n)+)|(\s)+(\n)+(\s)+|\s+', r' ', text)
    return text if text[0]!=' ' else text[1:]

def generate_text_hist(url, K, N):
    """
    Genera un texto ficticio partiendo de una url utilizando un modelo de cadenas
    de Markov y un histograma con las frecuencias de las K-tuplas en el mismo.
    Retorna el texto.
    
    Parámetros:
    url (str): Url del texto original.
    K (str): Orden K del modelo de Markov.
    N (str): Longitud en caractéres del texto resultante.
    """
    if not (K.isdigit() and N.isdigit()):
        raise Exception("K y N deben ser números.")
    K, N = int(K), int(N)
    
    if K > N:
        raise Exception("N debe ser mayor a K.")   

    try:
        response = requests.get(url)
    except:
        raise Exception("No pudo accederse a la URL.")
    
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # Se obtiene el texto plano de la página filtrando aquellos elementos de estilo y script
    text = u' '.join(t.strip() for t in filter(tag_visible, soup.findAll(string=True)))

    # Se modifica el texto eliminando caractéres que puedan dificultar la creación
    # del texto ficticio como signos mal espaciados, espacios contiguos, saltos
    # de línea y comillas
    text = adjust_text(text)

    # El texto inicia con los primeros K caracteres del texto original
    st = text[:K]

    # Se añadirán nuevos caractéres hasta alcanzar N, como ya van K, entonces
    # el ciclo se repite N-K veces
    for i in range(N-K):
        nc = get_next_char(st[-K:], text, K)
        st += nc
    
    # Se guarda el histograma como hist.png
    get_hist(st, K).savefig("hist.png", dpi=100)
    
    # Se retorna el texto resultado
    return st
