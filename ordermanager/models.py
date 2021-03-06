from django.db import models
from django.urls import reverse


class Order(models.Model):
    CUSTOMERS = (
        ("Customer A", "Customer A"),
        ("Customer B", "Customer B"),
        ("Customer C", "Customer C"),
        ("Customer D", "Customer D"),
        ("Customer E", "Customer E"),
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
        ("Customer Pickup", "Customer Pickup"),
    )

    REASON = (
        ("New Product", "New Product"),
        ("Not Applicable", "Not Applicable"),
        ("Unusual Size", "Unusual Size"),
        ("Unusual Profile", "Unusual Profile"),
        ("Unusual Material", "Unusual Material"),
        ("Obsolete Product", "Obsolete Product"),
        ("Non-Existing Material Specification", "Non-Existing Material Specification"),
        ("Customer Sample", "Customer Sample"),
        ("Special Assembly", "Special Assembly"),
        ("Special Inspection", "Special Inspection"),
        ("Special Packaging", "Special Packaging"),
        ("Profile Testing", "Profile Testing"),
        ("Process Testing", "Process Testing"),
    )

    TOOLING = (
        ("In Place", "In Place"),
        ("In Production", "In Production"),
        ("Other - See Notes", "Other - See Notes"),
    )

    author = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    order_number = models.CharField(max_length=255)
    order_reason = models.CharField(max_length=50, choices=REASON)
    customer = models.CharField(max_length=50, choices=CUSTOMERS)
    product_name = models.CharField(max_length=255)
    title = models.CharField(max_length=255)
    design_code = models.CharField(max_length=255)
    carrier = models.CharField(max_length=20, choices=CARRIER)
    ship_date = models.DateField()
    process_date = models.DateField()
    sequence_numbers = models.CharField(max_length=255)
    tooling_status = models.CharField(max_length=20, choices=TOOLING)
    programming_status = models.BooleanField(default=False)
    engineering_framing_setup = models.BooleanField(default=False)
    engineering_panel_setup = models.BooleanField(default=False)
    engineering_lipping_setup = models.BooleanField(default=False)
    engineering_assembly = models.BooleanField(default=False)
    engineering_options = models.BooleanField(default=False)
    engineering_other = models.BooleanField(default=False)
    order_notes = models.TextField(blank=True, null=True)
    feedback = models.TextField(blank=True, null=True)
    date = models.DateTimeField()

    def get_absolute_url(self):
        return reverse("order_detail", kwargs={'pk': self.pk})

    def __str__(self):
        return f"{self.date.strftime('%m/%d/%Y')}  {self.order_number}  {self.product_name}"


class Contact(models.Model):
    SITES = (
        ("FYA", "Facility A"),
        ("FYB", "Facility B"),
    )

    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email_address = models.CharField(max_length=100)
    site = models.CharField(max_length=3, choices=SITES)
    active = models.BooleanField(default=True)

    def get_absolute_url(self):
        return reverse("contact_detail", kwargs={'pk': self.pk})

    def __str__(self):
        return f"{self.first_name} {self.last_name} - {self.site}"
