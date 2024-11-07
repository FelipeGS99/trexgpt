import openai
import telebot
from dotenv import load_dotenv
import os

load_dotenv()

openai.api_key = os.getenv('openai_key')
bot = telebot.TeleBot(os.getenv('telegram_key'))
lista_mensagens = []

def enviar_mensagem(mensagem, lista_mensagens=[]):
    lista_mensagens.append({"role": "user", "content": mensagem})
    resposta = openai.chat.completions.create(model='gpt-4o', messages=lista_mensagens)
    return resposta.choices[0].message.content

@bot.message_handler(func=lambda message: True)
def responder_mensagem(message):
    chat_id = message.chat.id
    texto_recebido = message.text

    resposta_chatgpt = enviar_mensagem(texto_recebido, lista_mensagens)

    lista_mensagens.append({"role": "assistant", "content": resposta_chatgpt})
    
    bot.send_message(chat_id, resposta_chatgpt)
bot.polling()