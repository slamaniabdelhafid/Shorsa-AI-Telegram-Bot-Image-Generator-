import telebot
from telebot import types
from nanoAPI import image_generator
from io import BytesIO
from PIL import Image
import requests
import base64
import sqlite3
from datetime import datetime
import json
from typing import Dict, List, Any
import os
from dotenv import load_dotenv


load_dotenv()

SECRET = os.getenv("bot")
bot = telebot.TeleBot(SECRET)
PAYMENT_PROVIDER_TOKEN= os.getenv("PAYMENT_PROVIDER_TOKEN")
INITIAL_FREE_CREDITS = 3

def create_user(user_id, username):
    conn = sqlite3.connect("fastapi_tortoiseorm/db.sqlite3")
    cursor = conn.cursor()
 
    try:
      
        prompts_remaining = INITIAL_FREE_CREDITS
        history = ''  
        first_time_connection = datetime.now().isoformat() 
        last_time_use = first_time_connection
        
        cursor.execute("""
            INSERT INTO users (id, username, prompts_remaining, first_time_connection, last_time_use)
            VALUES (?, ?, ?, ?, ?)
        """, (user_id, username, prompts_remaining, first_time_connection, last_time_use))

        conn.commit()  

    except sqlite3.Error as e:
        print(f"Error : {e}")
    finally:
        cursor.close()
        conn.close()



def add_user_history(db_path: str, user_id, history_entry: Dict[str, Any]) -> bool:
    """
    Ajoute une entrée d'historique pour un utilisateur spécifique.
    Version synchrone sans await.
    
    Args:
        db_path (str): Chemin vers la base de données SQLite
        user_id (int): ID de l'utilisateur
        history_entry (dict): Données d'historique à ajouter
    
    Returns:
        bool: True si l'opération a réussi, False sinon
    """
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    try:
        # 1. Vérifier si l'utilisateur existe dans la table users
        cursor.execute("SELECT username FROM users WHERE id = ?", (user_id,))
        user_result = cursor.fetchone()
        
        if not user_result:
            print(f"❌ Utilisateur avec ID {user_id} n'existe pas.")
            return False
        
        username = user_result[0]
        
        # 2. Vérifier si l'utilisateur a déjà un historique
        cursor.execute("SELECT id, history FROM history WHERE id = ?", (username,))
        history_result = cursor.fetchone()
        
        if history_result:
            # L'utilisateur a déjà un historique existant
            print("rani hna")
            history_id, existing_history = history_result
            print("rani hna2")
            # Convertir l'historique existant de JSON string à liste Python
            if existing_history:
                try:
                    history_list = json.loads(existing_history)
                    if not isinstance(history_list, list):
                        history_list = [history_list]
                except json.JSONDecodeError:
                    history_list = [existing_history]
            else:
                history_list = []
                print("rani hna3")
            
            # Ajouter la nouvelle entrée
            history_list.append(history_entry)
            
            # Mettre à jour l'historique dans la base de données
            cursor.execute("""
                UPDATE history 
                SET history = ? 
                WHERE id = ?
            """, (json.dumps(history_list), history_id))
            
            print(f"✅ Historique mis à jour pour l'utilisateur {username}")
            
        else:
            # Créer une nouvelle entrée d'historique
          
            history_list = [history_entry]
         
   
            cursor.execute("""
                INSERT INTO history (user_id ,history)
                VALUES (?, ?)
            """, (user_id,json.dumps(history_list, ensure_ascii=False)))
       
            print(f"✅ Nouvel historique créé pour l'utilisateur {username}")
        
        conn.commit()
        return True
        
    except sqlite3.Error as e:
        print(f"❌ Erreur SQLite: {e}")
        conn.rollback()
        return False
        
    except Exception as e:
        print(f"❌ Erreur: {e}")
        conn.rollback()
        return False
        
    finally:
        cursor.close()
        conn.close()




def user_exists(user_id):
    conn = sqlite3.connect("fastapi_tortoiseorm/db.sqlite3")
    cursor = conn.cursor()
    cursor.execute("SELECT 1 FROM users WHERE id = ?", (user_id,))
    exists = cursor.fetchone() is not None
    cursor.close()
    conn.close()
    return exists

@bot.message_handler(commands=['start'])
def start(message):
    if not user_exists(message.from_user.id):
        create_user(message.from_user.id,message.from_user.username)  
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton("About")
    btn2 = types.KeyboardButton('Help')
    btn3 = types.KeyboardButton("Credit")
    btn4 = types.KeyboardButton('Contact')
    btn5 = types.KeyboardButton('payment')
    markup.add(btn1, btn2, btn3 ,btn4 ,btn5)
    bot.send_message(message.from_user.id, "What do you want to create ?", reply_markup=markup)


def get_credits(user_id):
    conn = sqlite3.connect("fastapi_tortoiseorm/db.sqlite3")
    cursor = conn.cursor()
    cursor.execute(f"SELECT prompts_remaining FROM users WHERE id={user_id}")
    row = cursor.fetchone()
    cursor.close()
    conn.close()

    return row[0]
def get_credits_b(user_id):
    conn = sqlite3.connect("fastapi_tortoiseorm/db.sqlite3")
    cursor = conn.cursor()
    cursor.execute("SELECT prompts_remaining FROM users WHERE id=?",user_id)
    row = cursor.fetchone()
    cursor.close()
    conn.close()

    return row[0]

def counter(user_id, credits):
    conn = sqlite3.connect("fastapi_tortoiseorm/db.sqlite3")
    cursor = conn.cursor()
    credit=credits -1
    cursor.execute("UPDATE users SET prompts_remaining =? WHERE id=?",(credit,user_id))
    conn.commit() 
    cursor.close()
    conn.close()
   


@bot.message_handler(func=lambda message: message.text == "Credit")
def credit_action(message):
    user_id =  message.from_user.id,
    balance = get_credits_b(user_id=user_id)
    bot.send_message(message.from_user.id,f"You have {balance} credits.")

@bot.message_handler(func=lambda message: message.text == "About")
def about_action(message):
    bot.send_message(message.from_user.id,"""✨ About Shorsa AI

Shorsa AI is an advanced image-generation bot powered by the Sber GigaChat API.  
You can create any artwork by simply describing it with text.

Features:
• AI-generated images in seconds  
• Unlimited creativity  
• Simple and intuitive commands

Type /help to learn how to use the bot.
""")
 
@bot.message_handler(func=lambda message: message.text == "Help")
def help_action(message):
    bot.send_message(message.from_user.id,"""❓ Help — How to use Shorsa AI

To generate an image, just send me a message describing what you want.

Commands:
/start – Welcome message  
/help – Instructions  
/about – Info about the bot    
/credit – Check your credits  
/payment – Buy more credits  
/contact – Contact support

Example:
"Draw a futuristic city at night with neon lights"

""")
 

@bot.message_handler(func=lambda message: message.text == "Contact")
def contact_action(message):
    bot.send_message(message.from_user.id,"""📩 Contact Support

If you need help, collaboration, or have questions about Shorsa AI, feel free to reach out:

Developer: Slamani Abdelhafid   
Telegram: @M8oshin

We usually reply within 24 hours.

""")
###################################
# --- PAYMENT BUTTONS ---

@bot.message_handler(func=lambda message: message.text == "payment")
def payment_action(message):
    markup = types.InlineKeyboardMarkup()

    btn6 = types.InlineKeyboardButton("50 images - 500₽", callback_data="buy50")
    btn7 = types.InlineKeyboardButton("100 images - 850₽", callback_data="buy100")

    markup.add(btn6, btn7)

    bot.send_message(
        message.chat.id,
        "Choose your package:",
        reply_markup=markup
    )


# --- CALLBACK FOR PACKS ---
@bot.callback_query_handler(func=lambda call: call.data in ["buy50", "buy100"])
def pack_callback(call):
    bot.answer_callback_query(call.id)

    user_id = call.from_user.id
    data = call.data

    if data == "buy50":
        price = 50000      # Price in RUB kopeks (500₽)
        label = "Pack 50 images"
        payload = f"buy50-{user_id}"

    elif data == "buy100":
        price = 85000
        label = "Pack 100 images"
        payload = f"buy100-{user_id}"

    bot.send_invoice(
        chat_id=call.message.chat.id,
        title="Buy Credits",
        description=f"{label}",
        invoice_payload=payload,
        provider_token=PAYMENT_PROVIDER_TOKEN,
        currency="RUB",
        prices=[types.LabeledPrice(label, price)]
    )


# --- PRE CHECKOUT (REQUIRED) ---
@bot.pre_checkout_query_handler(func=lambda query: True)
def checkout(pre_checkout_query):
    bot.answer_pre_checkout_query(pre_checkout_query.id, ok=True)


# --- SUCCESSFUL PAYMENT ---
@bot.message_handler(content_types=['successful_payment'])
def successful_payment(message):
    payload = message.successful_payment.invoice_payload
    user_id = message.from_user.id

    if payload.startswith("buy50"):
        bot.send_message(user_id, "Payment successful! You received 50 images!")

    elif payload.startswith("buy100"):
        bot.send_message(user_id, "Payment successful! You received 100 images!")
###################################

@bot.message_handler(content_types=['text'])
def get_text_messages(message):

    _credits = get_credits(message.from_user.id)
    if _credits >0 :
        bot.send_message(message.chat.id, "your image being generated...")
        image_bytes = image_generator(message.text)
        counter(credits=_credits,user_id=message.from_user.id)
        if image_bytes:
            
            print(f"Debug: Type of image_bytes before BytesIO: {type(image_bytes)}")
          
            image_stream =  base64.b64decode(image_bytes.content)
            image_=Image.open(BytesIO(image_stream))
            bot.send_photo(message.chat.id, photo=image_)
            add_user_history(
                db_path="fastapi_tortoiseorm/db.sqlite3",
                user_id=message.from_user.id,  # Convertir en int explicite
                history_entry={
                    "timestamp": datetime.now().isoformat(),  # Clé d'abord
                    "message": message.text,                   # Valeur ensuite
                    "user_id": str(message.from_user.id),      # Stocker aussi comme string si besoin
                    "username": message.from_user.username if message.from_user.username else "unknown"
                }
            )
        else:
            bot.send_message(message.chat.id, "Désolé, je n'ai pas pu générer l'image ou la récupérer.")
        if message.text == 'hello':
            bot.send_message(message.from_user.id, '❓ Задайте интересующий вас вопрос')
    else :
      
        bot.send_message(message.chat.id, "Sorry!, You don't have enought credits....click on /payment to get unlimited credit for free")

bot.polling(none_stop=True, interval=0)