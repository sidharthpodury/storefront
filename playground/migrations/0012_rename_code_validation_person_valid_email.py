# Generated by Django 4.2.3 on 2023-07-19 19:59

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('playground', '0011_validation'),
    ]

    operations = [
        migrations.RenameField(
            model_name='person',
            old_name='code_validation',
            new_name='valid_email',
        ),
    ]
