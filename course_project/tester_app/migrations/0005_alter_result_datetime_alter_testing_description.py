# Generated by Django 4.2.7 on 2023-12-13 10:54

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tester_app', '0004_alter_result_datetime_alter_testset_test_data'),
    ]

    operations = [
        migrations.AlterField(
            model_name='result',
            name='datetime',
            field=models.DateTimeField(default=datetime.datetime(2023, 12, 13, 13, 54, 31, 905380)),
        ),
        migrations.AlterField(
            model_name='testing',
            name='description',
            field=models.TextField(),
        ),
    ]