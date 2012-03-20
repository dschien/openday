from django.db import models
import datetime

# Create your models here.
class Contact(models.Model):
    topic = models.CharField(max_length=200)
    message = models.CharField(max_length=200)
    sender = models.CharField(max_length=200)


class Survey(models.Model):
    cc_pre = models.IntegerField()
    cc_post = models.IntegerField()
    it_pre = models.IntegerField()
    it_post = models.IntegerField()
    age = models.IntegerField()
    gender = models.IntegerField()
    survey_date = models.DateTimeField('date surveyed')
    
    # to_string
    def __unicode__(self):
        return "age: {}, gender: {}, cc_pre: {}, it_pre: {}, cc_post: {}, it_post:{}". format(self.age, self.gender, self.cc_pre, self.it_pre, self.cc_post, self.it_post)  

    def was_surveyed_recently(self):
        return self.pub_date >= datetime.datetime.now() - datetime.timedelta(days=1)
    
    was_surveyed_recently.admin_order_field = 'survey_date'
    was_surveyed_recently.boolean = True
    was_surveyed_recently.short_description = 'Surveyed recently?'
    