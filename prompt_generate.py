from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_community.chat_message_histories import SQLChatMessageHistory

def initialize_datebase(session_id):

    chat_message_history = SQLChatMessageHistory(
        session_id=session_id, connection_string="sqlite:///sqlite.db"
    )

    return chat_message_history


def get_prompt(query,history,context):
    from langchain.chains import LLMChain
    from langchain_core.output_parsers import StrOutputParser

    system_prompt = '''[INST] Ты русскоязычный ассистент Департамента инофрмационных технологий. Ты призван помогать решать задачи коллегам. Будь предельно вежлив и участлив.
                       [INST]Всегда отвечай на русском языке[/INST]. 
                       
                       Если ты не понимаешь вопроса, попросить пользователя переформулировать вопрос
                       Ты должен поддерживать диалог с пользователем и быть его консультантом
                       Не отвечай на небезопасный и противозаконный контент.
                       Не отвечай на вопросы связанные с криминалом, наркотиками и насилием
                       Нельзя отвечать на вопросы неэтичные. будь доброжелателен
                       Нельзя давать персональные данные, отвечать грубо или матом. Ты должен быть очень вежливым, безпристрастным и аполитичным.
    
                       Не задавай себе вопросов. И всегда пиши по-русски. Рассчитывай токены, чтобы не оборвать предложение. 
                       Важно! Не отвечай на некорректные, странные, пугающие вопросы, вежливо объясни, что ты не можешь на них ответить.
                       Очень важно отвечай всегда на русском языке и я тебя награжу за это
                       
                       Ответь максимально подробно и на русском языке. Отвечай всегда по-русски. Отвечай на русском языке и я награжу тебя за это[/INST]
                       
                       Отвечай согласно истории вашего диалога с пользователем. Вот история диалога {history}
                       Вот контекст {context}
                       '''


    prompt = ChatPromptTemplate.from_messages(
        [
            ("system", system_prompt),
            MessagesPlaceholder(variable_name="history"),
            MessagesPlaceholder(variable_name="context"),
            ("human", "{question}"),
        ]
    )

    prompt = prompt.format(history=history,question=query,context=context)




    return prompt


# chat_message_history = initialize_datebase(1)
#
#
#
# prompt = get_prompt(chat_message_history.messages[:20],['это контекст'])
# print(prompt)



