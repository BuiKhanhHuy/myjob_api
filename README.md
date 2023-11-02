<p align="center">
 <img src="https://github.com/BuiKhanhHuy/myjob_api/assets/69914972/ef0c454d-7947-46ab-a5e6-64ffe964bb3a" width="200"  alt="Image" />
</p>

<h1 align="center">JOB PORTAL SYSTEM</h1>
<h1 align="center">MyJob Backend API (Django REST Framework)</h1>

## Setup

### 👉 Clone repo

```plaintext
git clone https://github.com/BuiKhanhHuy/myjob_api.git
```

```plaintext
cd myjob_api
```

### 👉 Update the data in `.env` file 
Create `.env` file 
```plaintext
myjob_api/
  |-- ...
  |-- myjob_api
  |-- myjob
  |-- .env 👈
```

```plaintext
APP_ENV=local #(local or production)
DEBUG=True (True or False)
APPEND_SLASH=False (True or False)
ALLOWED_HOSTS=* (If there are multiple separated by comma ',')
CSRF_TRUSTED_ORIGINS=https://yourdomain
DB_ENGINE=django.db.backends.mysql
DB_HOST=
DB_NAME=myjob_db (your db name)
DB_PASSWORD=123456789 (your root mysql password)
DB_PORT=3306 (your mysql port)
DB_USER=root (default)
EMAIL_HOST=smtp.gmail.com
EMAIL_HOST_PASSWORD= (your password)
EMAIL_HOST_USER= (your email host user)
EMAIL_PORT=587
SERVICE_REDIS_HOST= (your redis host)
SERVICE_REDIS_PASSWORD= (your redis password)
SERVICE_REDIS_PORT= (your redis port) 
SERVICE_REDIS_USERNAME= (your redis username)
SERVICE_REDIS_DB= (your redis database)
SOCIAL_AUTH_FACEBOOK_KEY= (your facebook key)
SOCIAL_AUTH_FACEBOOK_SECRET= (your facebook secret)
SOCIAL_AUTH_GOOGLE_OAUTH2_KEY= (your google oauth2 key)
SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET= (your google oauth2 secret)
TWILIO_ACCOUNT_SID= (your twilio account side)
TWILIO_AUTH_TOKEN= (your twilio auth token
TWILIO_PHONE= (your twilio phone)
CLOUDINARY_CLOUD_NAME= (your cloudinary cloud name)
CLOUDINARY_API_KEY= (your cloudinay api key)
CLOUDINARY_API_SECRET= (your cloudinay  api secret)
WEB_CLIENT_URL=http://localhost:3001 (your web client url)
```

### 👉 Run app

<table><tbody><tr><td><h4>Docker</h4></td><td><h4>Manual (Windows)</h4></td></tr><tr><td><p>&nbsp;</p><pre><code class="language-python">docker compose -p myjob-api-project up -d </code></pre><p>&nbsp;</p></td><td><pre><code class="language-python">python -m venv venv</code></pre><pre><code class="language-python">venv\Scripts\activate</code></pre><pre><code class="language-python">pip install -r requirements.txt</code></pre><pre><code class="language-python">python manage.py migrate</code></pre><pre><code class="language-python">python manage.py runserver 0.0.0.0:8001</code></pre><p>→ New terminal in project</p><pre><code class="language-python">celery -A myjob_api.celery worker --pool=prefork --loglevel=info</code></pre><p>→ New terminal in project</p><pre><code class="language-python">celery -A myjob_api beat -l info --scheduler django_celery_beat.schedulers:DatabaseScheduler</code></pre><p><strong>→ Import data from </strong><code><strong>myjob_db.sql</strong></code><strong> file at:</strong></p><p>&nbsp;myjob_api/<br>&nbsp; &nbsp; &nbsp;|-- ...<br>&nbsp; &nbsp; &nbsp;|-- myjob_api<br>&nbsp; &nbsp; &nbsp;|-- myjob<br>&nbsp; &nbsp; &nbsp;|-- data/<br>&nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp;|-- …<br>&nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp;| myjob_db.sql 👈</p></td></tr></tbody></table>

### 👉 Go to all API: http://localhost:8001/swagger/

![Image](https://github.com/BuiKhanhHuy/myjob_api/assets/69914972/d43ffe6c-9c40-4d7c-8772-588f34616021)

### 👉 Go to Admin page: http://localhost:8001/admin/

![Image](https://github.com/BuiKhanhHuy/myjob_api/assets/69914972/1259d6d4-f94a-4086-8cd6-d2abfba64c90)

**Test administrator account:**

*   Email: [myjob.contact00000@gmail.com](mailto:myjob.testadmin@gmail.com)
*   Password: 123

## Live demo

### 👉 Link: https://huybk2-myjobapi-production.up.railway.app/admin/

### **👉** Test administrator account

*   Email: myjob.testadmin@gmail.com
*   Password: 123

## Frontend repo link

### 🌐 [Web-app](https://github.com/BuiKhanhHuy/my-job-web-app)

### 📱 [Mobile-app](https://github.com/BuiKhanhHuy/MyJobApp)