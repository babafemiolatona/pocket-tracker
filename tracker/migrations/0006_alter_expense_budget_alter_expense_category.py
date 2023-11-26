# Generated by Django 4.2.7 on 2023-11-21 15:54

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('tracker', '0005_alter_expense_budget_alter_expense_category'),
    ]

    operations = [
        migrations.AlterField(
            model_name='expense',
            name='budget',
            field=models.ForeignKey(default=1, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='expenses', to='tracker.budget'),
        ),
        migrations.AlterField(
            model_name='expense',
            name='category',
            field=models.ForeignKey(default=1, null=True, on_delete=django.db.models.deletion.CASCADE, to='tracker.category'),
        ),
    ]