from telethon.sessions import StringSession
from telethon.sync import TelegramClient

import os


PHONE_NUMBER: str = input("Введите номер телефона: ")
SOURCE = "7989912855"

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
