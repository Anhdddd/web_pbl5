# Generated by Django 4.2.1 on 2023-06-09 10:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('appPBL5', '0004_remove_parking_history_ispaid_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='identity_code',
            field=models.CharField(default=None, max_length=100),
        ),
    ]