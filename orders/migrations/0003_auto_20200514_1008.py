# Generated by Django 3.0.6 on 2020-05-14 13:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0002_auto_20200514_1006'),
    ]

    operations = [
        migrations.AlterField(
            model_name='member',
            name='tax_id',
            field=models.CharField(blank=True, max_length=10),
        ),
    ]