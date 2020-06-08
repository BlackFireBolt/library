# Generated by Django 2.2.8 on 2020-06-05 14:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='author',
            name='name',
        ),
        migrations.AddField(
            model_name='author',
            name='first_name',
            field=models.CharField(default='Андрей', max_length=20, verbose_name='Имя автора'),
        ),
        migrations.AddField(
            model_name='author',
            name='last_name',
            field=models.CharField(default='Андрей', max_length=20, verbose_name='Фамилия автора'),
        ),
        migrations.AddField(
            model_name='author',
            name='middle_name',
            field=models.CharField(blank=True, max_length=20, verbose_name='Отчество автора'),
        ),
        migrations.AlterField(
            model_name='article',
            name='slug',
            field=models.SlugField(max_length=100, unique=True, verbose_name='Алиас'),
        ),
        migrations.AlterField(
            model_name='author',
            name='slug',
            field=models.SlugField(max_length=20, unique=True, verbose_name='Алиас'),
        ),
        migrations.AlterField(
            model_name='publisher',
            name='slug',
            field=models.SlugField(max_length=20, unique=True, verbose_name='Алиас'),
        ),
        migrations.AlterField(
            model_name='topic',
            name='slug',
            field=models.SlugField(max_length=30, unique=True, verbose_name='Алиас'),
        ),
    ]
