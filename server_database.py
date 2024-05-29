from langchain_community.chat_message_histories import SQLChatMessageHistory
import langchain_core



class DatebaseManager():

    # def __init__(self, db_name):
    #     import sqlite3
    #
    #     self.conn = sqlite3.connect(db_name)
    #     self.cursor = self.conn.cursor()
    #
    #
    # def create_table(self, table_name, columns):
    #     query = f"CREATE TABLE IF NOT EXISTS {table_name} ({columns})"
    #     self.cursor.execute(query)
    #     self.conn.commit()
    #
    #
    # def insert_data(self, table_name, data):
    #     placeholders = ', '.join('?' * len(data))
    #     columns = ', '.join(data.keys())
    #     values = tuple(data.values())
    #     query = f"INSERT INTO {table_name} ({columns}) VALUES ({placeholders})"
    #     self.cursor.execute(query, values)
    #     self.conn.commit()
    #
    # def fetch_data(self, table_name, condition=None):
    #     query = f"SELECT * FROM {table_name}"
    #     if condition:
    #         query += f" WHERE {condition}"
    #     self.cursor.execute(query)
    #     return self.cursor.fetchall()
    #
    # def close_connection(self):
    #     self.conn.close()


    def initialize_datebase_message(self,session_id):

        chat_message_history = SQLChatMessageHistory(
            session_id=session_id, connection_string="sqlite:///sqlite.db"
        )

        return chat_message_history

# # Пример использования
# db = Database('example.db')
# db.create_table('users', 'id INTEGER PRIMARY KEY, name TEXT, age INTEGER')
# db.insert_data('users', {'name': 'Alice', 'age': 30})
# db.insert_data('users', {'name': 'Bob', 'age': 25})
# result = db.fetch_data('users', 'age > 26')
# print(result)
# db.close_connection()

from langchain_core.runnables import RunnableLambda, RunnablePassthrough

# db_m = DatebaseManager('db.db')
#
# ch_1= db_m.initialize_datebase_message('1')
# ch_2 = db_m.initialize_datebase_message('2')
#
# print(type(ch_1))
# print(type(ch_1.messages))
#
# x = ch_1.messages
# print(x)
#
#
#
# human_messages = [msg for msg in ch_2.messages if isinstance(msg, langchain_core.messages.human.HumanMessage)]
#
# for message in human_messages:
#     print(message.content)

