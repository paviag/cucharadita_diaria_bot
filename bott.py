from telegram import Update
from telegram.ext import Application, CommandHandler
from markov import generate_text


global gen_text
gen_text = ""
TOKEN = "6434936644:AAGX-mGnmAhgYa_wtU4WJ4IvsBZceWSw2Gc"

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
    alfabeto = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789_-.áéíóú?!¿¡'
    
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

async def start_command(update, context): 
    """Función correspondiente al comando /start"""
    await update.message.reply_text(
        "Hola"
    )
    
async def ayuda_command(update, context):
    """/ayuda"""
    await update.message.reply_text(
        "Lista de comandos disponibles:\n"
        +"/start - Mensaje de bienvenida.\n"
        +"/ayuda - Indica los comandos disponibles y su función.\n"
        +"/cifrado - \n"
        +"/markov - Permite generar textos con cadenas de Markov partiendo de una URL."
    )
    
async def cifrado_command(update, context): 
    """Función correspondiente al comando /cifrado"""
    await update.message.reply_text("cifrado")

async def markov_command(update, context): 
    """Función correspondiente al comando /markov"""
    global gen_text
    print(update.message)
    print(context.args)
    # arg contendrá las palabras que el usuario haya enviado después del comando /markov
    arg = update.message.text.split(" ")[1:]
    
    if gen_text == "" and len(arg) != 3:
        # Si no hay texto generado, y el usuario no dio indicaciones para generarlo,
        # se le indica cómo funciona el comando
        await update.message.reply_text(
            "No se ha generado ningún texto con cadenas de Markov aún.\n"
            +"Para la creación de un texto ficticio con cadenas de Markov, "
            +"debe ingresar junto al comando /markov: \n"
            +"- URL de un sitio web.\n"
            +"- El grado del modelo, K.\n"
            +"- El número de caracteres del texto resultante, N.\n"
            +"Escriba '/markov URL K N' para generar su texto.\n"
            +"Cuando ingrese el link, debe presionar la x para que no "
            +"envíe la previsualización."
        )
    elif len(arg) > 0:
        # Si el usuario ingreso alguna palabra tras el comando /markov, se verifican
        # para ejecutar las funciones de generar texto, mostrar histograma o mostrar texto
        if len(arg) == 3:
            # Si hay 3 palabras se asumen que son url, K, N y se trata de generar el texto
            try:
                # El texto se almacena en la variable global gen_text
                gen_text = generate_text(arg[0], arg[1], arg[2])
                # Se notifica al usuario de la generación exitosa del texto
                await update.message.reply_text("Su texto ficticio ha sido creado.")
            except Exception as e:
                # Si ocurre algún error, se indica al usuario qué ocurrió
                await update.message.reply_text(str(e))
        elif arg[0] == "hist":
            #await context.bot.send_photo(chat_id=update.message.chat_id, photo=r"filename")
            pass
        elif arg[0] == "texto":
            # Se escribe al usuario el texto anteriormente generado almacenado en gen_text
            await update.message.reply_text(gen_text)
    
    if gen_text != "" and (len(arg) == 0 or not arg[1] in ["hist", "texto"]):
        # Si ya fue generado texto anteriormente y el usuario no invocó las funciones
        # de mostrar histograma o texto, se le informa acerca de estas funciones
        await update.message.reply_text(
            "Se ha generado un texto ficticio con la URL dada.\n"
            +"Si desea visualizar el texto, escriba '/markov texto'.\n"
            +"Si desea visualizar el histograma de frecuencias de las "
            +"K-tuplas, escriba '/markov hist'.\n"
            +"Si desea generar un nuevo texto o cambiar los parámetros, "
            +"escriba '/markov URL K N' para generar su texto."
        )

async def error(update, context): 
    print(f"Update {update} caused error {context.error}")

def main():
    # Construye el bot
    app = Application.builder().token(TOKEN).build()
    # Añade comandos
    app.add_handler(CommandHandler("start", start_command)) 
    app.add_handler(CommandHandler("ayuda", ayuda_command)) 
    app.add_handler(CommandHandler("cifrado", cifrado_command)) 
    app.add_handler(CommandHandler("markov", markov_command))
    # Manejo de errores
    app.add_error_handler(error)
    # Run the bot until the user presses Ctrl-C
    app.run_polling(allowed_updates=Update.ALL_TYPES)
    
if __name__ == "__main__":
    main()