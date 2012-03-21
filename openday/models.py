from django.db import models
import datetime

# Create your models here.
class Contact(models.Model):
    topic = models.CharField(max_length=200)
    message = models.CharField(max_length=200)
    sender = models.CharField(max_length=200)


class Survey(models.Model):
    
    cc = models.IntegerField(null=True)    
    it = models.IntegerField(null=True)
    cit = models.IntegerField(null=True)
    age = models.IntegerField(null=True)
    gender = models.IntegerField(null=True)
    
    pre_servers = models.IntegerField(null=True)
    pre_laptop = models.IntegerField(null=True)
    pre_acc_net = models.IntegerField(null=True)
    pre_internet = models.IntegerField(null=True)
    pre_points = models.IntegerField(null=True)

    post_servers = models.IntegerField(null=True)
    post_laptop = models.IntegerField(null=True)
    post_acc_net = models.IntegerField(null=True)
    post_internet = models.IntegerField(null=True)
    post_points = models.IntegerField(null=True)
    
    survey_date = models.DateTimeField('date surveyed')
    
    # to_string
    def __unicode__(self):
        return "age: {}, gender: {}, cc: {}, it: {}, cit:{}". format(self.age, self.gender, self.cc, self.it, self.cit)  

    def was_surveyed_recently(self):
        return self.pub_date >= datetime.datetime.now() - datetime.timedelta(days=1)
    
    was_surveyed_recently.admin_order_field = 'survey_date'
    was_surveyed_recently.boolean = True
    was_surveyed_recently.short_description = 'Surveyed recently?'
    
