# Generated by Django 5.0.3 on 2024-03-31 11:23

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0005_remove_balancechange_regularity'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.RenameField(
            model_name='balancechange',
            old_name='category_id',
            new_name='category',
        ),
        migrations.RenameField(
            model_name='reports',
            old_name='user_id',
            new_name='user',
        ),
        migrations.CreateModel(
            name='RegularBalanceChange',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sum', models.IntegerField(verbose_name='Сумма')),
                ('creation_date', models.DateTimeField(auto_now_add=True)),
                ('description', models.TextField(blank=True, null=True, verbose_name='Описание')),
                ('regularity', models.DateTimeField(verbose_name='Регулярность')),
                ('type', models.CharField(choices=[('I', 'Income'), ('E', 'Expence')], max_length=1, verbose_name='Тип изменения баланса')),
                ('category', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='app.category')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'regular_balance_changes',
            },
        ),
    ]