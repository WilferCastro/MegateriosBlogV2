# Generated by Django 4.0.2 on 2022-03-24 15:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Blog', '0003_alter_article_content_alter_subcomment_commentfather_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='articlelikes',
            options={'verbose_name': 'Articulos Like', 'verbose_name_plural': 'Articulos Likes'},
        ),
        migrations.AlterModelOptions(
            name='commentlikes',
            options={'verbose_name': 'Comentario Like', 'verbose_name_plural': 'Comentarios Likes'},
        ),
        migrations.AddField(
            model_name='comment',
            name='dislikes',
            field=models.IntegerField(default=0, verbose_name='No me gusta'),
        ),
        migrations.AddField(
            model_name='comment',
            name='likes',
            field=models.IntegerField(default=0, verbose_name='Me gusta'),
        ),
        migrations.AddField(
            model_name='subcomment',
            name='dislikes',
            field=models.IntegerField(default=0, verbose_name='No me gusta'),
        ),
        migrations.AddField(
            model_name='subcomment',
            name='likes',
            field=models.IntegerField(default=0, verbose_name='Me gusta'),
        ),
    ]
