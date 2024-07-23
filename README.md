# Movie review project

Django project for rating movies and finding the best movie for you

## Check it out!
[Movie project deployed to render](https://movie-site.render.com)
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
#### You can use this credentials to login or create new superuser
Login: `admin`  
Password: `Qjasq123`



## Installing / Loading data

If you want to load already prepared data run this commands

```shell
python manage.py migrate
python manage.py import_data
```
