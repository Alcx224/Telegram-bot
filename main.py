from Token import *
from readstars import *
from rr import *
import telebot
from telebot.types import ForceReply

bot = telebot.TeleBot(TOKEN)
user={}

@bot.message_handler(commands=["start"])
def cmd_start(message):
    bot.send_message(message.chat.id, "Hola, Bienvenido a nuestro bot \nUtiliza /help "
                     "para ver los comandos que puedes utilizar.")

@bot.message_handler(commands=["help"])
def cmd_help(message):
    bot.send_message(message.chat.id, "Usa el comando: \n/constellation para iniciar "
                     "el modo de observación estelar \nUsa el comando"
                     " /rrnhccc para digitar una relación de recurrencia a resolver.")
        
    bot.send_message(message.chat.id, "Usa el comando:  \n/constellation <nombre de la constelación> "
                      "para ver la constelación dibujada en nuestra carta estelar o usa solo /constellation para ver"
                      " nuestro mapa sin ninguna constelación.")
    bot.send_message(message.chat.id, "Las constelaciones disponibles son: \n"
                     "Boyero, Casiopea, Cazo, Cygnet, Geminis, Hydra, OsaMayor y la OsaMenor. \n"
                     "Sí quieres ver todas las constelaciones dibujadas utiliza el argumento all.")

@bot.message_handler(commands=["constellation"])
def cmd_constellation(message):
    command, *parameters = message.text.split(' ')

    with open("./constellations/stars.txt", "r") as file:
        hd_dict, magnitude_dict, name_dict = read_coords(file)
        
    
    if len(parameters) == 0:
         stars_plot = stars_plotting(hd_dict, magnitude_dict)
         bot.send_message(message.chat.id, "Este es nuestro mapa estelar, échale un vistazo: ")
         bot.send_photo(message.chat.id, stars_plot)

    elif parameters[0] == "all":
        all_cons = read_all_constellation_lines("./constellations", "stars.txt")
        cons_plot = plot_constellation_lines(stars_plotting(hd_dict, magnitude_dict), hd_dict, all_cons, name_dict, "white")
        bot.send_message(message.chat.id, "Este es nuestro mapa estelar con todas nuestras constelaciones, " "échale un vistazo: ")
        bot.send_photo(message.chat.id, cons_plot)

    else:
        constellation_name = parameters[0]
        path = "./constellations/"+ constellation_name +".txt"
        with open(path, "r") as file:
            lines_dict = read_constellation_lines(file)
            
        cons_plot = plot_constellation_lines(stars_plotting(hd_dict, magnitude_dict), hd_dict, lines_dict, name_dict, "white")
        bot.send_message(message.chat.id, "Este es nuestro mapa estelar con la constelación "+ constellation_name + " échale un vistazo: ")
        bot.send_photo(message.chat.id, cons_plot)
        lines_dict ={}
        
    

@bot.message_handler(commands=["rrnhccc"])
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

    bot.set_my_commands([
        telebot.types.BotCommand("/start", "Inicia nuestro bot"),
        telebot.types.BotCommand("/help", "Cómo usar nuestros comandos"),
        telebot.types.BotCommand("/constellation", "Comando principal para nuestra carta estelar"),
        telebot.types.BotCommand("/rrnhccc", "Relaciones de recurrencia"),
    ])


    bot.infinity_polling()

