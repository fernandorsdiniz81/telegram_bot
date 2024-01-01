import requests

class TelegramBot():
	def __init__(self):
		# self.token = '6776703398:AAGkXWUbHE_ei8gN0Rbsrljps0ygX5WrSrU' # token antigo
		self.token = '6260965780:AAH25G6zzU21eBX_Aeqp2GaEPzW8Edb-4vg' # novo token
		init_url = f'https://api.telegram.org/bot{self.token}/getUpdates?timeout=100'
		response = requests.get(init_url)
		status_code = response.status_code
		response = response.json() # recebe todas as mensagens do chat
		# print(response) # teste
		if 'result' in response:
			amount_of_messages = len(response['result'])
			i = amount_of_messages - 1 # identifica o indice da última mensagem
			try:
				self.update_id = response['result'][i]['update_id'] # captura o update_id da última mensagem
				self.chat_id = response['result'][0]['message']['from']['id'] # captura o chat_id (quem é o cliente)
			except:
				self.update_id = response['result'][0]['update_id'] # captura o update_id da última mensagem
				self.chat_id = response['result'][0]['message']['from']['id'] # captura o chat_id (quem é o cliente)
		self.last_answered_message = None

	def read_messages(self):
		# print(f"\nID antes: {self.update_id}")
		try:
			read_message_url = f'https://api.telegram.org/bot{self.token}/getUpdates?timeout=100&offset={self.update_id}'
			response = requests.get(read_message_url)
			response = response.json()
			if 'result' in response:
				try: # importante, pois após o timeout, se não houver mensagem nova, haverá erro na request com o update_id que foi incrementado.
					self.text = response['result'][0]['message']['text'] # o índice sempre será 0 pq a request é pelo update_id
					# print(self.text)
					self.message_id = response['result'][0]['message']['message_id'] # sequencial de mensagens do cliente
					self.update_id += 1
					# print(f"ID depois:{self.update_id}")
				except:
					pass # não executa nada em caso de erro pq a função está no laço while
		except:
			pass

	def answer_messages(self):
		if self.last_answered_message != self.message_id:
			answer = f'Ola!! :) Você disse "{self.text}"!'
			url_para_responder = f'https://api.telegram.org/bot{self.token}/sendMessage?chat_id={self.chat_id}&text={answer}'
			requests.get(url_para_responder)
			self.last_answered_message = self.message_id


bot = TelegramBot()
while True:
	bot.read_messages()
	bot.answer_messages()
