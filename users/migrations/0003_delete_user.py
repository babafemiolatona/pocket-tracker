# Generated by Django 4.2.7 on 2023-11-24 23:45

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_alter_user_email'),
    ]

    operations = [
        migrations.DeleteModel(
            name='User',
        ),
    ]