# Generated by Django 5.1.4 on 2025-07-08 10:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0014_profile_forget_pass_token'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='forget_pass_token',
            field=models.CharField(max_length=100, null=True),
        ),
    ]
