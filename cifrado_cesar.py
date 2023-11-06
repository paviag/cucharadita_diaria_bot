def cifrado_cesar(msj_ingresado, desp, cif):
    """
    Función que descifra o cifra un mensaje de acuerdo al cifrado César y el número de
    desplazamientos.
    
    Parámetros:
    msj_ingresado (str): El mensaje a cifrar/descifrar.
    desp (int): El número de desplazamientos.
    cif (boolean): True si se va a cifrar. False si se va a descifrar.
    """
    # Define el alfabeto
    alfabeto = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789_-.áéíóú?!¿¡"
    
    # Cambia el signo de la variable desp dependiendo si se va a hacer un desplazamiento
    # a la izquierda/negativo (descifrar) o a la derecha/positivo (cifrar)
    desp = desp if cif else -desp
    
    # Se inicializa el mensaje de salida como vacío
    msj_salida = ""
    
    # Se recorren los caracteres del mensaje ingresado
    for c in msj_ingresado:
        # Si el caractér está en el alfabeto, es cifrado/descifrado
        # sino, se añade al mensaje de salida tal como está
        if c in alfabeto:
            # id es la posición del caractér desplazado tantas unidades como 
            # indica desp
            id = alfabeto.index(c)+desp
            if id > len(alfabeto):
                id = id-len(alfabeto)
            # Se añade el caractér encontrado tras hacer el desplazamiento al 
            # mensaje de salida 
            msj_salida += alfabeto[id]
        else:
            msj_salida += c
    return msj_salida