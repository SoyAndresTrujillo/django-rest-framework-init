# Create virtual environment
```bash
python3 -m venv venv
```
# Active virtual environment
```bash
source venv/bin/activate
```
After in console you see that:
```bash
(venv) ➜  django-rest-framework
```
Now install dependencies:
```bash
pip install django
```
```bas
pip install djangorestframework
```
Create project
```bash
django-admin startproject nameproject .
```
Create fiel requirements.txt and paste the librerias with them versión, script for see library version:
```bash
pip freeze
```
Then into folder project go to ```setting.py``` and add ```'rest_framework'``` to ```INSTALLED_APPS```
Execute project:
```bash
python manage.py runserver
```

# Models
Create app into my self project:
```bash
./manage.py startapp nameapp
```

# Migration
When the models is init, run the next script for generate de migrations:
```bash
./manage.py makemigrations
```
Then execute migrations:
```bash
./manage.py migrate
```
Is we want open the ([django shell](https://platzi.com/home/clases/10728-django-rest-framework/71313-modelos-y-serializadores-en-django-rest-framework/)) for import serializer:
```bash
./manage.py shell
```

# Docs with Swagger and OpenAPI
Create app
```bash
./manage.py startapp docs
```
#### After register the app into ```INSTALLED_APPS``` into ```setting.py```
Install libreria ([drf-spectacular](https://platzi.com/home/clases/10728-django-rest-framework/71313-modelos-y-serializadores-en-django-rest-framework/)):
```bash
pip install drf-spectacular
```
#### Now register libreria into ```setting.py```
Nos register the AutoSchema into ```setting.py```
```bash
REST_FRAMEWORK = {
    'DEFAULT_SCHEMA_CLASS': 'drf_spectacular.openapi.AutoSchema',
}
```
Great, now we need create urls for the docs:
```bash
from django.urls import path
from . import views

from drf_spectacular.views import SpectacularAPIView, SpectacularRedocView, SpectacularSwaggerView
urlpatterns = [
    # YOUR PATTERNS
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    # Optional UI:
    path('api/schema/swagger-ui/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('api/schema/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
]
```