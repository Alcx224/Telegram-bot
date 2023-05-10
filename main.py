from Token import *
from readstars import *
import telebot

bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=["start"])
def cmd_start(message):
    bot.send_message(message.chat.id, "Hola, Bienvenido a nuestro bot \nUtiliza /help para ver los comandos que puedes utilizar")

@bot.message_handler(commands=["help"])
def cmd_help(message):
    bot.send_message(message.chat.id, "Usa el comando /constelation para iniciar el modo de observación estelar \nUsa el comando /fgo para digitar la FGO a resolver")

@bot.message_handler(commands=["constellation"])
def cmd_constellation(message):
    picture = plot_background()
    with open("./constellations/stars.txt", "r") as file:
        hd_dict, magnitude_dict, name_dict = read_coords(file)
    starsplot = stars_plotting(picture, hd_dict, magnitude_dict)
    bot.send_message(message.chat.id, "Este es nuestro mapa estelar, échale un vistazo: ")
    bot.send_photo(message.chat.id, starsplot)

if __name__ == "__main__":
    print("Starting Bot")
    bot.infinity_polling()

