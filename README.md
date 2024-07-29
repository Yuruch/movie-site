# Movie review project

Django project for rating movies and finding the best movie for you

## Check it out!
[Movie project deployed to render](https://movie-site-0otf.onrender.com)
## Installing / Getting started

Python3 must be installed

```shell
git clone https://github.com/Yuruch/movie-site
cd movie-site
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python manage.py runserver
```
If you run this commands you will have project without any data
#### You can use these credentials to login or create new superuser
Login: `admin`  
Password: `Qjasq123`
## Installing / Environment variables and static files

To start this project you also need to install environment variables

In project root you have .env.example you should make your own .env file

You can use the command below to load .env automatically

`source ./load_env.sh`



You also should load static files if you want to use project with DEBUG=False

To load it run this command 

`python manage.py collectstatic --no-input`

## Installing / Loading data

If you want to load already prepared data run this commands

```shell
python manage.py migrate
python manage.py import_data
```

## Features
This site was developed so u can find the best movie for u based on rating,
your preferences and other people reviews

But some features were also added:
* You can choose whether to load media from local storage or cloud
* You can edit, create or delete movies, actors and directors
* You can also load pictures to movies, actors, directors and your user profile
* You can add reviews to movie, edit or delete your review
* Also was implemented star rating in review creation page
