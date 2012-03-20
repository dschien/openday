from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponseRedirect
from django.core.mail import send_mail
from forms import ContactForm
from models import Contact
import logging

# Create your views here.
# Get an instance of a logger
logger = logging.getLogger(__name__)

def start(request):    
    return render_to_response('start.html', context_instance=RequestContext(request))

def climate(request):
    # no data to show
    if not request.session :
        # if it doesn't have a session -> start again
        return render_to_response('start.html', {'error_message': "Your session had time out. Start again.", }, context_instance=RequestContext(request))
    # save the information from the form into the session
    #request.session
    return render_to_response('climate.html', {}, context_instance=RequestContext(request))
    
def gender(request):
    # no data to show    
    if not request.session :
        # if it doesn't have a session -> start again
        return render_to_response('start.html', {'error_message': "Your session had time out. Start again.", }, context_instance=RequestContext(request))

    logger.debug(request['gender'])    
    request.session['gender'] = request['gender'] 
        
    return render_to_response('gender.html', {}, context_instance=RequestContext(request))
    
def gender2(request):
    # no data to show    
    if not request.session :
        # if it doesn't have a session -> start again
        return render_to_response('start.html', {'error_message': "Your session had time out. Start again.", }, context_instance=RequestContext(request))    
    return render_to_response('gender.html', {}, context_instance=RequestContext(request))


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


def app(request):
    if not request.session :
        # if it doesn't have a session -> start again
        return render_to_response('start.html', {'error_message': "Your session had time out. Start again.", }, context_instance=RequestContext(request))
    # save the information from the form into the session
    
        #request.session
    return render_to_response('index.html', {}, context_instance=RequestContext(request))


def review(request):
    if not request.session :
        # if it doesn't have a session -> start again
        return render_to_response('start.html', {'error_message': "Your session had time out. Start again.", }, context_instance=RequestContext(request))
    # save the information from the form into the session
    #request.session
    return render_to_response('review.html', {}, context_instance=RequestContext(request))

def finish(request):
    if not request.session :
        # if it doesn't have a session -> start again
        return render_to_response('start.html', {'error_message': "Your session had time out. Start again.", }, context_instance=RequestContext(request))
#     save the information from the form into the session
    
    # save the session information    
    return render_to_response('start.html', {}, context_instance=RequestContext(request))
