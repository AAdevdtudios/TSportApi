# Generated by Django 5.0 on 2024-01-25 01:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('subscription', '0005_alter_subscribers_options_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='subscriptionplans',
            name='PlanCode',
            field=models.CharField(blank=True, max_length=256, null=True),
        ),
    ]