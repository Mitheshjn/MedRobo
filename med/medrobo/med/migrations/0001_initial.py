# Generated by Django 3.2.8 on 2021-10-27 17:01

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='details',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='', max_length=20)),
                ('disease', models.CharField(default='', max_length=20)),
                ('door', models.CharField(default='', max_length=2)),
                ('bed', models.CharField(default='', max_length=2)),
            ],
        ),
    ]
