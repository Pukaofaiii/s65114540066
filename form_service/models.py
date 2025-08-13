from django.db import models
import random

ORDER_CHOICE = (
    ("1", "เสร็จเเล้ว"),
    ("2", "กำลังดำเนินการ"),
    ("3", "รอการส่งซัก"),
    ("4", "ยกเลิกเเล้ว"),
)

class ModelForm(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(null=True)
    phone_number = models.CharField(max_length=100, null=True, blank=True)
    Laundry = models.CharField(max_length=100)
    date_start = models.DateField()
    date_end = models.DateField()
    clothes = models.CharField(max_length=100)
    number_clothes = models.CharField(max_length=100, null=True)
    number_baskets = models.CharField(max_length=100, null=True)
    note = models.CharField(max_length=100)
    admin_price = models.CharField(max_length=100 ,null=True)
    status = models.CharField(max_length=255, choices=ORDER_CHOICE, default="3")

    def __str__(self) -> str:
        return f"{self.first_name} {self.id}"