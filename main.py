import json
from telethon import events
from loader import PHONE_NUMBER, SOURCE, get_client, get_userinfo


F_NAME, API_ID, API_HASH = get_userinfo(PHONE_NUMBER)
client = get_client(PHONE_NUMBER, API_ID, API_HASH)



@client.on(events.NewMessage(SOURCE))
async def handler(event: events.NewMessage.Event):
    with open("keywords.json", "r", encoding="utf-8") as f:
        forward_chat_ids = json.loads(f.read())

    for keyword, chat_ids in forward_chat_ids.items():
        
        if keyword.lower() in event.message.text.lower():
            for chat_id in chat_ids:
                with open("groups.json", "r", encoding="utf-8") as f:
                    groups = json.loads(f.read())
                    chat_id = groups.get(chat_id, chat_id)
                    if isinstance(chat_id, dict):
                        chat_id = chat_id["id"]
                try:
                    await client.send_message(chat_id, event.message)
                    print(f"Сообщение с ключевым словом '{keyword}' переслано в чат {chat_id}")
                except Exception as ex:
                    print(f"Не удалось отправить сообщение в {chat_id}. Ошибка: {ex}")


with client:
    print("Юзербот запущен")
    client.run_until_disconnected()

    # {
    # "#frontend": [-1002443692087],
    # "#webdesign": [-1002443692087],
    # "#cms": [-1002443692087, -4751053130],
    # "#webdev": [-1002443692087, -4751053130],
    # "#landing": -1002443692087,
    # "#shop": [-1002443692087, -4751053130],
    # "#backend": 4751053130,
    # "": [-1002314677140],
    # }

    # 2307229106 -1002406205336