# Generated by Django 5.1.3 on 2024-11-24 18:39

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0002_rename_title_post_name'),
    ]

    operations = [
        migrations.RenameField(
            model_name='post',
            old_name='name',
            new_name='title',
        ),
    ]
