## Описание

Скрипт слушает айди целевого чат бота
Как только появилось сообщение, отправляет по ключевым словам сообщения в различные группы.


# Настройка

`SOURCE` - айди целового чата, который будем слушать (находится в loader.py)

`keywords.json` - словарь, где ключ - ключевое слово, значение - список, состоящий из:  

`айди` или `названия группы` или `пригласительной ссылки группы`.

`groups.json` - словарь, для работы скрипта. Там ничего менять не нужно


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
    pip install -r requirements.txt # для продакшена
    или
    pip install -r requirements-dev.txt # для разработки
    ```


4. Чтобы работала отправка по названию группы или пригласительной ссылки группы, то запустите сначала `loader.py` _(опционально)_
    ```shell
    python3 joiner.py
    ```


5. Запуск Бота

    ```shell
    python -m bot
    ```

Подключение сессии
. Создание файла `1-2-3.txt` (где `1` это номер телефона, `2` - api_id, `3` - api_hash)

В этот файл на каждой строке пишем пригласительные ссылки (они нужны для работы `joiner.py`)