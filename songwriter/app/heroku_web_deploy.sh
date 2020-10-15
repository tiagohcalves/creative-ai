#!/bin/bash

heroku login
heroku container:login

APP_NAME="song-vector-space"

heroku container:push web --app ${APP_NAME}

heroku container:release web --app ${APP_NAME}
heroku open --app $APP_NAME
heroku logs --tail --app ${APP_NAME}