# Generated by Django 3.2.23 on 2023-12-17 00:07

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0006_alter_enquiry_image'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='booking',
            name='available',
        ),
    ]
