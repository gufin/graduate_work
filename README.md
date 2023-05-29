# Проектная работа: диплом

У вас будет один репозиторий на все 4 недели работы над дипломным проектом. 

Если вы выбрали работу в командах, ревью будет организовано как в командных модулях с той лишь разницей, что формируете состав команды и назначаете тимлида вы сами, а не команда сопровождения.

Удачи!

[Репозиторий проекта](https://github.com/alex-fullstack/graduate_work)

[Репозиторий сервиса авторизации](https://github.com/alex-fullstack/Auth_sprint_2)

[Репозиторий сервиса панели администратора](https://github.com/alex-fullstack/new_admin_panel_sprint_3)

[Репозиторий сервиса с асинхронным апи](https://github.com/alex-fullstack/Async_API_sprint_2)

[Репозиторий сервиса с контентом пользователей](https://github.com/alex-fullstack/ugc_sprint_2)

[Техническое задание](https://github.com/alex-fullstack/graduate_work/tree/main/docs/tasks)

[Схема архитектуры](https://github.com/alex-fullstack/graduate_work/blob/main/docs/architecture.png)

**Зависимости проекта:**

- docker
- docker-compose
- python 3.10
- venv


### Установка зависимостей
- Инструкция по установке `docker` и `docker-compose` приведена на [оф. сайте](https://docs.docker.com/install/).

- Для установки `python` используйте любой удобный для Вас способ

- После установки `python` выполните команду по созданию виртуального окружения:

    ```shell script
    python3.10 -m venv ./venv && source ./venv/bin/activate
    ``` 

- Затем выполните команду по установке всех необходимых зависимостей:

    ```shell script
    pip3 install -r requirements.txt
    ```

### Инициализация проекта
1. Создайте файл `.env` и заполните его значениями из `.env.example`.

    ```shell script
    cp ./.env.example ./.env
    ```

2. Запустите проект:

    ```shell script
    docker-compose up --build -d
    ```

3. Создайте суперпользователя:
    
    ```shell script
    docker-compose exec admin python3 manage.py createsuperuser
    ```

4. Завершите работу всех контейнеров проекта:
    ```shell
    docker-compose stop
    ```

После успешного выполнения всех описанных выше команд вы должны получить полностью настроенное приложение.

5. Запуск в режиме разработки

    ```shell script
    docker-compose -f docker-compose.yml -f docker-compose.dev.yml up --build -d
    ```
