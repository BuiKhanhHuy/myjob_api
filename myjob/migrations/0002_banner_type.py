# Generated by Django 4.1.6 on 2023-05-26 14:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myjob', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='banner',
            name='type',
            field=models.IntegerField(choices=[(1, 'HOME'), (2, 'MAIN_JOB_RIGHT')], default=1),
        ),
    ]