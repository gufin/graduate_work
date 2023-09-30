# 🛠 Educational project

This is the graduate work for the course "Middle Python Developer". The goal of this project is to add a user profile 
service to an online cinema. In this service, the business offers to save sensitive information about a person: phone 
number and full name. The business will further use the phone number in marketing communications, to determine the 
uniqueness of the user, as well as for two-factor authorization.


[Authorization service repository](https://github.com/alex-fullstack/Auth_sprint_2)

[Admin panel service repository](https://github.com/alex-fullstack/new_admin_panel_sprint_3)

[Service repository with asynchronous API](https://github.com/alex-fullstack/Async_API_sprint_2)

[Service repository with user content](https://github.com/alex-fullstack/ugc_sprint_2)

[Technical task](https://github.com/gufin/graduate_work/tree/main/docs/tasks)

![Architecture](https://github.com/gufin/graduate_work/blob/main/docs/architecture.png)

**Project Dependencies:**

- docker
- docker-compose
- python 3.10
- venv


### Installing dependencies
- Instructions for installing `docker` and `docker-compose` are given at [off. website](https://docs.docker.com/install/).

- To install `python` use any method convenient for you

- After installing `python`, run the command to create a virtual environment:

    ```shell script
    python3.10 -m venv ./venv && source ./venv/bin/activate
    ``` 

- Then run the command to install all the required dependencies:

    ```shell script
    pip3 install -r requirements.txt
    ```

### Инициализация проекта
1. Create a `.env` file and fill it with the values from `.env.example`.

    ```shell script
    cp ./.env.example ./.env
    ```

2. Run the project:

    ```shell script
    docker-compose up --build -d
    ```

3. Create a superuser:
    
    ```shell script
    docker-compose exec admin python3 manage.py createsuperuser
    ```

4. Shut down all project containers:
    ```shell
    docker-compose stop
    ```

After successfully running all the above commands, you should have a fully configured application.

5. Running in development mode

    ```shell script
    docker-compose -f docker-compose.yml -f docker-compose.dev.yml up --build -d
    ```
