from django.db import models

# Create your models here.


class feestatus(models.Model):
    student_name = models.CharField(max_length=100)
    student_email = models.EmailField()
    fee_amount = models.IntegerField()
    fee_paid = models.BooleanField(default=False)


    def __str__(self):
        return self.student_email

