from telegram import Update
from telegram.ext import Application, CommandHandler
from markov import generate_text_hist
import sympy as sp
import re
from cifrado_cesar import cifrado_cesar


global gen_text
global hist
gen_text = ""
hist = None
TOKEN = "6434936644:AAGX-mGnmAhgYa_wtU4WJ4IvsBZceWSw2Gc"

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
    
    # arg contendrá las palabras que el usuario haya enviado después del comando /cifrado
    arg = update.message.text.split(" ")[1:]
    
    # Si el número de argumentos después de escribir el comando está entre 2 y 3, se asume que
    # estos argumentos corresponden a des, msj y desp (si se incluye)
    if 2 <= len(arg) <= 3:
        # Si solo da dos argumentos, se asume el desp por defecto 5
        if len(arg) == 2:
            arg.append("5")
            
        try:
            # Si desp no cumple el formato, se notifica al usuario del error
            if not arg[2].isdigit():
                raise Exception("'desp' debe ser un número entero positivo.")
            
            # Se realiza el cifrado/descifrado del msj
            if arg[0] == "cif":
                res = cifrado_cesar(arg[1], int(arg[2]), True)
            elif arg[0] == "des":
                res = cifrado_cesar(arg[1], int(arg[2]), False)
            else:
                # Si el argumento no está dentro de las opciones, se notifica al usuario
                raise Exception("Debe indicar 'des' para descifrar o 'cif' para cifrar.")
            
            # Se envía al usuario el mensaje resultante y el desplazamiento usado
            await update.message.reply_text(
                "Su mensaje cifrado con desplazamiento "+arg[2]+":\n"
                +res
            )
        except Exception as e:
            # Si ocurre algún error, se indica al usuario qué ocurrió
            await update.message.reply_text(
                "Cometió un error escribiendo el comando. Recuerde: "+str(e)
            )
    else:
        # En cualquier otro caso, se le indica al usuario cómo usar el comando
        await update.message.reply_text(
            "Para cifrar un mensaje, escriba '/cifrado cif msj desp'.\n"
            +"Para descifrar, escriba '/cifrado des msj desp'.\n"
            +"Reemplace 'msj' por el mensaje que desea cifrar/descifrar "
            +"y 'desp' por el desplazamiento a aplicar según el cifrado "
            +"césar. El desplazamiento es opcional, pero si no se ingresa, "
            +"se asumirá que desp = 5."
        )
        
async def markov_command(update, context): 
    """Función correspondiente al comando /markov"""
    global gen_text
    global hist
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
                gen_text = generate_text_hist(arg[0], arg[1], arg[2])
                # Se notifica al usuario de la generación exitosa del texto
                await update.message.reply_text("Su texto ficticio ha sido creado.")
            except Exception as e:
                # Si ocurre algún error, se indica al usuario qué ocurrió
                await update.message.reply_text(str(e))
        elif arg[0] == "hist":
            await context.bot.send_photo(chat_id=update.message.chat_id, photo=r"hist.png")
        elif arg[0] == "texto":
            # Se escribe al usuario el texto anteriormente generado almacenado en gen_text
            await update.message.reply_text(gen_text)
    
    if gen_text != "" and (len(arg) == 0 or (len(arg) > 0 and not arg[1] in ["hist", "texto"])):
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