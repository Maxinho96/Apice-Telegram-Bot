#!/bin/bash

heroku container:push --app apice30elodebot web
heroku container:release --app apice30elodebot web
