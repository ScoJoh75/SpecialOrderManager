from django.db import models
from django.utils import timezone
from django.urls import reverse


class Order(models.Model):
    CUSTOMERS = (
        ("AWC", "American Woodmark Corporation"),
        ("ACP", "ACP"),
        ("JB", "Jim Bishop"),
        ("FT", "Fabritec"),
        ("HM", "Hanssem"),
        ("KA", "KabinArt"),
        ("LG", "Legacy"),
        ("MBC", "MasterBrand Cabinets, Inc"),
        ("UNI", "Unicor"),
    )

    CARRIER = (
        ("UPEXP", "UPEXP"),
        ("UPSAR", "UPSAR"),
        ("UPSBL", "UPSBL"),
        ("UPSCN", "UPSCN"),
        ("UPSGR", "UPSGR"),
        ("UPSRD", "UPSRD"),
        ("UPSRS", "UPSRS"),
        ("UPSSV", "UPSSV"),
        ("UPSWX", "UPSWX"),
        ("UPS2A", "UPS2A"),
        ("UPS3D", "UPS3D"),
        ("FX2DY", "FX2DY"),
        ("FXSTD", "FXSTD"),
        ("FXPAM", "FXPAM"),
        ("FXGRN", "FXGRN"),
        ("FXFNL", "FXFNL"),
        ("CUSPK", "Customer Pickup"),
    )

    REASON = (
        ("NEW", "New Product"),
        ("NA", "Not Applicable"),
        ("US", "Unusual Size"),
        ("UP", "Unusual Profile"),
        ("UM", "Unusual Material"),
        ("OP", "Obsolete Product"),
        ("NMS", "Non-Existing Material Specification"),
        ("CS", "Customer Sample"),
        ("SA", "Special Assembly"),
        ("SI", "Special Inspection"),
        ("SP", "Special Packaging"),
        ("PFT", "Profile Testing"),
        ("PRT", "Process Testing"),
    )

    TOOLING = (
        ("ONF", "On Floor"),
        ("IGR", "In Grinding Room"),
        ("OTR", "Other - See Notes"),
    )

    author = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    order_number = models.CharField(max_length=255)
    order_reason = models.CharField(max_length=3, choices=REASON)
    customer = models.CharField(max_length=3, choices=CUSTOMERS)
    product_name = models.CharField(max_length=255)
    title = models.CharField(max_length=255)
    design_code = models.CharField(max_length=255)
    carrier = models.CharField(max_length=5, choices=CARRIER)
    ship_date = models.DateField()
    process_date = models.DateField()
    sequence_numbers = models.CharField(max_length=255)
    tooling_status = models.CharField(max_length=3, choices=TOOLING)
    programming_status = models.BooleanField(default=False)
    engineering_framing_setup = models.BooleanField(default=False)
    engineering_panel_setup = models.BooleanField(default=False)
    engineering_lipping_setup = models.BooleanField(default=False)
    engineering_assembly = models.BooleanField(default=False)
    engineering_options = models.BooleanField(default=False)
    engineering_other = models.BooleanField(default=False)
    order_notes = models.TextField(blank=True, null=True)
    feedback = models.TextField(blank=True, null=True)
    date = models.DateTimeField(default=timezone.now)

    def get_absolute_url(self):
        return reverse("order_detail", kwargs={'pk': self.pk})

    def __str__(self):
        return self.product_name


class Contact(models.Model):
    SITES = (
        ("BVS", "Beaver Springs"),
        ("BVT", "Beavertown"),
    )

    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    email_address = models.CharField(max_length=30)
    site = models.CharField(max_length=3, choices=SITES)
    active = models.BooleanField(default=True)

    def make_active(self):
        self.active = True
        self.save()

    def make_inactive(self):
        self.active = False
        self.save()

    def __str__(self):
        return self.first_name + " " + self.last_name
