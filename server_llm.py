from flask import Flask, request, jsonify, render_template
from prompt_generate import get_prompt,initialize_datebase
import langchain_core
from flask_oauthlib.provider import OAuth2Provider
import logging

app = Flask(__name__)


class ServerLLM:



    # Роут для обработки POST запросов
    def __init__(self):
        import sqlite3
        # Инициализация объекта Flask
        self.app = Flask(__name__)
        self.chat_history_user = None
        self.app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///oauth_example.db'
        self.oauth = OAuth2Provider(app)


        conn = sqlite3.connect('oauth_example.db')
        conn.execute('CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, username TEXT, password TEXT)')
        conn.commit()
        conn.close()

        @self.app.route('/get-username')
        def get_username():
            username = self.username
            print(username)
            return jsonify({'username': username})

        @self.app.route('/')
        def index():
            self.username = 'ssergeymiss123456'

            self.chat_history_user = initialize_datebase(self.username)

            chats = get_user_chats_from_database(
                self.username)  # Функция для получения чатов пользователя из базы данных

            print(chats)
            return render_template('chat_bot.html', chats=chats)

        def get_user_chats_from_database(username):
            import sqlite3
            conn = sqlite3.connect('sqlite.db')
            c = conn.cursor()
            c.execute("SELECT session_id FROM message_store WHERE session_id LIKE ?", (f'{username}%',))
            chats = [row[0] for row in c.fetchall()]
            unique_chats = list(set(chats))  # Преобразование множества обратно в список для сохранения порядка
            conn.close()
            return unique_chats

        @self.app.route('/chat', methods=['POST'])
        def chat():
            message = request.json['message']
            print(message)
            response = self.get_bot_response(message)
            return jsonify({'response': response})

        @self.app.route('/chat/<chat_id>', methods=['GET'])
        def get_chat_history(chat_id):
            print(chat_id)
            self.chat_history_user = initialize_datebase(chat_id)

            messages = []
            for msg in self.chat_history_user.messages:
                if isinstance(msg, langchain_core.messages.ai.AIMessage):
                    messages.append((msg.content, 'ai'))
                elif isinstance(msg, langchain_core.messages.human.HumanMessage):
                    messages.append((msg.content, 'human'))

            print(messages)

            return jsonify(messages=messages)


        ##################################################################

        @self.oauth.clientgetter
        def get_client(client_id):
            return {'client_id': client_id, 'client_secret': 'secret'}

        @self.oauth.usergetter
        def get_oauth_user(username, password, client, request):
            user = self.get_user(username)
            if user and user[2] == password:
                return {'id': username}

        @self.app.route('/oauth/token', methods=['POST'])
        @self.oauth.token_handler
        def access_token():
            return None

        @self.app.route('/register', methods=['POST'])
        def register():
            data = request.json
            username = data.get('username')
            password = data.get('password')
            if not username or not password:
                return jsonify({'error': 'Missing username or password'}), 400
            self.create_user(username, password)
            return jsonify({'message': 'User registered successfully'})



    #################################################################################################################

    # Функция для получения пользователя по имени
    def get_user(self,username):
        import sqlite3
        conn = sqlite3.connect('oauth_example.db')
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE username=?", (username,))
        user = cursor.fetchone()
        conn.close()
        return user

    # Функция для создания пользователя
    def create_user(self,username, password):
        import sqlite3
        conn = sqlite3.connect('oauth_example.db')
        cursor = conn.cursor()
        cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
        conn.commit()
        conn.close()


    def crop_string(self,input_string):

        S = ["ASSISTANT: ", "Assistant: ", "Bot: ", "bot: ", "AI: ", "System:  ", "Ассист: ", "Ответ:"]

        for s in S:
            if s in input_string:
                return input_string[input_string.find(s) + len(s):]
        return input_string

    # Простой пример ответа чат-бота
    def get_bot_response(self,message):

        import base64
        import pandas as pd
        import logging
        import requests


        query = message


        id = self.username

        chat_history_user = self.chat_history_user



        Prompt_chain_query = get_prompt(query,history=chat_history_user.messages[:10],context=[''])
        print(Prompt_chain_query)

        kwargs = {"max_new_tokens": 512,
                  "pad_token_id": 0,
                  "temperature": 0.8,
                  "top_k": 40,
                  "top_p": 0.8}

            # print(Prompt_chain_query)
        dat = {'id': [123],
               'prompt': [base64.b64encode((Prompt_chain_query).encode("utf-8")).decode("utf-8")],
               'gen_kwargs': [kwargs],
               }



        df_tmp = pd.DataFrame(dat)

        model_url = 'https://aiplatform.mos.ru/operation/mistralbotv2q8/invocations'

        # Отправка POST-запроса с данными на предсказание
        response = requests.post(model_url, json={'dataframe_records': df_tmp.to_dict(orient='records')})

        if not response.ok:
            logging.info(f'{response}')
            logging.info(f'{response.json()}')

        logging.info(f'{response}')
        answer = response.json()['predictions'][0]['assistent_answer'].strip()

        ######################################################################

        start = answer.find('Assistant:')
        end = answer.find('Human:')

        answer = answer if start == -1 else answer[start:].strip()
        answer = answer if end == -1 else answer[:end].strip()

        answer=str(answer)
        answer = self.crop_string(answer)

        chat_history_user.add_user_message(query)
        chat_history_user.add_ai_message(answer)

        return answer


        ########################################################################




# Создание экземпляра класса ServerLLM


if __name__ == '__main__':
    server = ServerLLM()
    server.app.run(host='0.0.0.0', port=5000)