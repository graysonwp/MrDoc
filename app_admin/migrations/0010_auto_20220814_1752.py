# Generated by Django 2.2.28 on 2022-08-14 17:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_admin', '0009_auto_20220716_1029'),
    ]

    operations = [
        migrations.AlterField(
            model_name='useroptions',
            name='editor_mode',
            field=models.IntegerField(default=1, verbose_name='编辑器选项'),
        ),
    ]
