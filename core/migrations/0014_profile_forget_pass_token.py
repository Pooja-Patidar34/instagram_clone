# Generated by Django 5.1.4 on 2025-07-08 09:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0013_alter_profile_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='forget_pass_token',
            field=models.CharField(default=1, max_length=100),
            preserve_default=False,
        ),
    ]
