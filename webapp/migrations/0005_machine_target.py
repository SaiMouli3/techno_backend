# Generated by Django 4.2.11 on 2024-04-11 09:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("webapp", "0004_alter_performs_date"),
    ]

    operations = [
        migrations.AddField(
            model_name="machine",
            name="target",
            field=models.IntegerField(default=100),
            preserve_default=False,
        ),
    ]
