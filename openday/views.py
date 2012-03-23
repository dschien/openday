from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from django.http import HttpResponseRedirect
from forms import ContactForm
from models import Contact, Survey, Selection
import logging
import datetime
from django.core.urlresolvers import reverse
import re
import json
#import pdb;

# Create your views here.


def start(request):
           
    if not request.session :
        # if it doesn't have a session -> start again
        return render_to_response('start', {'error_message': "Your session had time out. Start again.", }, context_instance=RequestContext(request))        
        
    logging.info('<start> : {}'.format(request.session.session_key)) 
    return render_to_response('start.html', context_instance=RequestContext(request))
    del request.session['type']
    
def gender(request):

    if not request.session :
        # if it doesn't have a session -> start again
        return render_to_response('start', {'error_message': "Your session had time out. Start again.", }, context_instance=RequestContext(request))             
    logging.info('<gender> sid: {} , POST:{}'.format(request.session.session_key, request.POST))

    if 'survey_id' in request.session:
        del request.session['survey_id']

    if request.POST['answer'] == 'Skip survey':
        request.session['type'] = 'skip'
#        return render_to_response('index.html', {}, context_instance=RequestContext(request))
        return HttpResponseRedirect(reverse('openday.views.app'))
    
    # create new survey
    s = Survey() 
    s.survey_date = datetime.datetime.now()
    s.save()
    request.session['survey_id'] = s.id
    request.session['type'] = 'survey'
    # no data to show    
    return render_to_response('gender.html', {}, context_instance=RequestContext(request))

def climate(request):
    # no data to show
    if not request.session:
        # if it doesn't have a session -> start again
        return render_to_response('start.html', {'error_message': "Your session had time out. Start again.", }, context_instance=RequestContext(request))
    # save the information from the form into the session                
    logging.info('<climate> sid: {} , POST:{}'.format(request.session.session_key, request.POST))        
    
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

def rank(request):
    if not request.session :
        # if it doesn't have a session -> start again
        return render_to_response('start.html', {'error_message': "Your session had time out. Start again.", }, context_instance=RequestContext(request))
    
    logging.info('<rank> sid: {} , POST:{}'.format(request.session.session_key, request.POST))

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

def rate(request):
    if not request.session :
        # if it doesn't have a session -> start again
        return render_to_response('start.html', {'error_message': "Your session had time out. Start again.", }, context_instance=RequestContext(request))
    # save the information from the form into the session
    logging.info('<rate> sid: {} , POST:{}'.format(request.session.session_key, request.POST))    
    
    if request.session['type'] == 'survey':
        
        if not re.search('Skip', request.POST['answer']): 
            if not all([ key in request.POST for key in ['pre_servers', 'pre_laptop', 'pre_acc_net', 'pre_internet']]) \
                or not all([  request.POST[key] > 0 for key in ['pre_servers', 'pre_laptop', 'pre_acc_net', 'pre_internet']]) \
                    or not 'confidence' in request.POST:
                        return render_to_response('rank.html', {'error_message':'Please make all selections'}, context_instance=RequestContext(request))

            s = get_object_or_404(Survey, id=request.session['survey_id'])
            
            s.servers = request.POST['pre_servers']                        
            s.laptop = request.POST['pre_laptop']
            s.acc_net = request.POST['pre_acc_net']
            s.internet = request.POST['pre_internet']
            s.rate_confidence = request.POST['confidence']
                    
            s.save()
            
    return render_to_response('rate.html', {}, context_instance=RequestContext(request))

    

def app(request):
     
    if not request.session :
        # if it doesn't have a session -> start again
        return render_to_response('start.html', {'error_message': "Your session had time out. Start again.", }, context_instance=RequestContext(request))
    # save the information from the form into the session
    logging.info('<app> sid: {} , POST:{}'.format(request.session.session_key, request.POST))    
    
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

def review(request):    
    #store app data
    
    logging.info('<review> sid: {} , POST:{}'.format(request.session.session_key, request.POST))
    
    s = get_object_or_404(Survey, id=request.session['survey_id'])
    now = datetime.datetime.now()
    s.duration = (now - s.survey_date).total_seconds()
    if 'selections' in request.POST and request.POST['selections'] != '':
        s.selections = createSelections(json.loads(request.POST['selections']))
    s.save()
    
    logging.info('<review> sid: {} , POST:{}'.format(request.session.session_key, request.POST))
    return render_to_response('review.html', {'type':request.session['type']}, context_instance=RequestContext(request))


def thankyou(request):
    if not request.session :
        # if it doesn't have a session -> start again
        return render_to_response('start.html', {'error_message': "Your session had time out. Start again.", }, context_instance=RequestContext(request))
    
    logging.info('<thankyou> sid: {} , POST:{}'.format(request.session.session_key, request.POST))

    if not 'expect' in request.POST:        
        return render_to_response('review.html', {'error_message':'Please choose one answer'}, context_instance=RequestContext(request))
    
    logging.info('<thankyou> storing info')
    s = get_object_or_404(Survey, id=request.session['survey_id'])                    
    s.expect = request.POST['expect']                        
            
    s.save()
        # reset the session information
    del request.session['survey_id']
    
    return render_to_response('thankyou.html', {}, context_instance=RequestContext(request))

def contact(request):
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
    
