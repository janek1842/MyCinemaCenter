# Generated by Django 3.2.2 on 2021-05-24 18:13

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('mycinema', '0010_alter_news_short_description'),
    ]

    operations = [
        migrations.CreateModel(
            name='Opinions',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('author_id', models.IntegerField()),
                ('films_id', models.IntegerField()),
                ('news_id', models.IntegerField()),
                ('staff_id', models.IntegerField()),
                ('cinemas_id', models.IntegerField()),
                ('opinion', models.TextField(blank=True)),
                ('rating', models.IntegerField(choices=[(1, 1), (2, 2), (3, 3), (4, 4), (5, 5)])),
                ('date_posted', models.DateTimeField(default=django.utils.timezone.now)),
            ],
        ),
    ]
