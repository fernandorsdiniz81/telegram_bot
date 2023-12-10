import requests
import time

class TelegramBot():
	def __init__(self) -> None:
		self.token = '6776703398:AAGkXWUbHE_ei8gN0Rbsrljps0ygX5WrSrU'
		init_url = f'https://api.telegram.org/bot{self.token}/getUpdates?timeout=30'
		response = requests.get(init_url)
		response = response.json()
		amount_of_messages = len(response['result'])
		i = amount_of_messages - 1
		self.update_id = response['result'][i]['update_id']
		self.chat_id = response['result'][i]['message']['from']['id']

	def read_messages(self):
		read_message_url = f'https://api.telegram.org/bot{self.token}/getUpdates?timeout=100&offset={self.update_id}'
		response = requests.get(read_message_url)
		response = response.json()		
		self.update_id += 1
		message_id = response['result'][0]['message']['message_id'] # sequencial de mensagens do cliente
		text = response['result'][0]['message']['text']
		print(text)

	def answer_messages(self):
		answer = 'Ola!! :) Tudo Bem?'
		url_para_responder = f'https://api.telegram.org/bot{self.token}/sendMessage?chat_id={self.chat_id}&text={answer}'
		requests.get(url_para_responder)


bot = TelegramBot()
while True:
	bot.read_messages()
	bot.answer_messages()



