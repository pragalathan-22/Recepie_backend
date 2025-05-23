# Generated by Django 5.2 on 2025-04-29 06:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0007_order_orderitem'),
    ]

    operations = [
        migrations.CreateModel(
            name='Transaction',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('order_id', models.CharField(max_length=100)),
                ('payment_id', models.CharField(blank=True, max_length=100, null=True)),
                ('amount', models.FloatField()),
                ('status', models.CharField(max_length=20)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.AddField(
            model_name='fooditem',
            name='video',
            field=models.FileField(blank=True, null=True, upload_to='foods/videos/'),
        ),
    ]
