# Generated by Django 4.2.3 on 2024-03-15 14:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0002_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='fooditem',
            name='active',
            field=models.BooleanField(default=True),
        ),
    ]
