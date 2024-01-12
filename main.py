import requests
import time


class TelegramBot():
	def __init__(self):
		self.token = '6776703398:AAE8zIuXhIaIsmimPkK0I5v-T9iYjZGv1Wc' # Feibot
		self.initial_url = f'http://api.telegram.org/bot{self.token}/getUpdates?timeout=30'


	def get_update_id(self):
		response = requests.get(self.initial_url)
		print(f"status code: {response.status_code}")
		response = response.json()
		print(f"response: {response}")
		i = len(response['result']) - 1 if len(response['result']) > 0 else 0
		print(f"i: {i}\n")
		try:
			self.update_id = response['result'][i]['update_id'] # último "update_id" do json
			return True
		except Exception as error:
			print(error)
		
		
	def read_messages(self):
		try: # tenta buscar uma mensagem com "update_id + 1" para não ficar buscando mensagens antigas
			read_message_url = f'https://api.telegram.org/bot{self.token}/getUpdates?timeout=30&offset={self.update_id}' #offset é para fazer a request pelo "update_id" ao invés de baixar todo o histórico
			response = requests.get(read_message_url)
			response = response.json()
			self.update_id = response['result'][0]['update_id'] # sequencial da mensagem do bot, cada "update-id" é uma mensagem, do mesmo cliente ou não
			self.chat_id = response['result'][0]['message']['from']['id'] # quem é o cliente - identificador único do chat
			self.first_name = response['result'][0]['message']['from']['first_name'] # primeiro nome do cliente
			self.message_id = response['result'][0]['message']['message_id'] # sequencial de mensagens do cliente
			self.text = response['result'][0]['message']['text'] # mensagem do cliente
			self.update_id += 1
			print(f"update_id: {self.update_id}\nfirst_name: {self.first_name}\nchat_id: {self.chat_id}\nmessage_id: {self.message_id}\ntext: {self.text}\n")
			return True
		except:
			pass # caso não haja mensagem com "update_id+1", o laço "while" continuará buscando pelo mesmo "update_id+1" até encontrar


	def answer_messages(self):
		answer = f'Ola {self.first_name}!!! 😃\n Você disse: "{self.text}"!'
		answer_message_url = f'https://api.telegram.org/bot{self.token}/sendMessage?chat_id={self.chat_id}&text={answer}'
		requests.get(answer_message_url)

	
	def run_bot(self):
		while True:
			if self.get_update_id():
				break
		while True:
			if self.read_messages():
				self.answer_messages()



######## Excutando o bot #########:
if __name__ == "__main__":
	time.sleep(5)
	bot = TelegramBot()
	bot.run_bot()		
