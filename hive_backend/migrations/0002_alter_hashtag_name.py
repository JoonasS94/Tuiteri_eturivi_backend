# Generated by Django 5.1.3 on 2024-11-20 05:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hive_backend', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='hashtag',
            name='name',
            field=models.CharField(max_length=20),
        ),
    ]