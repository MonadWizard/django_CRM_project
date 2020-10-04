from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.contrib.auth.models import Group  # add user to group

from .models import Customer


def customer_profile(sender, instance, created, **kwargs):
    if created:
        # auto add register username to customer group
        group = Group.objects.get(name='customer')  
        instance.groups.add(group)

        # auto add register customer username to user
        Customer.objects.create(
            user = instance,
            name=instance.username,
        )
post_save.connect(customer_profile, sender=User)


