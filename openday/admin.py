'''
Created on 20 Mar 2012

@author: schien
'''
from openday.models import Survey#,Page, Questionaire

from django.contrib import admin

    
class SurveyAdmin(admin.ModelAdmin):
#    fieldsets = [
#        (None, {'fields': ['age', 'gender', 'it_pre', 'it_post', 'cc_pre', 'cc_post']}),
#        ('Date information', {'fields': ['survey_date'], 'classes': ['collapse']}),
#    ]
    
    list_display = ('survey_date', 'cc', 'it', 'cit')
    list_filter = ['survey_date']
    search_fields = ['it_pre']
    date_hierarchy = 'survey_date'  


#admin.site.register(Page)
#admin.site.register(Questionaire)
admin.site.register(Survey, SurveyAdmin)
