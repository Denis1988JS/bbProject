# Generated by Django 4.2.2 on 2023-06-23 14:55

from django.db import migrations, models
import django.db.models.deletion
import django.db.models.manager


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Rubric',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20, verbose_name='Название рубрики')),
                ('order', models.IntegerField(db_index=True, default=0, verbose_name='Порядок')),
            ],
            options={
                'verbose_name': 'Рубрика',
                'verbose_name_plural': 'Рубрики',
                'ordering': ['id'],
            },
        ),
        migrations.CreateModel(
            name='SubRubric',
            fields=[
            ],
            options={
                'verbose_name': 'Подрубрика',
                'verbose_name_plural': 'Подрубрики',
                'ordering': ['id', 'name', 'super_rubric__order', 'super_rubric__name'],
                'proxy': True,
                'indexes': [],
                'constraints': [],
            },
            bases=('mainapp.rubric',),
            managers=[
                ('object', django.db.models.manager.Manager()),
            ],
        ),
        migrations.CreateModel(
            name='SuperRubric',
            fields=[
            ],
            options={
                'verbose_name': 'Надрубрика',
                'verbose_name_plural': 'Надрубрики',
                'ordering': ['id', 'name'],
                'proxy': True,
                'indexes': [],
                'constraints': [],
            },
            bases=('mainapp.rubric',),
            managers=[
                ('object', django.db.models.manager.Manager()),
            ],
        ),
        migrations.AddField(
            model_name='rubric',
            name='super_rubric',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='mainapp.superrubric', verbose_name='Надрубрика'),
        ),
    ]