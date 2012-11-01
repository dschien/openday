from django.db import models
import datetime
import base64

class Contact(models.Model):
    topic = models.CharField(max_length=200)
    message = models.CharField(max_length=200)
    sender = models.CharField(max_length=200)


class SurveyGroup(models.Model):
    name = models.CharField(max_length=200)
    def __unicode__(self):
        return  u'%s' % self.name
    
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
    group = models.ForeignKey(SurveyGroup, null=True)
    
    cc = models.IntegerField('knowledgeable about climate change', null=True)    
    it = models.IntegerField('knowledgeable about IT', null=True)
    cit = models.IntegerField('thought about the climate impacts of using the Internet', null=True)
    
    age = models.IntegerField('age', null=True)
    gender = models.IntegerField('gender', null=True)
    
    home_rank = models.IntegerField('home ranking (more,less,same)', null=True)
    home_rank_confidence = models.IntegerField('ranking confidence for home to internet ratio', null=True)

    rating = models.IntegerField('rating', null=True)
    rate_confidence = models.IntegerField('rating confidence', null=True)

    expect = models.IntegerField('expectation met', null=True)    
    new_rank = models.IntegerField('ranking after app', null=True)    
    opinion_change = models.NullBooleanField('opinion changed by survey', null=True)    
    
    selections = models.ManyToManyField(Selection)
    
    ua = models.CharField(max_length=10000, null=True)
    
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
    
    
