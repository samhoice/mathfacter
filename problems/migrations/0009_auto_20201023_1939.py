# Generated by Django 3.0.7 on 2020-10-23 19:39

from django.db import migrations

def create_default_category(apps, schema_editor):
    Category = apps.get_model('problems', 'Category')
    Category.objects.create(name="Uncategorized")

class Migration(migrations.Migration):

    dependencies = [
        ('problems', '0008_category'),
    ]

    operations = [
        migrations.RunPython(create_default_category),
    ]
