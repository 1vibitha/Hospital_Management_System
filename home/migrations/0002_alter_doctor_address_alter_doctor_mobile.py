# Generated by Django 5.1.4 on 2025-01-17 09:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='doctor',
            name='address',
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name='doctor',
            name='mobile',
            field=models.CharField(max_length=15, null=True),
        ),
    ]
