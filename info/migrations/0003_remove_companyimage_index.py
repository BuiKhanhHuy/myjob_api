# Generated by Django 4.1.6 on 2023-04-04 15:22

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('info', '0002_company_company_cover_image_public_id_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='companyimage',
            name='index',
        ),
    ]