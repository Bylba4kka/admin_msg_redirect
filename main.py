import json
import random
import time
from telethon import events
from loader import PHONE_NUMBER, SOURCE, get_client, get_userinfo
from bs4 import BeautifulSoup
import requests


F_NAME, API_ID, API_HASH = get_userinfo(PHONE_NUMBER)
client = get_client(PHONE_NUMBER, API_ID, API_HASH)



def get_title_group_from_link(invite_link):

    r = requests.get(invite_link, headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:133.0) Gecko/20100101 Firefox/133.0"})

    soup = BeautifulSoup(r.text, "html.parser")

    title = soup.find("div", class_="tgme_page_title").get_text(strip=True)
    return title.lower()


def get_joined_groups(client) -> list[dict]:
    """
    Получает присоединённые группы и возвращает список словарей, содержащих название группы, её username и ID.
    """
    groups_info = []
    
    # Перебор всех диалогов
    for dialog in client.iter_dialogs():
        try:
            # Получаем название, username и ID группы
            group_info = {
                'title': dialog.name, # Название группы
                'id': dialog.id  # ID группы
            }
            groups_info.append(group_info)
        except AttributeError:
            # Обработка ошибки, когда атрибуты отсутствуют
            print(f"Ошибка: Для диалога {dialog.id} не найден необходимый атрибут.")
    
    return groups_info


@client.on(events.NewMessage())
async def handler(event: events.NewMessage.Event):
    global groups_info
    with open("keywords.json", "r", encoding="utf-8") as f:
        forward_chat_ids = json.loads(f.read())

    for obj in forward_chat_ids:
        keyword = obj["keyword"]
        chat_id = obj["id"]
        group_title = obj["group_title"]
        group_invite_link = obj["group_invite_link"]

        if not chat_id:
            if group_title:
                chat_id = next((group["id"] for group in groups_info if group["title"] == group_title), None)

            else:
                group_title = get_title_group_from_link(group_invite_link)
                print(group_title)
                chat_id = next((group["id"] for group in groups_info if group["title"] == group_title), None)
                print(chat_id)
            
        if keyword.lower() in event.message.text.lower():
            try:
                await client.send_message(chat_id, event.message)

                print(f"Сообщение с ключевым словом '{keyword}' переслано в чат {chat_id}")
            except Exception as ex:
                print(f"Не удалось отправить сообщение в {chat_id}. Ошибка: {ex}")



with client:
    groups_info = get_joined_groups(client)
    print("Юзербот запущен")
    client.run_until_disconnected()

