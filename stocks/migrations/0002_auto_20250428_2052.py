# Generated by Django 3.2.4 on 2025-04-28 18:52

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('articles', '0001_initial'),
        ('stocks', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='stockmovement',
            name='type_mouvement',
        ),
        migrations.AddField(
            model_name='stockmovement',
            name='mouvement_type',
            field=models.CharField(choices=[('entrée', 'Entrée'), ('sortie', 'Sortie')], default='entrée', max_length=10),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='stockmovement',
            name='article',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='mouvements', to='articles.article'),
        ),
    ]
