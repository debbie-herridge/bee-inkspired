# Generated by Django 3.2.23 on 2023-12-14 08:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0002_auto_20231213_1918'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='booking',
            name='status',
        ),
        migrations.AddField(
            model_name='booking',
            name='available',
            field=models.BooleanField(default=True),
        ),
        migrations.AlterField(
            model_name='booking',
            name='preference',
            field=models.CharField(choices=[('radio', 'Radio'), ('talking', 'Talking'), ('silence', 'Silence'), ('not fused', 'Not fused')], max_length=200, null=True),
        ),
    ]
