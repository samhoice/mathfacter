# Generated by Django 3.0.6 on 2020-06-16 21:23

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('problems', '0002_answer_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='rule',
            name='created',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='rule',
            name='left_exact',
            field=models.BooleanField(default=False),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='rule',
            name='right_exact',
            field=models.BooleanField(default=False),
            preserve_default=False,
        ),
    ]
