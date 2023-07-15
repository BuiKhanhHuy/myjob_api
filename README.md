<p align="center">
 <img src="https://github.com/BuiKhanhHuy/myjob_api/assets/69914972/ef0c454d-7947-46ab-a5e6-64ffe964bb3a" width="200"  alt="Image" />
</p>

<h1 align="center">JOB PORTAL SYSTEM</h1>
<h2 align="center">MyJob Backend API (Django REST Framework)</h2>
 
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
```
```bash
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
```
```base
virtualenv venv
```
```base
.\venv\Scripts\activate
```
```base
pip install -r requirements.txt
```
```base
python manage.py makemigrations
```
```base
python manage.py migrate
```
```base
python manage.py runserver
```

### 👉 `celery` command to below
```base
celery -A myjob_api.celery worker --pool=prefork --loglevel=info
```
```base
celery -A myjob_api beat -l info --scheduler django_celery_beat.schedulers:DatabaseScheduler
```

### 👉 Go to http://localhost:8000/swagger/
<img src="https://github.com/BuiKhanhHuy/myjob_api/assets/69914972/bdf34cb0-40e9-4403-9345-5e6f6299df3a" alt="Image" /> 

### 👉 Go to http://localhost:8000/admin/
<img src="https://github.com/BuiKhanhHuy/myjob_api/assets/69914972/c411ed48-6c1e-4940-a51a-8d30859aa90e" alt="Image" /> 

### 👉 Live demo: https://bkhuy-myjobapi-production.up.railway.app/admin/
Test Admin Account:
* Email: myjob.testadmin@gmail.com
* Password: 123

### 👉 Frontend repo link
* #### 🌐  [Web-app](https://github.com/BuiKhanhHuy/my-job-web-app) 
* #### 📱  [Mobile-app](https://github.com/BuiKhanhHuy/MyJobApp) 
