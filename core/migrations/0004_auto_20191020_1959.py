# Generated by Django 2.2.6 on 2019-10-20 19:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0003_auto_20191016_1332'),
    ]

    operations = [
        migrations.CreateModel(
            name='Leagues',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('league_id', models.IntegerField()),
                ('name', models.CharField(max_length=50)),
                ('country', models.CharField(max_length=50)),
                ('country_code', models.CharField(max_length=10)),
                ('season', models.IntegerField()),
                ('season_start', models.CharField(max_length=50)),
                ('season_end', models.CharField(max_length=50)),
                ('logo', models.URLField()),
                ('flag', models.URLField()),
                ('standings', models.IntegerField()),
                ('is_current', models.IntegerField()),
            ],
            options={
                'ordering': ['league_id'],
            },
        ),
        migrations.AlterField(
            model_name='match',
            name='roundSeason',
            field=models.CharField(max_length=50, verbose_name='Round'),
        ),
    ]
