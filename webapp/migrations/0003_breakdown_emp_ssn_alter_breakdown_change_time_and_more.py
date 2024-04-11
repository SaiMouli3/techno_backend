# Generated by Django 4.2.11 on 2024-04-08 09:48

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("webapp", "0002_reviving1_delete_reviving"),
    ]

    operations = [
        migrations.AddField(
            model_name="breakdown",
            name="emp_ssn",
            field=models.ForeignKey(
                default="SB24",
                on_delete=django.db.models.deletion.CASCADE,
                to="webapp.employee2",
            ),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name="breakdown",
            name="change_time",
            field=models.IntegerField(),
        ),
        migrations.AlterField(
            model_name="performs",
            name="partial_shift",
            field=models.FloatField(),
        ),
    ]
