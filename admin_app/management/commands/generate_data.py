import random
import datetime
from django.core.management.base import BaseCommand
from django.utils import timezone
from form_service.models import ModelForm, ORDER_CHOICE

class Command(BaseCommand):
    help = 'Generate sample data for ModelForm'

    def handle(self, *args, **kwargs):
        for _ in range(50):  # จำนวนข้อมูลที่ต้องการเจนเนอเรท
            ModelForm.objects.create(
                first_name=f"Name{random.randint(1, 100)}",
                last_name=f"Lastname{random.randint(1, 100)}",
                email=f"user{random.randint(1, 100)}@example.com",
                phone_number=f"0800000{random.randint(100, 999)}",
                Laundry="Laundry Service",
                date_start=timezone.now() - datetime.timedelta(days=random.randint(1, 30)),
                date_end=timezone.now(),
                clothes="Shirt",
                number_clothes=str(random.randint(1, 10)),
                number_baskets=str(random.randint(1, 5)),
                note="No notes",
                admin_price=str(random.randint(100, 500)),
                status=random.choice([choice[0] for choice in ORDER_CHOICE]),
            )
        self.stdout.write(self.style.SUCCESS('Sample data generated successfully.'))
