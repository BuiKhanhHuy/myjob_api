# Generated by Django 4.1.6 on 2023-03-29 11:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myjob', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='feedback',
            name='content',
            field=models.CharField(max_length=500),
        ),
    ]