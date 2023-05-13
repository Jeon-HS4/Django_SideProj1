# Generated by Django 4.2 on 2023-05-13 13:21

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('pybo', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='question',
            old_name='subject',
            new_name='title',
        ),
        migrations.RenameField(
            model_name='question',
            old_name='create_date',
            new_name='write_date',
        ),
        migrations.AddField(
            model_name='question',
            name='addFile',
            field=models.FileField(blank=True, null=True, upload_to='uploads/'),
        ),
        migrations.AddField(
            model_name='question',
            name='author',
            field=models.ForeignKey(default='user', on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='question',
            name='catego',
            field=models.CharField(default='diary', max_length=50),
        ),
        migrations.DeleteModel(
            name='Answer',
        ),
    ]
