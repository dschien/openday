from django.http import HttpResponse
from django.views.decorators.http import require_http_methods
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from django.http import HttpResponseRedirect
from forms import ContactForm
from models import Survey, Selection , Contact
import logging
import datetime
from django.core.urlresolvers import reverse
import re
import json
from openday.models import SurveyGroup
#import pdb;

# Create your views here.

#https://docs.djangoproject.com/en/dev/ref/request-response/#django.http.HttpResponse.set_cookie
logger = logging.getLogger(__name__)

def start(request, group=None):

    logger.info("Group:" + group if group else ' no group defined')
    if not group:
        # if it doesn't have a group -> run in no-tracking mode
        #@todo: implement no group mode
        pass        
           
    if not request.session :
        # if it doesn't have a session -> start again
        return render_to_response('start.html', {'error_message': "Your session had time out. Start again.", }, context_instance=RequestContext(request))        
        
    logger.info('<start> : {}'.format(request.session.session_key)) 
    return render_to_response('start.html', {'group':group}, context_instance=RequestContext(request))
    del request.session['type']
    
@require_http_methods(["POST"])    
def gender(request, group=None):

    if not request.session :
        # if it doesn't have a session -> start again
        return render_to_response('start.html', {'error_message': "Your session had time out. Start again.", }, context_instance=RequestContext(request))             
    logger.info('<gender> sid: {} , POST:{}'.format(request.session.session_key, request.POST))

    if 'survey_id' in request.session:
        del request.session['survey_id']

    if request.POST['answer'] == 'Skip survey':
        request.session['type'] = 'skip'
#        return render_to_response('index.html', {}, context_instance=RequestContext(request))
        return HttpResponseRedirect(reverse('openday.views.app'))
    
    # create new survey
    s = Survey() 
    s.survey_date = datetime.datetime.now()
    s.group = get_group(group)
    s.save()
    request.session['survey_id'] = s.id
    request.session['type'] = 'survey'
    # no data to show    
    return render_to_response('gender.html', {}, context_instance=RequestContext(request))

@require_http_methods(["POST"])
def climate(request, group=None):
    # no data to show
    if not request.session:
        # if it doesn't have a session -> start again
        return render_to_response('start.html', {'error_message': "Your session had time out. Start again.", }, context_instance=RequestContext(request))
    # save the information from the form into the session                
    logger.info('<climate> sid: {} , POST:{}'.format(request.session.session_key, request.POST))        
    
    if re.search('Skip', request.POST['answer']):
        return render_to_response('climate.html', {}, context_instance=RequestContext(request))
    
    errors = []
    if not 'gender' in request.POST : 
        errors.append('error_gender')
    if not 'age' in request.POST : 
        errors.append('error_age')                                
    
    if len(errors) > 0:
        return render_to_response('gender.html', {'error_message':'Please answer each question.'}, context_instance=RequestContext(request))
    
    s = get_object_or_404(Survey, id=request.session['survey_id'])   
    s.gender = request.POST['gender'] if 'gender' in request.POST else -1  
    s.age = request.POST['age'] if 'age' in request.POST else -1    
    s.save()
    
    return render_to_response('climate.html', {}, context_instance=RequestContext(request))

@require_http_methods(["POST"])
def rank(request, group=None):
    if not request.session :
        # if it doesn't have a session -> start again
        return render_to_response('start.html', {'error_message': "Your session had time out. Start again.", }, context_instance=RequestContext(request))
    
    logger.info('<rank> sid: {} , POST:{}'.format(request.session.session_key, request.POST))

    if re.search('Skip', request.POST['answer']):
        return render_to_response('rank.html', {}, context_instance=RequestContext(request))
    
    errors = []
    if not 'cc' in request.POST : 
        errors.append('error_cc')
    if not 'it' in request.POST : 
        errors.append('error_it')                
    if not 'cit' in request.POST : 
        errors.append('error_cit')                
    
    if len(errors) > 0:
        return render_to_response('climate.html', {k : True for k in errors}, context_instance=RequestContext(request))
            
    s = get_object_or_404(Survey, id=request.session['survey_id'])
    s.cc = request.POST['cc']
    s.it = request.POST['it'] 
    s.cit = request.POST['cit'] 
    s.save()
    
    return render_to_response('rank.html', {}, context_instance=RequestContext(request))

@require_http_methods(["POST"])
def rate(request, group=None):
    if not request.session :
        # if it doesn't have a session -> start again
        return render_to_response('start.html', {'error_message': "Your session had time out. Start again.", }, context_instance=RequestContext(request))
    # save the information from the form into the session
    logger.info('<rate> sid: {} , POST:{}'.format(request.session.session_key, request.POST))    
    
    if request.session['type'] == 'survey':
        
        if not re.search('Skip', request.POST['answer']): 
            if not 'rank' in request.POST or not 'confidence' in request.POST : 
                return render_to_response('rank.html', {'error_message':'Please make all selections'}, context_instance=RequestContext(request))                

            s = get_object_or_404(Survey, id=request.session['survey_id'])
            
            s.home_rank = request.POST['rank']                                    
            s.home_rank_confidence = request.POST['confidence']
                    
            s.save()
            
    return render_to_response('rate.html', {}, context_instance=RequestContext(request))

    

def app(request, group=None):
     
    if not request.session :
        # if it doesn't have a session -> start again
        return render_to_response('start.html', {'error_message': "Your session had time out. Start again.", }, context_instance=RequestContext(request))
    # save the information from the form into the session
    logger.info('<app> sid: {} , POST:{}'.format(request.session.session_key, request.POST))    
    
    if request.session['type'] == 'survey':
                
        if not re.search('Skip', request.POST['answer']): 
            if not 'pre_points' in request.POST or request.POST['pre_points'] == -1 \
                or not 'confidence' in request.POST:
                    return render_to_response('rate.html', {'error_message':'Please answer each question.'}, context_instance=RequestContext(request))

            s = get_object_or_404(Survey, id=request.session['survey_id'])
            
            s.survey_date = datetime.datetime.now()            
            s.rating = request.POST['pre_points']
            s.rank_confidence = request.POST['confidence']
            s.save()
            
    return render_to_response('index.html', {'type':request.session['type']}, context_instance=RequestContext(request))

@require_http_methods(["POST"])
def review(request, group=None):    
    #store app data
    
    logger.info('<review> sid: {} , POST:{}'.format(request.session.session_key, request.POST))
    
    s = get_object_or_404(Survey, id=request.session['survey_id'])
    now = datetime.datetime.now()
    s.duration = (now - s.survey_date).total_seconds()
    if 'selections' in request.POST and request.POST['selections'] != '':
        s.selections = createSelections(json.loads(request.POST['selections']))
    s.save()
    
    logger.info('<review> sid: {} , POST:{}'.format(request.session.session_key, request.POST))
    return render_to_response('review.html', {'type':request.session['type']}, context_instance=RequestContext(request))

@require_http_methods(["POST"])
def thankyou(request, group=None):
    if not request.session :
        # if it doesn't have a session -> start again
        return render_to_response('start.html', {'error_message': "Your session had time out. Start again.", }, context_instance=RequestContext(request))
    
    logger.info('<thankyou> sid: {} , POST:{}'.format(request.session.session_key, request.POST))

    if not re.search('Skip', request.POST['answer']): 
        if not 'expect' in request.POST:        
            return render_to_response('review.html', {'error_message':'Please choose one answer'}, context_instance=RequestContext(request))
        
        logger.info('<thankyou> storing info')
        s = get_object_or_404(Survey, id=request.session['survey_id'])                    
        s.expect = request.POST['expect']                                        
        s.save()
            # reset the session information
    del request.session['survey_id']
    
    return render_to_response('thankyou.html', {}, context_instance=RequestContext(request))

def contact(request, group=None):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
#            topic = form.clean_data['topic']
#            message = form.clean_data['message']
#            sender = form.clean_data.get('sender', 'noreply@example.com')
            topic = form.data['topic']
            message = form.data['message']
            sender = form.data.get('sender', 'noreply@example.com')
            c = Contact(topic=topic, message=message, sender=sender)
            c.save()
            return HttpResponseRedirect('/contact/thanks/')
    else:
        form = ContactForm()
    return render_to_response('form.html', {'form': form}, context_instance=RequestContext(request))

    

def createSelections(jsonArray):
    # iterate over all
    list = []
    for json in jsonArray:
        s = Selection(time=json['duration'], connection=json['connection'], device=get_device(json), content=json['service'])
        s.save()    
        list.append(s)
    return list    
                
def get_device(json):
    if json['device'] == 'phone':
        return 'P'
    if json['device'] == 'tablet':
        return 'T'
    if json['device'] == 'laptop':
        return 'L'
    if json['device'] == 'pc':
        return 'D'
    
def export(request):
    html = "<html><body>"
    list = Survey.objects.all()
    
    s = Survey.objects.get(pk=1)
    fields = ""
    for field in ['acc_net', 'age', 'cc', 'cit', 'duration', 'expect', 'gender', 'id', 'internet', 'it', 'laptop', 'pk', 'rank_confidence', 'rate_confidence', 'rating', 'servers', 'survey_date']:        
        fields += field + ","
    
#    fields += s.get_acc_net_display()
    
    html += fields
    html += "<br>"
    for s in list:
        html += "{}, {} , {}, {}, {}, {}, {}, {}, {}, {}, {}, {} , {} , {} , {} , {} , {}".format(s.acc_net, s.age, s.cc, s.cit, s.duration, s.expect, s.gender, s.id, s.internet, s.it, s.laptop, s.pk, s.rank_confidence, s.rate_confidence, s.rating, s.servers, s.survey_date)
        html += "<br>"
    html += "</body></html>"
    return HttpResponse(html)
    
def get_group(name):
    groups = SurveyGroup.objects.all()
    group = groups.filter(name=name)[0]
    return group
