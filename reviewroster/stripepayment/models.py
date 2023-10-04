from django.db import models
from django.dispatch import receiver
from django.db.models.signals import post_save
# Create your models here.
class subscriptionStatus(models.Model):
    customer_id = models.CharField(primary_key=True,max_length=100)
    customer_email = models.EmailField(unique=True)
    is_subscibed = models.BooleanField(default=False)

    def __str__(self):
        return self.customer_email

class AddSubscriptionStatus(models.Model):
    customer_email = models.EmailField(unique=True)
    subscribed_time = models.DateTimeField(auto_now_add=True)




# @receiver(post_save)
# def create_subscription_status(sender,instance,**kwargs):
#         if(kwargs.get("created")):
#             AddSubscriptionStatus.objects.create(customer_email=instance)






