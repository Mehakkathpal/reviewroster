from django.db import models

# Create your models here.


class Companies(models.Model):
    company_id = models.IntegerField(primary_key=True)
    company_name = models.CharField(max_length=50)
    company_category = models.CharField(max_length=20)
    company_origin = models.CharField(max_length=20)
    company_size = models.IntegerField()
    company_logo = models.URLField(blank=True)
    founded_on = models.DateField()


    def __str__(self):
        return self.company_name

    
