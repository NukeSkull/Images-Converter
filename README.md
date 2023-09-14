# PNG Image Converter

## Table of Content

1. [About the project](#about-the-project)
2. [Setup/Installation](#setup--installation)
3. [Technologies](#technologies)
4. [Available Scripts](#available-scripts)

## About the Project

PNG Image Converter is an app you can use in order to convert png images into jpg
images.\
You just need to upload your png image and download the resulting file.

## Setup / Installation

You can either run this project through docker containers or raise both Back End and
Front End manually, here are the instructions for both cases:

### Through Docker containers

For this option you need to have installed both docker and docker-compose

* Download or clone the repository
* Open a terminal at the root of the project
* Run command `docker-compose up --build`
* In your browser, open [http://localhost:3000](http://localhost:3000)

In case you want to access Django admin site, follow this steps:

* Open a terminal on the root of the project
* Run command `docker compose exec -it backend python manage.py createsuperuser`
    * When asked for a username and password, enter `postgres` for both
    * There's no specific needed email, when asked for it input goes to your choice
    * When asked for password validation enter `y`
* When accessing Django admin site (`localhost:8000/admin`), use this user credentials

### Manually

* Download or clone the repository

#### Front End

* Open a terminal at the root of the project
* Run command `cd frontend`
* Run command `yarn install` in order to install all dependencies
* Run command `yarn start` to run the frontend
* In your browser, open [http://localhost:3000](http://localhost:3000)

#### Back End

* Open a terminal at the root of the project
* Run `yarn install` in the terminal
* Open `.env` file and modify the variables with your values:
    * `DATABASE_HOST`: The host for your database. E.g `127.0.0.1`
    * `DATABASE_PORT`: The port for your database. E.g `5432`
    * `DJANGO_SECRET_KEY`: Your django secret key
    * `BROKER_URL`: The URL of the broker you want to use for the celery workers.
      E.g `amqp://guest:guest@localhost:5672//`
    * `RESULT_BACKEND`: The result backend of the broker. E.g `rpc://`
* Run `python manage.py runserver` to start the backend service
* Open another terminal
* Run command `celery -A images_converter worker -l INFO` to start celery workers

In case you want to access Django admin site, follow this steps:

* Open a terminal on the root of the project
* Run command `python manage.py createsuperuser`
* When asked for a username and password, enter `postgres` for both
* There's no specific needed email, when asked for it input goes to your choice
* When asked for password validation enter `y`
* When accessing Django admin site (`localhost:8000/admin`), use this user credentials

## Technologies

PNG Image Converter uses the following technologies:

### Front End

* React.js
* Testing-Library / Jest

### Back End

* Python 3.7
* Django
* Django-Rest-Framework
* Celery / RabbitMQ
* Docker
* PostgresSQL
* Pytest

## Available Scripts

### Front End

In the Front End project directory, you can run:

#### `yarn start:dev`

Runs the app in the development mode.\
Open [http://localhost:3000](http://localhost:3000) to view it in your browser.

The page will reload when you make changes.\
You may also see any lint errors in the console.

#### `yarn start:prod`

Runs the app in the production mode.\
Open [http://localhost:3000](http://localhost:3000) to view it in your browser.

The page will reload when you make changes.\
You may also see any lint errors in the console.

#### `yarn test`

Launches the test runner in the interactive watch mode.\

#### `yarn test:ci`

Launches the test runner in continuous integration mode

#### `yarn test:debug`

Launches the test runner in debug mode.

#### `yarn run build`

Builds the app for production to the `build` folder.\
It correctly bundles React in production mode and optimizes the build for the best
performance.

The build is minified and the filenames include the hashes.\
Your app is ready to be deployed!

#### `yarn run eject`

**Note: this is a one-way operation. Once you `eject`, you can't go back!**

If you aren't satisfied with the build tool and configuration choices, you can `eject`
at any time. This command will remove the single build dependency from your project.

Instead, it will copy all the configuration files and the transitive dependencies (
webpack, Babel, ESLint, etc) right into your project so you have full control over them.
All of the commands except `eject` will still work, but they will point to the copied
scripts so you can tweak them. At this point you're on your own.

You don't have to ever use `eject`. The curated feature set is suitable for small and
middle deployments, and you shouldn't feel obligated to use this feature. However we
understand that this tool wouldn't be useful if you couldn't customize it when you are
ready for it.

### Back End

#### `python manage.py runserver`

Starts the Back End server.

#### `celery -A images_converter worker -l INFO`

Starts celery workers.