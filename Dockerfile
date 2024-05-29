# Используем базовый образ Python
FROM python:3.11

# Устанавливаем зависимости
RUN pip install Flask
RUN pip install transformers langchain_core Flask-OAuthlib langchain_community langchain pandas

# Копируем код сервера Flask и prompt generation в контейнер
COPY server_llm.py /app/server_llm.py
COPY prompt_generate.py /app/prompt_generate.py
COPY templates/chat_bot.html /app/templates/chat_bot.html

# Рабочая директория
WORKDIR /app

# Запускаем сервер Flask
CMD ["python", "server_llm.py"]
