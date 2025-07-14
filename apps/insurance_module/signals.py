from django.db.models.signals import post_save, m2m_changed
from .models import Insurance
from django.dispatch import receiver
from datetime import timedelta


@receiver(m2m_changed, sender=Insurance.subsets.through)
def calculate_price(sender, instance, action, **kwargs):
    if action in ["post_add", "post_clear", "post_remove"]:
        day = (instance.end_date - instance.start_date) + timedelta(days=1)
        day = int(day.days)

        subs = 0

        if instance.subsets.count() > 0:

            subs = instance.subsets.count()

        if instance.insurance_maneger:
            subs += 1

        if subs > 0:
            if (
                day > instance.insuranceprice.all_value_day
                or day == instance.insuranceprice.all_value_day
            ):
                temp = day - int(instance.insuranceprice.all_value_day)
                if temp > 0:
                    all_value = int(instance.insuranceprice.all_value_day) * int(
                        instance.insuranceprice.all_value_price
                    )
                    half_value = temp * int(instance.insuranceprice.other_day_price)

                    total = int(all_value) + int(half_value)

                    instance.total_price = total * subs

            else:
                price = day * int(instance.insuranceprice.all_value_price)

                instance.total_price = price * subs

        instance.save()
