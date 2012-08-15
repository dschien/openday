'''
Created on 20 Mar 2012

@author: schien
'''
from openday.models import Survey, Selection, SurveyGroup#,Page, Questionaire

from django.contrib import admin

class SurveyGroupAdmin(admin.ModelAdmin):
    pass
    
class SelectionAdmin(admin.ModelAdmin):
    list_display = ('device', 'connection', 'content', 'time')
    list_filter = ['device', 'connection', 'content', 'time']
    search_fields = ['device', 'connection', 'content', 'time']
    
class SurveyAdmin(admin.ModelAdmin):
#    fieldsets = [
#        (None, {'fields': ['age', 'gender', 'it_pre', 'it_post', 'cc_pre', 'cc_post']}),
#        ('Date information', {'fields': ['survey_date'], 'classes': ['collapse']}),
#    ]
    
    list_display = ('survey_date', 'cc', 'it', 'cit')
    list_filter = ['survey_date']
    search_fields = ['it_pre']
    date_hierarchy = 'survey_date'  


admin.site.register(SurveyGroup, SurveyGroupAdmin)
admin.site.register(Selection, SelectionAdmin)
#admin.site.register(Questionaire)
admin.site.register(Survey, SurveyAdmin)
