# Generated by Django 4.2.11 on 2024-04-16 11:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("webapp", "0005_machine_target"),
    ]

    operations = [
        migrations.AlterField(
            model_name="performs",
            name="machine_id",
            field=models.CharField(max_length=100),
        ),
    ]
