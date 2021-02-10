import requests

def telegram_bot_sendtext(bot_message):

   bot_token = '1647175637:AAHAZQtJkrAcpoOU1JhiMuEUHMJ-6o_5dNE'
   bot_chatID = '399508171'
   send_text = 'https://api.telegram.org/bot' + bot_token + '/sendMessage?chat_id=' + bot_chatID + '&parse_mode=Markdown&text=' + bot_message

   response = requests.get(send_text)

   return response.json()

#message="kjadgckdajcbakdjcbakdjcb"
#telegram_bot_sendtext(message)
