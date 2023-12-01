# file_sharing_system

### Tech-Stack used:
* Python
* Django Framework

### clone the repository

```
git clone https://github.com/MustafaAsad198/file_sharing_system
```

### install requirements

```
pip install django
```

### run migration to register models in admin
```
python manage.py makemigrations
python manage.py migrate
```

### create a super user for admin panel
```
python manage.py createsuperuser
```

### to run django server on your localhost
```
python manage.py runserver
```

You can open the local server and try implenting the APIs through given URL patterns in core/urls.py.
This application has frontend integrated, so there is no need to type and test whole APIs. Instead, there is interactive GUI for testing APIs and understanding how website works.
