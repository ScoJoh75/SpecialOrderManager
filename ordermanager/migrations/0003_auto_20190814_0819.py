# Generated by Django 2.2 on 2019-08-14 12:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ordermanager', '0002_auto_20190814_0805'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='carrier',
            field=models.CharField(choices=[('UPEXP', 'UPEXP'), ('UPSAR', 'UPSAR'), ('UPSBL', 'UPSBL'), ('UPSCN', 'UPSCN'), ('UPSGR', 'UPSGR'), ('UPSRD', 'UPSRD'), ('UPSRS', 'UPSRS'), ('UPSSV', 'UPSSV'), ('UPSWX', 'UPSWX'), ('UPS2A', 'UPS2A'), ('UPS3D', 'UPS3D'), ('FX2DY', 'FX2DY'), ('FXSTD', 'FXSTD'), ('FXPAM', 'FXPAM'), ('FXGRN', 'FXGRN'), ('FXFNL', 'FXFNL'), ('CUSPK', 'Customer Pickup')], max_length=20),
        ),
        migrations.AlterField(
            model_name='order',
            name='customer',
            field=models.CharField(choices=[('AWC', 'American Woodmark Corporation'), ('ACP', 'ACP'), ('JB', 'Jim Bishop'), ('FT', 'Fabritec'), ('HM', 'Hanssem'), ('KA', 'KabinArt'), ('LG', 'Legacy'), ('MBC', 'MasterBrand Cabinets, Inc'), ('UNI', 'Unicor')], max_length=50),
        ),
        migrations.AlterField(
            model_name='order',
            name='order_reason',
            field=models.CharField(choices=[('NEW', 'New Product'), ('NA', 'Not Applicable'), ('US', 'Unusual Size'), ('UP', 'Unusual Profile'), ('UM', 'Unusual Material'), ('OP', 'Obsolete Product'), ('NMS', 'Non-Existing Material Specification'), ('CS', 'Customer Sample'), ('SA', 'Special Assembly'), ('SI', 'Special Inspection'), ('SP', 'Special Packaging'), ('PFT', 'Profile Testing'), ('PRT', 'Process Testing')], max_length=50),
        ),
        migrations.AlterField(
            model_name='order',
            name='tooling_status',
            field=models.CharField(choices=[('ONF', 'On Floor'), ('IGR', 'In Grinding Room'), ('OTR', 'Other - See Notes')], max_length=20),
        ),
    ]
