import ai_engine
import requests
import os
from dotenv import load_dotenv
import menu


class TelegramBot:
	def __init__(self, timeout:int=30) -> None:
		load_dotenv()
		self.token = os.environ["TOKEN"] # token do bot do Telegram
		self.timeout = timeout
		self.initial_url = f"http://api.telegram.org/bot{self.token}/getUpdates?timeout={self.timeout}"
		self.user_names = dict()
		self.bot_intelligence = ai_engine.AIEngine()
		self.menu = menu.Menu()


	def get_update_id(self) -> bool: # esta função verifica se há mensagem nova (update_id)
		response = requests.get(self.initial_url)
		response = response.json()
		print(f"response: {response}")
		if len(response) > 0: #significa que há ao menos um "update_id"
			try:
				i = len(response["result"]) - 1
				self.update_id = response["result"][i]["update_id"] # último "update_id" do json
				return True
			except Exception as error:
				print(error)
		
		
	def read_messages(self) -> bool:
		try: 
			read_message_url = f"https://api.telegram.org/bot{self.token}/getUpdates?timeout={self.timeout}&offset={self.update_id}" #offset é para fazer a request pelo "update_id" ao invés de baixar todo o histórico de não lidas
			response = requests.get(read_message_url)
			response = response.json()
			self.update_id = response["result"][0]["update_id"] # sequencial da mensagem do bot, cada "update-id" é uma mensagem, do mesmo cliente ou não
			self.chat_id = str(response["result"][0]["message"]["from"]["id"]) # quem é o cliente - identificador único do chat
			self.first_name = response["result"][0]["message"]["from"]["first_name"] # primeiro nome do cliente
			self.message_id = response["result"][0]["message"]["message_id"] # sequencial de mensagens do cliente
			self.human_message = response["result"][0]["message"]["text"] # mensagem do cliente
			self.user_names[self.chat_id] = self.first_name
			self.bot_intelligence.answer_messages_with_ai(self.chat_id, f"Meu nome é {self.user_names.get(self.chat_id)}.")
			self.update_id += 1 # incrementa update_id a fim de buscar a próxima mensagem (por isso este bloco está dentro de "try")
			print(f"update_id: {self.update_id}\nfirst_name: {self.first_name}\nchat_id: {self.chat_id}\nmessage_id: {self.message_id}\n\n{self.user_names.get(self.chat_id)}: {self.human_message}\n")
			return True
		except:
			pass # caso não haja mensagem com "update_id+1", o laço "while" continuará buscando pelo mesmo "update_id+1" até encontrar


	def answer_messages(self) -> None:
		answer =  self.bot_intelligence.answer_messages_with_ai(self.chat_id, self.human_message) # -> LangChain object
		answer_content = answer.content
		answer_message_url = f"https://api.telegram.org/bot{self.token}/sendMessage?chat_id={self.chat_id}&text={answer_content}"
		requests.get(answer_message_url)
		print(f"bot para {self.user_names.get(self.chat_id)}: {answer_content}")


	def answer_menu_messages(self): # este método trata a interação com o módulo "menu"
		options =  self.menu.show_menu()
		answer_menu_url = f"https://api.telegram.org/bot{self.token}/sendMessage?chat_id={self.chat_id}&text={options}"
		requests.get(answer_menu_url)
		print(f"bot: {options}")



	def run_bot(self) -> None:
		while True:
			if self.get_update_id(): # quando encontrado um update_id, significa que chegou a primeira mensagem e chat inicia
				break 
		while True:
			if self.read_messages():
				# if message.strip().lower() == "menu":
				# 	self.answer_menu_messages()
				# else:
				self.answer_messages()
				



######## Excutando o bot #########:
if __name__ == "__main__":
	bot = TelegramBot()
	bot.run_bot()		
