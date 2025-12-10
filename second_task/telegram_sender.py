import sys
import requests

#Замените на ваш токен бота
BOT_TOKEN = "YOUR_BOT_TOKEN"

#Замените на ID вашего чата
CHAT_ID = "YOUR_CHAT_ID"

#Имя файла с текстом
TEXT_FILE_PATH = "second_task/message.txt"

def send_message_to_telegram(text):
    """Отправляет сообщение в указанный Telegram-chat."""
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": CHAT_ID,
        "text": text,
        "parse_mode": 'Markdown'
    }

    try:
        response = requests.post(url, data=payload)
        response.raise_for_status()
        print("Сообщение успешно доставлено")
    except requests.exceptions.RequestException as e:
        print(f"Ошибка при отправке сообшения: {e}")

def read_text_from_file(file_path):
    """Читает весь текст из файла"""
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            return file.read()
    except FileNotFoundError:
        print(f"Ошибка: Файл '{file_path}' не найден.")
        sys.exit(1)
    except IOError as e:
        print(f"Ошибка чтения файла: {e}")
        sys.exit(1)

if __name__ == '__main__':
    message_text = read_text_from_file(TEXT_FILE_PATH)
    if message_text:
        send_message_to_telegram(message_text)