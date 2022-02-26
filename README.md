# SAD-Lab 4: Docker

### Creation of Django Project

You can create a file called `requirements.txt` to put the Django dependencies. You can create the file on the terminal or any text editor of your choice. The `requirements.txt` should contain (but not limited) this:

```
Django>=3.1.2
psycopg2>=2.8.6,<2.8.7
```


# Dockerize
## Creating the Dockerfile
You should add a `Dockerfile` in the root of the project. The `Dockerfile` should contain the following:

```
FROM python:3.9-alpine

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

COPY ./requirements.txt requirements.txt

# Installation of the Postgres requirement
RUN apk add --update --no-cache postgresql-client

# Installation of other individual dependencies
RUN apk add --update --no-cache --virtual .tmp-build-deps \
	gcc libc-dev linux-headers postgresql-dev

# Running the requirements.txt

RUN pip install --no-cache-dir -r requirements.txt
RUN apk del .tmp-build-deps


COPY ./mysite /mysite
WORKDIR /mysite

EXPOSE 3003

RUN adduser -D user

USER user
```
## Creating the Docker Compose File

```
version: "3"

services:
  db:
    expose:
      - 5432
    image: postgres:13-alpine
    env_file:
        - secret.env # Stores the Postgres configurations
    ports:
      - "5432:5432"
    volumes:
      - sad-lab6-volume:/var/lib/postgresql/data

  app:
    build:
      context: .
    ports:
      - "3003:3003"
    volumes:
      - ./mysite:/mysite
    command: >
      sh -c "python manage.py migrate && python manage.py runserver 0.0.0.0:3003" 
    env_file:
        - secret.env
    depends_on:
      - db

volumes:
  sad-lab6-volume:
    
```

Make sure to add `0.0.0.0` on the `ALLOWED_HOSTS` on the `settings.py`.
```
ALLOWED_HOSTS = ['0.0.0.0']
```

## Creating and Running of the Containers (using Docker Compose)
In order to build the containers, the `docker-compose up --build -d` will do its job. This should be shown once the command has been run.
```
[+] Building 2.1s (14/14) FINISHED
 => [internal] load build definition from Dockerfile                                                                                                     0.0s
 => => transferring dockerfile: 32B                                                                                                                      0.0s
 => [internal] load .dockerignore                                                                                                                        0.0s
 => => transferring context: 2B                                                                                                                          0.0s
 => [internal] load metadata for docker.io/library/python:3.9-alpine                                                                                     1.9s
 => [internal] load build context                                                                                                                        0.0s
 => => transferring context: 2.85kB                                                                                                                      0.0s
 => [1/9] FROM docker.io/library/python:3.9-alpine@sha256:8aa61e15b347b0e0173872af4ca79ab72d2a140ae07e206e56467363011e00af                               0.0s
 => => resolve docker.io/library/python:3.9-alpine@sha256:8aa61e15b347b0e0173872af4ca79ab72d2a140ae07e206e56467363011e00af                               0.0s
 => CACHED [2/9] COPY ./requirements.txt requirements.txt                                                                                                0.0s
 => CACHED [3/9] RUN apk add --update --no-cache postgresql-client                                                                                       0.0s
 => CACHED [4/9] RUN apk add --update --no-cache --virtual .tmp-build-deps  gcc libc-dev linux-headers postgresql-dev                                    0.0s
 => CACHED [5/9] RUN pip install --no-cache-dir -r requirements.txt                                                                                      0.0s
 => CACHED [6/9] RUN apk del .tmp-build-deps                                                                                                             0.0s
 => CACHED [7/9] COPY ./mysite /mysite                                                                                                                   0.0s
 => CACHED [8/9] WORKDIR /mysite                                                                                                                         0.0s
 => CACHED [9/9] RUN adduser -D user                                                                                                                     0.0s
 => exporting to image                                                                                                                                   0.0s
 => => exporting layers                                                                                                                                  0.0s
 => => writing image sha256:afcf1298c05e23a1a5d90e2c32257f997907a2584987b1ea26182d2a64839c6a                                                             0.0s
 => => naming to docker.io/library/sad-lab6_app                                                                                                          0.0s

Use 'docker scan' to run Snyk tests against images to find vulnerabilities and learn how to fix them
[+] Running 3/3
 ⠿ Network sad-lab6_default  Created                                                                                                                     0.1s
 ⠿ Container sad-lab6-db-1   Started                                                                                                                     0.6s
 ⠿ Container sad-lab6-app-1  Started
```

To run the container you can use this command:
```
docker compose up
```

Once the command above has been executed, it should show this:

```
docker-compose up
[+] Running 2/0
 ⠿ Container sad-lab6-db-1   Running                                                                                                                     0.0s
 ⠿ Container sad-lab6-app-1  Created                                                                                                                     0.0s
Attaching to sad-lab6-app-1, sad-lab6-db-1
sad-lab6-app-1  | Operations to perform:
sad-lab6-app-1  |   Apply all migrations: admin, auth, contenttypes, counterapp, sessions
sad-lab6-app-1  | Running migrations:
sad-lab6-app-1  |   Applying contenttypes.0001_initial... OK
sad-lab6-app-1  |   Applying auth.0001_initial... OK
sad-lab6-app-1  |   Applying admin.0001_initial... OK
sad-lab6-app-1  |   Applying admin.0002_logentry_remove_auto_add... OK
sad-lab6-app-1  |   Applying admin.0003_logentry_add_action_flag_choices... OK
sad-lab6-app-1  |   Applying contenttypes.0002_remove_content_type_name... OK
sad-lab6-app-1  |   Applying auth.0002_alter_permission_name_max_length... OK
sad-lab6-app-1  |   Applying auth.0003_alter_user_email_max_length... OK
sad-lab6-app-1  |   Applying auth.0004_alter_user_username_opts... OK
sad-lab6-app-1  |   Applying auth.0005_alter_user_last_login_null... OK
sad-lab6-app-1  |   Applying auth.0006_require_contenttypes_0002... OK
sad-lab6-app-1  |   Applying auth.0007_alter_validators_add_error_messages... OK
sad-lab6-app-1  |   Applying auth.0008_alter_user_username_max_length... OK
sad-lab6-app-1  |   Applying auth.0009_alter_user_last_name_max_length... OK
sad-lab6-app-1  |   Applying auth.0010_alter_group_name_max_length... OK
sad-lab6-app-1  |   Applying auth.0011_update_proxy_permissions... OK
sad-lab6-app-1  |   Applying auth.0012_alter_user_first_name_max_length... OK
sad-lab6-app-1  |   Applying counterapp.0001_initial... OK
sad-lab6-app-1  |   Applying sessions.0001_initial... OK
sad-lab6-app-1  | Watching for file changes with StatReloader
sad-lab6-app-1  | Performing system checks...
sad-lab6-app-1  |
sad-lab6-app-1  | System check identified no issues (0 silenced).
sad-lab6-app-1  | February 26, 2022 - 07:58:26
sad-lab6-app-1  | Django version 4.0.2, using settings 'mysite.settings'
sad-lab6-app-1  | Starting development server at http://0.0.0.0:3003/
sad-lab6-app-1  | Quit the server with CONTROL-C.
```

You can now see your created Counter app using Django through `http://0.0.0.0:3003/`.




