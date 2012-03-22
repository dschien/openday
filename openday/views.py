from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from django.http import HttpResponseRedirect
from forms import ContactForm
from models import Contact, Survey
import logging
import datetime
from django.core.urlresolvers import reverse
import re
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

    if request.POST['type'] == 'Skip survey':
        request.session['type'] = 'skip'
#        return render_to_response('index.html', {}, context_instance=RequestContext(request))
        return HttpResponseRedirect(reverse('openday.views.app'))
 
    
    request.session['type'] = 'survey'
    # no data to show    
    return render_to_response('gender.html', {}, context_instance=RequestContext(request))

def climate(request):
    # no data to show
    if not request.session :
        # if it doesn't have a session -> start again
        return render_to_response('start.html', {'error_message': "Your session had time out. Start again.", }, context_instance=RequestContext(request))
    # save the information from the form into the session                
    logging.info('<climate> sid: {} , POST:{}'.format(request.session.session_key, request.POST))        
    
    s = Survey()     
    s.gender = request.POST['gender'] if 'gender' in request.POST else -1  
    s.age = request.POST['age'] if 'age' in request.POST else -1
    s.survey_date = datetime.datetime.now()
    
    s.save()
    request.session['survey_id'] = s.id
    
    return render_to_response('climate.html', {}, context_instance=RequestContext(request))

def prepower(request):
    if not request.session :
        # if it doesn't have a session -> start again
        return render_to_response('start.html', {'error_message': "Your session had time out. Start again.", }, context_instance=RequestContext(request))
    
    logging.info('<prepower> sid: {} , POST:{}'.format(request.session.session_key, request.POST))

    if re.search('Skip', request.POST['type']):
        return render_to_response('prepower.html', {}, context_instance=RequestContext(request))
    
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
    
    return render_to_response('prepower.html', {}, context_instance=RequestContext(request))

def app(request):
     
    if not request.session :
        # if it doesn't have a session -> start again
        return render_to_response('start.html', {'error_message': "Your session had time out. Start again.", }, context_instance=RequestContext(request))
    # save the information from the form into the session
    logging.info('<app> sid: {} , POST:{}'.format(request.session.session_key, request.POST))    
    
    if request.session['type'] == 'survey':
        t = request.POST['type']
        logging.debug(t)
        if not re.search('Skip', request.POST['type']): 
            if not all([ key in request.POST for key in ['pre_servers', 'pre_laptop', 'pre_acc_net', 'pre_internet', 'pre_points']]) \
                or any([ re.search('Please select', request.POST[key]) for key in ['pre_servers', 'pre_laptop', 'pre_acc_net', 'pre_internet', 'pre_points']]):
                    return render_to_response('prepower.html', {'error_message':'Please choose one answer'}, context_instance=RequestContext(request))

            s = get_object_or_404(Survey, id=request.session['survey_id'])
            
            s.pre_servers = request.POST['pre_servers']                        
            s.pre_laptop = request.POST['pre_laptop']
            s.pre_acc_net = request.POST['pre_acc_net']
            s.pre_internet = request.POST['pre_internet']
    
            # has opt'ed out?        
            if request.POST['opt_out'] == 1:
                s.pre_points = -1
            s.pre_points = request.POST['pre_points']
                    
            s.save()
            
    return render_to_response('index.html', {'type':request.session['type']}, context_instance=RequestContext(request))

def branch(request):    
    #store app data
    logging.info('<branch> sid: {} , POST:{}'.format(request.session.session_key, request.POST))
    return render_to_response('branch.html', {'type':request.session['type']}, context_instance=RequestContext(request))


def postpower(request):
    if not request.session :
        # if it doesn't have a session -> start again
        return render_to_response('start.html', {'error_message': "Your session had time out. Start again.", }, context_instance=RequestContext(request))
    
    logging.info('<postpower> sid: {} , POST:{}'.format(request.session.session_key, request.POST))
    
    # if branched, go to thankyou
    if request.POST['next'] == 'thankyou':
        # go there
        return thankyou(request, nav='skip_pp')
        
    return render_to_response('postpower.html', {}, context_instance=RequestContext(request))

def thankyou(request, nav=None):
    if not request.session :
        # if it doesn't have a session -> start again
        return render_to_response('start.html', {'error_message': "Your session had time out. Start again.", }, context_instance=RequestContext(request))
    
    logging.info('<thankyou> sid: {} , POST:{}'.format(request.session.session_key, request.POST))

    if nav == 'skip_pp':
        logging.info('<thankyou> - post power question was skipped')
    else:
        if not all([ key in request.POST for key in ['post_servers', 'post_laptop', 'post_acc_net', 'post_internet', 'post_points']]) \
            or any([ re.search('Please select', request.POST[key]) for key in ['post_servers', 'post_laptop', 'post_acc_net', 'post_internet', 'post_points']]):        
            return render_to_response('postpower.html', {'error_message':'Please choose one answer'}, context_instance=RequestContext(request))
        
        logging.info('<thankyou> storing power power info')
        s = get_object_or_404(Survey, id=request.session['survey_id'])        
        s.post_servers = request.POST['post_servers']                        
        s.post_laptop = request.POST['post_laptop']
        s.post_acc_net = request.POST['post_acc_net']
        s.post_internet = request.POST['post_internet']
        
        # has opt'ed out?        
        if request.POST['opt_out'] == 1:
            s.pre_points = -1        
        s.post_points = request.POST['post_points']
                
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

    
