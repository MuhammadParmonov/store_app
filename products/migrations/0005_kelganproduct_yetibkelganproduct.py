# Generated by Django 4.2.7 on 2023-11-10 16:23

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0004_alter_product_image'),
    ]

    operations = [
        migrations.CreateModel(
            name='KelganProduct',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('yetkazib_beruvci', models.CharField(max_length=150, verbose_name='Yetkazib beruvchi')),
                ('datetime', models.DateTimeField(auto_now_add=True)),
                ('savdo_turi', models.CharField(choices=[('qarz', 'Nasiya'), ('naqt', 'Naqt')], max_length=50, verbose_name='Savdo turi')),
            ],
        ),
        migrations.CreateModel(
            name='YetibkelganProduct',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('soni', models.PositiveIntegerField()),
                ('cargo', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='products.kelganproduct')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='products.product')),
            ],
        ),
    ]