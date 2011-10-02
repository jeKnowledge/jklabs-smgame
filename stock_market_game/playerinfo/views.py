# Create your views here.
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
from social_auth.backends import BACKENDS
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout

from gamecore.models import MenuItem, GEvent
from models import UserCredit

DEFAULT_CREDITS=1000

def home(request):
	if request.user.is_authenticated():
		return HttpResponseRedirect('dashboard')
	else:
		backends=[]
		for name, backend in BACKENDS.iteritems():
			if name == 'facebook':
				backends.append((name,backend))
				break
		return render_to_response('home.html',{'backends':backends},RequestContext(request))

@login_required
def dashboard(request):
	total_credits=UserCredit.objects.filter(user=request.user)
	if len(total_credits) == 0:
		inicial_credits=UserCredit(user=request.user, current_credits=DEFAULT_CREDITS)
		inicial_credits.save()
		total_credits=inicial_credits
	else:
		total_credits=total_credits[0]

	menu_items=MenuItem.objects.all()
	last_events=GEvent.objects.all()[:20]
	return render_to_response('dash.html',{'user':request.user.username,
											'name':request.user.first_name,'menu_items':menu_items, 'credits':total_credits.current_credits, 'last_events':last_events},
											RequestContext(request))
	
@login_required
def exit_game(request):
	logout(request)
	return HttpResponseRedirect('/')
		
