<p align="center">
 <img src="https://res.cloudinary.com/dtnpj540t/image/upload/v1681050602/my-job/my-company-media/myjob-dark-logo.png" width="200"  alt="Image" />
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

#### Import data from file `myjob_db.sql` 
 

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
celery -A core worker --loglevel=INFO --pool=solo
celery -A myjob_api beat -l info --scheduler django_celery_beat.schedulers:DatabaseScheduler
```
