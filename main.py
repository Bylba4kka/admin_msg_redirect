import json
import random
import time
import requests
import os

from bs4 import BeautifulSoup
from telethon.sessions import StringSession
from telethon.sync import TelegramClient, Button
from telethon import events, custom


PHONE_NUMBER: str = input("Введите номер телефона: ")
SOURCE = "-1002406205336"

def _get_string_session(phone_number, api_id, api_hash):
    if f"{phone_number}.session" in os.listdir():
        with open(f"{phone_number}.session", "r", encoding="utf-8") as session_file:
            for session_line in session_file:
                if session_line.startswith(phone_number):
                    return "-".join((session_line.split("-")[3:]))
    client = TelegramClient(StringSession(), api_id, api_hash, system_version="4.16.30-vxCUSTOM")
    client.start(phone=phone_number)
    session = client.session.save()
    client.disconnect()
    with open(f"{phone_number}.session", "w", encoding="utf-8") as session_file:
        session_file.write(f"{phone_number}-{api_id}-{api_hash}-{session}")
    return session


def get_client(phone_number, api_id, api_hash) -> TelegramClient:
    session = _get_string_session(phone_number, api_id, api_hash)
    if not session:
        print("Ошибка получения сессии")
        exit

    return TelegramClient(StringSession(session), api_id, api_hash, system_version="4.16.30-vxCUSTOM")


def get_session(phone_number, api_id, api_hash) -> TelegramClient:
    client = get_client(phone_number, api_id, api_hash)
    client.start()
    return client


def get_userinfo(phone_number) -> tuple[str | None, str | None, str | None]:
    directory = os.listdir(".")
    f_name = api_id = api_hash = None

    for file_name in directory:
        if file_name.startswith(phone_number) and file_name.endswith(".txt"):
            _, api_id, api_hash = file_name.split(".")[0].split("-")
            f_name = file_name
            break

    return f_name, api_id, api_hash


def get_groups(file_path: str | None) -> list[str]:
    try:
        with open(str(file_path), "r", encoding="utf-8-sig") as file:
            lines = [line.strip().split("/")[-1] for line in file.readlines()]

        # lines = file_contents.split("\n")
        # groups = [line for line in lines if line]  # Remove empty strings
        while "None" in lines:
            lines.remove("None")

        return lines
    except FileNotFoundError:
        print("Файл с группами не найден")
        return []


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
    if not groups_info:
        return
    with open("keywords.json", "r", encoding="utf-8") as f:
        forward_chat_ids = json.loads(f.read())

    for obj in forward_chat_ids:
        keywords = obj.get("send", None)
        group_link_or_title = obj.get("group", None)

        if not keywords:
            print("Нет send")
            return
        if not group_link_or_title:
            print("Нет group")
            return

        if "https://" in group_link_or_title:
            group_title = get_title_group_from_link(group_link_or_title)
        else:
            group_title = group_link_or_title

        chat_id = next((group["id"] for group in groups_info if group["title"].lower() == group_title.lower()), None)

        for keyword in keywords:
            if keyword.lower() in event.message.text.lower():
                try:
                    await client.forward_messages(chat_id, event.message)

                    print(f"Сообщение с ключевым словом '{keyword}' переслано в чат {chat_id} ({group_link_or_title})")
                except Exception as ex:
                    print(f"Не удалось отправить сообщение в {chat_id} ({group_link_or_title}). Ошибка: {ex}")


groups_info = None
with client:
    groups_info = get_joined_groups(client)
    print("Юзербот запущен")
    client.run_until_disconnected()
