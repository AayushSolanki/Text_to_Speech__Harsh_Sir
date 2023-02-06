# Generated by Django 4.1.1 on 2023-02-01 04:56

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='audio',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('file_name', models.CharField(max_length=40)),
                ('date_time', models.DateTimeField(auto_now_add=True)),
                ('audio_file', models.FileField(blank=True, null=True, upload_to='recs')),
            ],
        ),
        migrations.CreateModel(
            name='PDFAudio',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.TextField()),
                ('lines', models.TextField()),
                ('pdf', models.FileField(upload_to='pdfs')),
                ('audio_file', models.FileField(blank=True, null=True, upload_to='recs')),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='podcast_files',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('file_name', models.CharField(max_length=40)),
                ('date_time', models.DateTimeField(auto_now_add=True)),
                ('audio_file', models.FileField(blank=True, null=True, upload_to='podcast')),
            ],
        ),
    ]