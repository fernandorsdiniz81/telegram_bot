import requests

class TelegramBot():
	def __init__(self):
		self.token = '6776703398:AAGkXWUbHE_ei8gN0Rbsrljps0ygX5WrSrU'
		init_url = f'https://api.telegram.org/bot{self.token}/getUpdates?timeout=100'
		response = requests.get(init_url)
		status_code = response.status_code
		response = response.json() # recebe todas as mensagens do chat
		print(status_code, response.keys()) # teste
		print(response['result'])# teste
		amount_of_messages = len(response['result'])
		i = amount_of_messages - 1 # identifica o indice da última mensagem
		try:
			self.update_id = response['result'][i]['update_id'] # captura o update_id da última mensagem
		except:
			self.update_id = response['result'][0]['update_id'] # caso não haja mensagens anteriores
		self.chat_id = response['result'][0]['message']['from']['id'] # captura o chat_id (quem é o cliente)
					
	def read_messages(self):
		try:
			print(f"\nID antes: {self.update_id}")
			read_message_url = f'https://api.telegram.org/bot{self.token}/getUpdates?timeout=100&offset={self.update_id}'
			response = requests.get(read_message_url)
			response = response.json()		
			self.text = response['result'][0]['message']['text']
			
			print(self.text)
			#message_id = response['result'][0]['message']['message_id'] # sequencial de mensagens do cliente
			self.update_id += 1
			print(f"ID depois:{self.update_id}")
		except:
			pass

	def answer_messages(self):
		answer = f'Ola!! :) Você disse "{self.text}"!'
		url_para_responder = f'https://api.telegram.org/bot{self.token}/sendMessage?chat_id={self.chat_id}&text={answer}'
		requests.get(url_para_responder)


bot = TelegramBot()
while True:
	bot.read_messages()
	bot.answer_messages()



