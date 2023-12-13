# Generated by Django 4.2.7 on 2023-12-13 09:35

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('tester_app', '0002_alter_result_datetime'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='question',
            name='correct_answer',
        ),
        migrations.AlterField(
            model_name='result',
            name='datetime',
            field=models.DateTimeField(default=datetime.datetime(2023, 12, 13, 12, 35, 12, 854516)),
        ),
        migrations.CreateModel(
            name='TestSet',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('test_data', models.TextField()),
                ('answer', models.TextField()),
                ('question', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tester_app.question')),
            ],
        ),
    ]