# Generated by Django 4.1.6 on 2023-04-02 17:18

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django_extensions.db.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('common', '0001_initial'),
        ('info', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='JobPost',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('create_at', models.DateTimeField(auto_now_add=True)),
                ('update_at', models.DateTimeField(auto_now=True)),
                ('job_name', models.CharField(max_length=255)),
                ('slug', django_extensions.db.fields.AutoSlugField(blank=True, editable=False, populate_from='job_name', unique=True)),
                ('deadline', models.DateField()),
                ('quantity', models.IntegerField()),
                ('gender_required', models.CharField(blank=True, choices=[('M', 'Nam'), ('F', 'Nữ'), ('O', 'Khác')], max_length=1, null=True)),
                ('job_description', models.TextField()),
                ('job_requirement', models.TextField(blank=True, null=True)),
                ('benefits_enjoyed', models.TextField(blank=True, null=True)),
                ('position', models.SmallIntegerField(choices=[(1, 'Sinh viên/Thực tập sinh'), (2, 'Mới tốt nghiệp'), (3, 'Nhân viên'), (4, 'Trưởng nhóm/Giám sát'), (5, 'Quản lý'), (6, 'Phó Giám đốc'), (7, 'Giám đốc'), (8, 'Tổng Giám đốc'), (9, 'Chủ tịch/Phó Chủ tịch')])),
                ('type_of_workplace', models.SmallIntegerField(choices=[(1, 'Làm việc tại văn phòng'), (2, 'Làm việc kết hợp'), (3, 'Làm việc tại nhà')])),
                ('experience', models.SmallIntegerField(choices=[(1, 'Chưa có kinh nghiệm'), (2, 'Dưới 1 năm kinh nghiệm '), (3, '1 năm kinh nghiệm'), (4, '2 năm kinh nghiệm'), (5, '3 năm kinh nghiệm'), (6, '4 năm kinh nghiệm'), (7, '5 năm kinh nghiệm'), (8, 'Trên 5 năm kinh nghiệm')])),
                ('academic_level', models.SmallIntegerField(choices=[(1, 'Trên Đại học'), (2, 'Đại học'), (3, 'Cao đẳng'), (4, 'Trung cấp'), (5, 'Trung học'), (6, 'Chứng chỉ nghề')])),
                ('job_type', models.SmallIntegerField(choices=[(1, 'Nhân viên chính thức'), (2, 'Bán thời gian'), (4, 'Thời vụ - Nghề tự do'), (5, 'Thực tập')])),
                ('salary_min', models.IntegerField()),
                ('salary_max', models.IntegerField()),
                ('is_hot', models.BooleanField(default=False)),
                ('is_urgent', models.BooleanField(default=False)),
                ('is_verify', models.BooleanField(default=False)),
                ('contact_person_name', models.CharField(max_length=100)),
                ('contact_person_phone', models.CharField(max_length=15)),
                ('contact_person_email', models.EmailField(max_length=100)),
                ('views', models.BigIntegerField(default=0)),
                ('shares', models.BigIntegerField(default=0)),
                ('career', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='job_posts', to='common.career')),
                ('company', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='job_posts', to='info.company')),
                ('location', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='job_posts', to='common.location')),
            ],
            options={
                'db_table': 'myjob_job_job_post',
            },
        ),
        migrations.CreateModel(
            name='SavedJobPost',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('create_at', models.DateTimeField(auto_now_add=True)),
                ('update_at', models.DateTimeField(auto_now=True)),
                ('job_post', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='job.jobpost')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'myjob_job_saved_job_post',
            },
        ),
        migrations.CreateModel(
            name='JobPostActivity',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('create_at', models.DateTimeField(auto_now_add=True)),
                ('update_at', models.DateTimeField(auto_now=True)),
                ('job_post', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='job.jobpost')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'myjob_job_job_post_activity',
            },
        ),
        migrations.AddField(
            model_name='jobpost',
            name='peoples_applied',
            field=models.ManyToManyField(related_name='job_posts_activity', through='job.JobPostActivity', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='jobpost',
            name='peoples_saved',
            field=models.ManyToManyField(related_name='saved_job_posts', through='job.SavedJobPost', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='jobpost',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='job_posts', to=settings.AUTH_USER_MODEL),
        ),
    ]