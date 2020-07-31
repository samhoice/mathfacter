# Generated by Django 3.0.6 on 2020-06-18 21:28

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('problems', '0003_auto_20200616_2123'),
    ]

    operations = [
        migrations.CreateModel(
            name='MathSession',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('ended', models.DateTimeField(blank=True, default=None, null=True)),
                ('rules', models.ManyToManyField(to='problems.Rule')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]