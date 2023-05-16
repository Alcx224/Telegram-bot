from Token import *
from readstars import *
from rr import *
import telebot
from telebot.types import ForceReply

bot = telebot.TeleBot(TOKEN)
user={}

@bot.message_handler(commands=["start"])
def cmd_start(message):
    bot.send_message(message.chat.id, "Hola, Bienvenido a nuestro bot \nUtiliza /help para ver los comandos que puedes utilizar")

@bot.message_handler(commands=["help"])
def cmd_help(message):
    bot.send_message(message.chat.id, "Usa el comando /constellation para iniciar el modo de observación estelar \nUsa el comando /recurrency para digitar una relación de recurrencia a resolver")

@bot.message_handler(commands=["constellation"])
def cmd_constellation(message):
    picture = plot_background()
    with open("./constellations/stars.txt", "r") as file:
        hd_dict, magnitude_dict, name_dict = read_coords(file)
    starsplot = stars_plotting(picture, hd_dict, magnitude_dict)
    bot.send_message(message.chat.id, "Este es nuestro mapa estelar, échale un vistazo: ")
    bot.send_photo(message.chat.id, starsplot)

@bot.message_handler(commands=["recurrency"])
def g_n(message):
    markup=ForceReply()
    msg = bot.send_message(message.chat.id, "Ingresa tú g(n)", reply_markup=markup)
    bot.register_next_step_handler(msg, coeff)

def coeff(message):
    markup=ForceReply()
    user[message.chat.id] = {}
    user[message.chat.id]["gn"] = message.text
    msg = bot.send_message(message.chat.id, "Ingresa tus coeficientes separados por coma", reply_markup=markup)
    bot.register_next_step_handler(msg, initcond)
    
def initcond(message):
    markup=ForceReply()
    user[message.chat.id]["Coeff"] = message.text
    msg = bot.send_message(message.chat.id, "Ingresa los casos iniciales", reply_markup=markup)
    bot.register_next_step_handler(msg, lastdata)

def lastdata(message):
    user[message.chat.id]["init"] = message.text
    to_g = user[message.chat.id]["gn"]
    
    to_f_coeffs = user[message.chat.id]["Coeff"]
    to_f_coeffs= list(map(int, to_f_coeffs.split(",")))
    to_initial_conditions = user[message.chat.id]["init"]
    to_initial_conditions = list(map(int, to_initial_conditions.split(",")))
    g, f_coeffs, initial_conditions = getvalues(to_g, to_f_coeffs, to_initial_conditions)
    bot.send_message(message.chat.id,"Tú recurrencia es: ")
    bot.send_message(message.chat.id, solve_recurrence(g, f_coeffs, initial_conditions))

if __name__ == "__main__":
    print("Starting Bot")
    bot.infinity_polling()

