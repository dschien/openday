from django.db import models
import datetime
import base64

# Create your models here.
class Contact(models.Model):
    topic = models.CharField(max_length=200)
    message = models.CharField(max_length=200)
    sender = models.CharField(max_length=200)


class Selection(models.Model):
    DEVICE_CHOICES = (
        ('P', 'phone'),
        ('T', 'tablet'),
        ('L', 'laptop'),
        ('D', 'pc'),
    )
    device = models.CharField(max_length=1, choices=DEVICE_CHOICES)
    CONNECTION_CHOICES = (
        ('W', 'wifi & router'),
        ('M', '3G mobile'),
    )
    connection = models.CharField(max_length=1, choices=CONNECTION_CHOICES)
    CONTENT_CHOICES = (
        ('V', 'video'),
        ('W', 'web page'),
    )
    content = models.CharField(max_length=1, choices=CONTENT_CHOICES)
    
    time = models.IntegerField('reading viewing time')

    


class Survey(models.Model):
    
    cc = models.IntegerField('knowledgeable about climate change', null=True)    
    it = models.IntegerField('knowledgeable about IT', null=True)
    cit = models.IntegerField('thought about the climate impacts of using the Internet', null=True)
    age = models.IntegerField('age', null=True)
    gender = models.IntegerField('gender', null=True)
    
    servers = models.IntegerField('server ranking', null=True)
    laptop = models.IntegerField('laptop ranking', null=True)
    acc_net = models.IntegerField('access network ranking', null=True)
    internet = models.IntegerField('internet ranking', null=True)

    rank_confidence = models.IntegerField('ranking confidence', null=True)

    rating = models.FloatField('rating', null=True)
    rate_confidence = models.IntegerField('rating confidence', null=True)

    expect = models.IntegerField('expectation met', null=True)    
    
    selections = models.ManyToManyField(Selection)
    
#    # ------------- selections --------------------
#    _selections = models.TextField(
#            db_column='data',
#            blank=True, null=True)
#
#    def set_selections(self, selections):
#        self._data = base64.encodestring(selections)
#
#    def get_selections(self):
#        return base64.decodestring(self._selections)
#
#    selections = property(get_selections, set_selections)
    
#    # ------------------- selections ------------------
#    
    
    duration = models.IntegerField('interaction time in seconds', null=True)
    survey_date = models.DateTimeField('date surveyed')
    
    # to_string
    def __unicode__(self):
        return "age: {}, gender: {}, cc: {}, it: {}, cit:{}". format(self.age, self.gender, self.cc, self.it, self.cit)  

    def was_surveyed_recently(self):
        return self.pub_date >= datetime.datetime.now() - datetime.timedelta(days=1)
    
    was_surveyed_recently.admin_order_field = 'survey_date'
    was_surveyed_recently.boolean = True
    was_surveyed_recently.short_description = 'Surveyed recently?'
    
    
