# Generated by Django 5.1.4 on 2025-07-16 09:56

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='studentinfo',
            fields=[
                ('rollno', models.IntegerField(primary_key=True, serialize=False)),
                ('name', models.TextField(max_length=50)),
                ('password', models.TextField(max_length=20)),
                ('confpass', models.TextField(max_length=20)),
                ('phoneno', models.BigIntegerField(max_length=10)),
                ('email', models.EmailField(max_length=254)),
                ('image', models.ImageField(upload_to='')),
            ],
        ),
    ]
