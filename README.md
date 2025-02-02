## Описание

Скрипт слушает айди целевого чат бота
Как только появилось сообщение, отправляет по ключевым словам сообщения в различные группы.


# Настройка

`SOURCE` - айди целового чата, который будем слушать.

`keywords.json` - конфигурационный словарь, отвечающий за рассылку

```
{
"group": "название или ссылка на группу, канал",
"send": "список ключевых слов, по которым фильтруем",
}
```
где:

- `id` - айди группы (может быть null)

- `keyword` - ключевое слово, по которому отсылаем

- `group_title` - название группы (отсылаем по названию группы если нет айди)

- `group_invite_link` - пригласительная ссылка (отсылаем по пригласительной ссылке если нет названия или айди)


## Запуск 

1. Переходим в папку скрипта

    ```shell
    cd admin_msg_redirect/
    ```

2. Создание и запуск окружения _(опционально)_

    ```shell
    python3 -m venv .venv
    source .venv/bin/activate
    ```

3. Установка зависимостей

    ```shell
    pip install -r requirements.txt 
    ```


4. Запуск Бота

    ```shell
    python main.py
    ```

5. Подключение сессии.

    Создание файла `1-2-3.txt` (где `1` это номер телефона, `2` - api_id, `3` - api_hash)

