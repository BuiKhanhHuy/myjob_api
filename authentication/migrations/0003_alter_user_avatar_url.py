# Generated by Django 4.1.6 on 2023-04-07 02:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0002_alter_user_avatar_url'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='avatar_url',
            field=models.URLField(default='https://res.cloudinary.com/dtnpj540t/image/upload/v1680687265/my-job/images_default/avt_default.jpg', max_length=300),
        ),
    ]