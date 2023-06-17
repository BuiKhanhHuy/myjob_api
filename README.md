<p align="center">
 <img src="https://github.com/BuiKhanhHuy/myjob_api/assets/69914972/d25c4a6d-72f1-48ad-99f0-d196bf495806" width="200"  alt="Image" />
</p>

<h1 align="center">Backend API for Job portal app (MyJob)</h3>
 
`Dependencies`
```commandline
celery==5.2.7
Django==4.1.6
django-celery-beat==2.5.0
django-oauth-toolkit==2.2.0
django-redis==3.1.6
djangorestframework==3.14.0
drf-social-oauth2==1.2.1
firebase-admin==6.1.0
redis==4.5.1
twilio==8.0.0
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
```bash
APP_ENV=
DEBUG=
APPEND_SLASH=
ALLOWED_HOSTS=
CSRF_TRUSTED_ORIGINS=
DB_ENGINE=
DB_HOST=
DB_NAME=
DB_PASSWORD=
DB_PORT=
DB_USER=
EMAIL_HOST=
EMAIL_HOST_PASSWORD=
EMAIL_HOST_USER=
EMAIL_PORT=
SERVICE_REDIS_HOST=
SERVICE_REDIS_PASSWORD=
SERVICE_REDIS_PORT=
SERVICE_REDIS_USERNAME=
SERVICE_REDIS_DB=
SOCIAL_AUTH_FACEBOOK_KEY=
SOCIAL_AUTH_FACEBOOK_SECRET=
SOCIAL_AUTH_GOOGLE_OAUTH2_KEY=
SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET=
TWILIO_ACCOUNT_SID=
TWILIO_AUTH_TOKEN=
TWILIO_PHONE=
CLOUDINARY_CLOUD_NAME=
CLOUDINARY_API_KEY=
CLOUDINARY_API_SECRET=
WEB_CLIENT_URL=
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

### 👉 Go to http://localhost:8000/swagger/
<img src="https://github.com/BuiKhanhHuy/myjob_api/assets/69914972/eb594bfe-1ade-43d2-b437-b102e8bc3f53"  alt="Image" /> 

### 👉 Go to http://localhost:8000/admin/
<img src="https://github.com/BuiKhanhHuy/myjob_api/assets/69914972/c411ed48-6c1e-4940-a51a-8d30859aa90e" alt="Image" /> 
