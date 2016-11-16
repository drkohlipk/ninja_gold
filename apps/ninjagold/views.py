from django.shortcuts import render, redirect
import random, time, pytz
from datetime import datetime
from pytz import timezone
from tzlocal import get_localzone

def index(request):
	try: #attempt to add request.session values to the context...if they've been initialized
		context = {
			'gold' : request.session['gold'],
			'activities' : request.session['activities']
		}
	except KeyError: #if they haven't been initialized, define gold!...but not activities (to have the correct display on index.html)
		request.session['gold'] = 0
		context = {
			'gold' : request.session['gold']
		}

	return render(request, 'ninjagold/index.html', context) #render the index.html page with context

def processgold(request, place):
	#########get and set local time stamp (django workaround...)#########
	local_tz = get_localzone()
	ts = time.time()
	utc_now= datetime.utcfromtimestamp(ts)
	local_now = utc_now.replace(tzinfo=pytz.utc).astimezone(local_tz)
	request.session['time'] = local_now.strftime('%b %-d, %Y at %-I:%M:%S %p')
	#########get and set local time stamp (django workaround...)#########

	if 'activities' not in request.session: #if request.session['activities'] doesn't already exit, make it
		request.session['activities'] = []

	places = { #create an object for places and their corresponding randomly generated gold values
		'farm' : random.randint(10,20),
		'cave' : random.randint(5,10),
		'house' : random.randint(2,5),
		'casino' : random.randint(-50,50)
	}

	result = places[place] #set result equal to the gold generated for the specific place clicked on
	activity = { #create activity dictionary for this specific place visited this click
		'class' : 'red' if result < 0 else 'green', #if result is negative, make class red, if not, make it green
		'activity' : 'You entered a {} and lost {} golds... Ouch...'.format(place, result) if result < 0 else 'Earned {} golds from the {}!'.format(result, place),
		'time' : request.session['time'],
	}

	request.session['gold'] += result # add result to the already collected gold
	request.session['activities'].insert(0, activity) #prepend the activity dictionary to request.session['activities']

	return redirect('/')

def reset(request):
	try: #assuming request.session has been at least initalized...clear it!
		request.session.clear()
		return redirect('/')
	except KeyError: #otherwise, just head back to index.html
		return redirect('/')
