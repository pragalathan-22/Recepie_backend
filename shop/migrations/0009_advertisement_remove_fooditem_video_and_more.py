# Generated by Django 5.2 on 2025-04-29 09:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0008_transaction_fooditem_video'),
    ]

    operations = [
        migrations.CreateModel(
            name='Advertisement',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('description', models.TextField()),
                ('image', models.ImageField(blank=True, null=True, upload_to='ads_images/')),
                ('video', models.FileField(blank=True, null=True, upload_to='ads_videos/')),
                ('start_date', models.DateTimeField()),
                ('end_date', models.DateTimeField()),
            ],
        ),
        migrations.RemoveField(
            model_name='fooditem',
            name='video',
        ),
        migrations.AlterField(
            model_name='fooditem',
            name='category',
            field=models.CharField(choices=[('top', 'Top Rated'), ('all', 'All Foods')], max_length=20),
        ),
        migrations.AlterField(
            model_name='fooditem',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='foods/'),
        ),
        migrations.AlterField(
            model_name='fooditem',
            name='name',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='fooditem',
            name='rate',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=6, null=True),
        ),
    ]
