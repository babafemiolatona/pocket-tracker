# Generated by Django 4.2.7 on 2023-11-22 22:43

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('tracker', '0010_alter_expense_options_alter_expensecategory_options_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='expensecategory',
            name='user',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
