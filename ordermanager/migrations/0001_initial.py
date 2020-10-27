# Generated by Django 2.2 on 2019-08-09 18:45

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Contact',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=30)),
                ('last_name', models.CharField(max_length=30)),
                ('email_address', models.CharField(max_length=30)),
                ('site', models.CharField(choices=[('BVS', 'Beaver Springs'), ('BVT', 'Beavertown')], max_length=3)),
                ('active', models.BooleanField(default=True)),
            ],
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('order_number', models.CharField(max_length=255)),
                ('order_reason', models.CharField(choices=[('NEW', 'New Product'), ('NA', 'Not Applicable'), ('US', 'Unusual Size'), ('UP', 'Unusual Profile'), ('UM', 'Unusual Material'), ('OP', 'Obsolete Product'), ('NMS', 'Non-Existing Material Specification'), ('CS', 'Customer Sample'), ('SA', 'Special Assembly'), ('SI', 'Special Inspection'), ('SP', 'Special Packaging'), ('PFT', 'Profile Testing'), ('PRT', 'Process Testing')], max_length=3)),
                ('customer', models.CharField(choices=[('AWC', 'American Woodmark Corporation'), ('ACP', 'ACP'), ('JB', 'Jim Bishop'), ('FT', 'Fabritec'), ('HM', 'Hanssem'), ('KA', 'KabinArt'), ('LG', 'Legacy'), ('MBC', 'MasterBrand Cabinets, Inc'), ('UNI', 'Unicor')], max_length=3)),
                ('product_name', models.CharField(max_length=255)),
                ('title', models.CharField(max_length=255)),
                ('design_code', models.CharField(max_length=255)),
                ('carrier', models.CharField(choices=[('UPEXP', 'UPEXP'), ('UPSAR', 'UPSAR'), ('UPSBL', 'UPSBL'), ('UPSCN', 'UPSCN'), ('UPSGR', 'UPSGR'), ('UPSRD', 'UPSRD'), ('UPSRS', 'UPSRS'), ('UPSSV', 'UPSSV'), ('UPSWX', 'UPSWX'), ('UPS2A', 'UPS2A'), ('UPS3D', 'UPS3D'), ('FX2DY', 'FX2DY'), ('FXSTD', 'FXSTD'), ('FXPAM', 'FXPAM'), ('FXGRN', 'FXGRN'), ('FXFNL', 'FXFNL'), ('CUSPK', 'Customer Pickup')], max_length=5)),
                ('ship_date', models.DateField()),
                ('process_date', models.DateField()),
                ('sequence_numbers', models.CharField(max_length=255)),
                ('tooling_status', models.CharField(choices=[('ONF', 'On Floor'), ('IGR', 'In Grinding Room'), ('OTR', 'Other - See Notes')], max_length=3)),
                ('programming_status', models.BooleanField(default=False)),
                ('engineering_framing_setup', models.BooleanField(default=False)),
                ('engineering_panel_setup', models.BooleanField(default=False)),
                ('engineering_lipping_setup', models.BooleanField(default=False)),
                ('engineering_assembly', models.BooleanField(default=False)),
                ('engineering_options', models.BooleanField(default=False)),
                ('engineering_other', models.BooleanField(default=False)),
                ('order_notes', models.TextField(blank=True, null=True)),
                ('feedback', models.TextField(blank=True, null=True)),
                ('date', models.DateTimeField(default=django.utils.timezone.now)),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]