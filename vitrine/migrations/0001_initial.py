# Generated by Django 2.2.1 on 2019-05-03 17:12

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Article',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('titre', models.CharField(max_length=100)),
                ('auteur', models.CharField(max_length=50, null=True)),
                ('date', models.DateTimeField(default=django.utils.timezone.now)),
                ('contenu', models.TextField()),
                ('epingler', models.BooleanField(default=False)),
            ],
            options={
                'ordering': ['date'],
            },
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nom_tag', models.CharField(max_length=30)),
            ],
        ),
        migrations.CreateModel(
            name='Commentaires',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateTimeField(default=django.utils.timezone.now)),
                ('contenu', models.TextField()),
                ('id_article', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='vitrine.Article')),
            ],
            options={
                'ordering': ['date'],
            },
        ),
        migrations.AddField(
            model_name='article',
            name='tag',
            field=models.ManyToManyField(null=True, to='vitrine.Tag'),
        ),
    ]
