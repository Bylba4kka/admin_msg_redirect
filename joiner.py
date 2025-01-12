import json
from random import randint
from time import sleep
from telethon import errors
from telethon.tl.functions.channels import JoinChannelRequest
from telethon.tl.functions.messages import ImportChatInviteRequest

from loader import get_groups, get_session, get_userinfo, PHONE_NUMBER

from bs4 import BeautifulSoup
import requests



resolve_title_to_invite_link = {}


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
        if dialog.is_group:
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


def join_group(client, chat) -> bool:
    """
    Пытается войти в группу.
    """
    global resolve_title_to_invite_link
    
    try:
        # отправка запроса на вступление в группу
        if chat.startswith("+"):
            resolve_title_to_invite_link[get_title_group_from_link("https://t.me/" + chat)] = "https://t.me/" + chat
            
            result = client(ImportChatInviteRequest(chat[1:]))
        else:
            result = client(JoinChannelRequest(channel=chat))
        group = result.chats[0]  # результат всегда список, берем первый элемент
        print(f"Успешно присоединились к группе: {group.title}")
        return True
    except errors.InviteHashExpiredError:
        print(f"Срок действия хеша приглашения истек. Получите новый и повторите попытку. ({chat})")
        return False
    except errors.InviteHashInvalidError:
        print(f"Хэш приглашения недействителен. Пожалуйста, проверьте ссылку или хэш. ({chat})")
        return False
    except errors.UserAlreadyParticipantError:
        print(f"Вы уже являетесь участником группы {chat}")
        return False
    except Exception as ex:
        print(f"Ошибка вступления в группу {chat}: {ex}")
        return False


def join_groups(client, f_name) -> None:
    """
    Пытается войти во все группы из файла.
    """
    joined_groups: list[str] = get_joined_groups(client)
    file_groups: list[str] = get_groups(f_name)
    for group in file_groups:
        if group in joined_groups:
            print(f"Уже состою в группе: {group}")
        else:
            print(f"Успешное вступление в группу: {group}") if join_group(client, group) else print(
                f"Не удалось вступить в группу: {group}"
            )
            # sleep(randint(301, 999))
            sleep(5)


def save_all_groups(client, f_name) -> None:
    """
    Сохраняет все группы, к которым присоединился, в формате JSON.
    Ключами будут название группы и её пригласительная ссылка, значениями — ID группы.
    """
    groups_info = get_joined_groups(client)

    # Создаем словарь для сохранения данных
    groups_dict = {}

    for group in groups_info:
        # Получаем название, username и ID группы
        title = group['title']
        group_id = group['id']
        
        # Формируем ссылку на группу
        invite_link = resolve_title_to_invite_link.get(title.lower(), None)
        
        if invite_link:  # Если ссылка существует, добавляем в словарь
            keys = [title, invite_link]
            for key in keys:
                groups_dict[key] = {
                    'id': group_id
                }
        else:
            key = title
            groups_dict[key] = {
                'id': group_id
            }

        # Сохраняем словарь в JSON файл
        with open(f_name, "w", encoding="utf-8") as file:
            json.dump(groups_dict, file, ensure_ascii=False, indent=4)

    print(f"Группы успешно сохранены в {f_name}")
    



def main_joiner(phone_number: str) -> None:
    """
    Точка входа в программу.
    """
    f_name, api_id, api_hash = get_userinfo(phone_number)

    if api_id and api_hash:
        client = get_session(phone_number, api_id, api_hash)
        if not client:
            return
        join_groups(client, f_name)
        save_all_groups(client, "groups.json")
    else:
        print(f"Файл с номером телефона {phone_number} не найден")


if __name__ == "__main__":
    try:
        main_joiner(PHONE_NUMBER)
        print("Вошёл во все группы. Программа завершена.")
    except (KeyboardInterrupt, SystemExit):
        print("\nПриложение было остановлено")
