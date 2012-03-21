from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponseRedirect
from forms import ContactForm
from models import Contact, Survey
import logging
import datetime
from django.core.urlresolvers import reverse
#import pdb;

# Create your views here.
# Get an instance of a logger
logger = logging.getLogger(__name__)

def start(request):   
    if not request.session :
        # if it doesn't have a session -> start again
        return render_to_response('start', {'error_message': "Your session had time out. Start again.", }, context_instance=RequestContext(request))
    request.session['start_time'] = datetime.datetime.now() 
    return render_to_response('start.html', context_instance=RequestContext(request))

def climate(request):
    # no data to show
    if not request.session :
        # if it doesn't have a session -> start again
        return render_to_response('start.html', {'error_message': "Your session had time out. Start again.", }, context_instance=RequestContext(request))
    # save the information from the form into the session
    #request.session
            
    logging.info('view climate w/ {}'.format(request.POST))
    
    if 'gender' in request.POST:
        request.session['gender'] = request.POST['gender']
    else:
        request.session['gender'] = -1
    if 'age' in request.POST:        
        request.session['age'] = request.POST['age']
    else: 
        request.session['age'] = -1
    return render_to_response('climate.html', {}, context_instance=RequestContext(request))
    
def gender(request):

    if not request.session :
        # if it doesn't have a session -> start again
        return render_to_response('start', {'error_message': "Your session had time out. Start again.", }, context_instance=RequestContext(request))             

    if request.POST['type'] == 'Skip survey':
        request.session['type'] = 'skip'
        return render_to_response('index.html', {}, context_instance=RequestContext(request)) 
    
    request.session['type'] = 'survey'
    # no data to show    
    return render_to_response('gender.html', {}, context_instance=RequestContext(request))


def app(request):
    if not request.session :
        # if it doesn't have a session -> start again
        return render_to_response('start.html', {'error_message': "Your session had time out. Start again.", }, context_instance=RequestContext(request))
    # save the information from the form into the session
    logging.info('gender:{}, age: {}'.format(request.session['gender'], request.session['age']))
        #request.session
    
    if request.session['type'] == 'survey' and not 'cc' in request.POST or not 'it' in request.POST : 
        return render_to_response('climate.html', {'error_message':'Please choose one answer'}, context_instance=RequestContext(request))
    
    request.session['cc_pre'] = request.POST['cc']
    request.session['it_pre'] = request.POST['it'] 
#    pdb.set_trace()    
    return render_to_response('index.html', {'type':request.session['type']}, context_instance=RequestContext(request))


def review(request):
    if not request.session :
        # if it doesn't have a session -> start again
        return render_to_response('start.html', {'error_message': "Your session had time out. Start again.", }, context_instance=RequestContext(request))
    # save the information from the form into the session
    #request.session
    
    logging.info('gender:{}, age: {}'.format(request.session['gender'], request.session['age']))
    return render_to_response('review.html', {}, context_instance=RequestContext(request))

def finish(request):
    if not request.session :
        # if it doesn't have a session -> start again
        return render_to_response('start.html', {'error_message': "Your session had time out. Start again.", }, context_instance=RequestContext(request))
#     save the information from the form into the session
    request.session['cc_post'] = request.POST['cc_post']
    request.session['it_post'] = request.POST['it_post']
    
    # save the session information
    s = Survey(cc_pre=request.session['cc_pre'], cc_post=request.session['cc_post'], it_pre=request.session['it_pre'], it_post=request.session['it_post'], age=request.session['age'], gender=request.session['gender'], survey_date=request.session['start_time'])
    s.save()
    return render_to_response('start.html', {}, context_instance=RequestContext(request))

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

    
