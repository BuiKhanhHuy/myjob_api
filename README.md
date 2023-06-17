<p align="center">
 <img src="https://github.com/BuiKhanhHuy/myjob_api/assets/69914972/d25c4a6d-72f1-48ad-99f0-d196bf495806" width="200"  alt="Image" />
</p>

<h1 align="center">Backend API for Job portal app (MyJob)</h3>
 
`Dependencies`
```commandline
aiohttp==3.8.4
aiohttp-retry==2.8.3
aiosignal==1.3.1
amqp==5.1.1
asgiref==3.6.0
async-timeout==4.0.2
asyncio==3.4.3
attrs==22.2.0
billiard==3.6.4.0
CacheControl==0.12.11
cachetools==5.3.0
celery==5.2.7
certifi==2022.12.7
cffi==1.15.1
charset-normalizer==3.0.1
click==8.1.3
click-didyoumean==0.3.0
click-plugins==1.1.1
click-repl==0.2.0
cloudinary==1.32.0
colorama==0.4.6
coreapi==2.3.3
coreschema==0.0.4
cron-descriptor==1.2.35
cryptography==39.0.0
defusedxml==0.7.1
Deprecated==1.2.13
Django==4.1.6
django-admin-list-filter-dropdown==1.0.3
django-admin-volt==1.0.10
django-autoslug==1.9.9
django-celery-beat==2.5.0
django-ckeditor==6.5.1
django-cors-headers==3.14.0
django-extensions==3.2.1
django-filter==23.1
django-js-asset==2.0.0
django-light==0.1.0.post3
django-oauth-toolkit==2.2.0
django-otp==1.1.6
django-redis==3.1.6
django-timezone-field==5.0
djangorestframework==3.14.0
drf-social-oauth2==1.2.1
drf-yasg==1.21.4
ecdsa==0.18.0
elasticsearch==7.17.9
elasticsearch-dsl==7.4.1
fast-autocomplete==0.9.0
firebase-admin==6.1.0
frozenlist==1.3.3
geographiclib==2.0
geopy==2.3.0
google-api-core==2.11.0
google-api-python-client==2.76.0
google-auth==2.16.0
google-auth-httplib2==0.1.0
google-cloud-core==2.3.2
google-cloud-firestore==2.9.1
google-cloud-storage==2.7.0
google-crc32c==1.5.0
google-resumable-media==2.4.1
googleapis-common-protos==1.58.0
grpcio==1.52.0
grpcio-status==1.52.0
gunicorn==20.1.0
httplib2==0.21.0
idna==3.4
inflection==0.5.1
itypes==1.2.0
Jinja2==3.1.2
jsonschema==4.17.3
jwcrypto==1.4.2
kombu==5.2.4
MarkupSafe==2.1.2
msgpack==1.0.4
multidict==6.0.4
numpy==1.24.3
oauthlib==3.2.2
openapi-codec==1.3.2
packaging==23.0
pandas==2.0.1
Pillow==9.4.0
prompt-toolkit==3.0.38
proto-plus==1.22.2
protobuf==4.21.12
psycopg2-binary==2.9.6
pyasn1==0.4.8
pyasn1-modules==0.2.8
pycparser==2.21
PyJWT==2.6.0
pylev==1.4.0
PyMySQL==1.0.3
pyparsing==3.0.9
pyrsistent==0.19.3
python-crontab==2.7.1
python-dateutil==2.8.2
python-decouple==3.7
python-jose==3.3.0
python3-openid==3.2.0
pytz==2022.7.1
PyYAML==6.0
redis==4.5.1
requests==2.28.2
requests-oauthlib==1.3.1
rsa==4.9
ruamel.yaml==0.17.21
ruamel.yaml.clib==0.2.7
simplejson==3.18.1
six==1.16.0
social-auth-app-django==5.0.0
social-auth-core==4.3.0
sqlparse==0.4.3
swagger-spec-validator==3.0.3
twilio==8.0.0
typing_extensions==4.4.0
tzdata==2022.7
uritemplate==4.1.1
urllib3==1.26.14
vine==5.0.0
wcwidth==0.2.6
whitenoise==6.4.0
wrapt==1.14.1
yarl==1.8.2

```

### 👉 Setup

#### Clone repo
```bash
git clone https://github.com/BuiKhanhHuy/myjob_api.git
cd myjob_api
```

#### Update the data in the file `.env`
```bash
|--> .env
```

### 👉 Applocation Local server `environment` setup

```base
pip install virtualenv 
virtualenv venv
.\venv\Scripts\activate
pip install -r requirements.txt
python manage.py makemigrations
python manage.py migrate
python manage.py runserver
```

### 👉 `celery` command to below
```base
celery -A myjob_api.celery worker --pool=solo --loglevel=info
celery -A myjob_api beat -l info --scheduler django_celery_beat.schedulers:DatabaseScheduler
```
