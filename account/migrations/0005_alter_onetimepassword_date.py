# Generated by Django 5.0 on 2023-12-27 00:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0004_onetimepassword'),
    ]

    operations = [
        migrations.AlterField(
            model_name='onetimepassword',
            name='date',
            field=models.CharField(max_length=256),
        ),
    ]
