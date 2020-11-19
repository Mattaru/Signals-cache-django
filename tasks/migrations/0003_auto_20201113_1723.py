# Generated by Django 2.2.10 on 2020-11-13 17:23

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('tasks', '0002_auto_20201113_1257'),
    ]

    operations = [
        migrations.CreateModel(
            name='PriorityCounter',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('priority', models.PositiveIntegerField(default=0)),
                ('counter', models.PositiveIntegerField(default=0)),
            ],
        ),
        migrations.AddField(
            model_name='todoitem',
            name='priority_counter',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='prior_counter', to='tasks.PriorityCounter'),
        ),
    ]
