from datetime import datetime

from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login,  logout
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse

from rango.models import Category, Page
from .forms import CategoryForm, PageForm, UserForm, UserProfileForm

#def index(request):
#	context_dict = {'boldmessage': "Crunchy, creamy, cookie, candy, cupcake"}
#	return render(request, 'rango/index.html', context = context_dict)

#2 def index(request):
#2 	request.session.set_test_cookie()
#2 	category_list = Category.objects.order_by('-likes')[:5]
#2 	page_list = Page.objects.order_by('-views')[:5]
#2 	context_dict = {'categories': category_list,
#2 					'pages': page_list}

#2 	return render(request, 'rango/index.html', context = context_dict)

#2 add cookie for visits counting
def index(request):
	category_list = Category.objects.order_by('-likes')[:5]
	page_list = Page.objects.order_by('-views')[:5]
	context_dict = {'categories': category_list, 'pages': page_list}

	visitor_cookie_handler(request)
	context_dict['visits'] = request.session['visits']

	response = render(request, 'rango/index.html',  context_dict)
	return response


def about(request):
#	if request.session.test_cookie_worked():
#		print "TEST COOKIE WORKED!"
#		request.session.delete_test_cookie()
	context_dict = {}

	visitor_cookie_handler(request)
	context_dict['visits'] = request.session['visits']
	
	response = render(request, 'rango/about.html', context_dict)
	return response

#	return HttpResponse("""Rango says here is the about page. <br />
#		<a href = '/rango/'>Index</a>
#		""")


def show_category(request, category_name_slug):
	context_dict = {}
	try:
		category = Category.objects.get(slug = category_name_slug)
		pages = Page.objects.filter(category = category).order_by('-views')
		category.views = category.views + 1
		category.save()
		context_dict['category'] = category
		context_dict['pages'] = pages
		
	except Category.DoesNotExist:
		context_dict['category'] = None
		context_dict['pages'] = None
	return render(request, 'rango/category.html', context = context_dict)

# @login_required
def add_category(request):
	form = CategoryForm()

	if request.method == 'POST':
		form = CategoryForm(request.POST)
		if form.is_valid():
			form.save(commit = True)
			return index(request)
		else:
			print(form.errors)

	return render(request, 'rango/add_category.html', { 'form': form })

#@login_required
def add_page(request, category_name_slug):
	try:
		category = Category.objects.get(slug = category_name_slug)
	except Category.DoesNotExist:
		category = None

	form = PageForm()
	if request.method == 'POST':
		form = PageForm(request.POST)
		if form.is_valid():
			if category:
				page = form.save(commit = False)
				page.category = category
				page.views = 0
				page.save()
				return show_category(request, category_name_slug)
		else:
			print form.errors

	context_dict = { 'form': form, 'category': category }
	return render(request, 'rango/add_page.html', context_dict)


def register(request):
	registered = False

	if request.method == 'POST':
		user_form = UserForm(data = request.POST)
		profile_form = UserProfileForm(data = request.POST)

		if user_form.is_valid() and profile_form.is_valid():
			user = user_form.save()
			user.set_password(user.password)
			user.save()
			profile = profile_form.save(commit = False)
			profile.user = user
			if 'picture' in request.FILES:
				profile.picture = request.FILES['picture']
			profile.save()
			registered = True
		else:
			print user_form.errors, profile_form.errors
	else:
		user_form = UserForm()
		profile_form = UserProfileForm()

	return render(request, 'rango/register.html', {
		'user_form': user_form,
		'profile_form': profile_form,
		'registered': registered
		})

def user_login(request):
	if request.method == 'POST':
		username = request.POST.get('username')
		password = request.POST.get('password')
		user = authenticate(username = username, password = password)
		if user:
			if user.is_active:
				login(request, user)
				return HttpResponseRedirect(reverse('index'))
			else:
				return HttpResponse("Your Rango account is disabled.")
		else:
			print "Invalid login details: {0}, {1}". format(username, password)
			return HttpResponse("Invalid login details supplied.")
	else:
		return render(request, 'rango/login.html', {})

@login_required
def restricted(request):
	return HttpResponse("Since you're logged in, you can see this text!")

@login_required
def user_logout(request):
	logout(request)
	return HttpResponseRedirect(reverse('index'))


##2 add cookie for visits counting
#3 def visitor_cookie_handler(request, response):
#3 	visits_cookie = int(request.COOKIES.get('visits', '1'))

#3 	last_visit_cookie = request.COOKIES.get('last_visit', str(datetime.now()))
#3 	last_visit_time = datetime.strptime(last_visit_cookie[:-7], '%Y-%m-%d %H:%M:%S')

#3 	if(datetime.now() - last_visit_time).days > 0 :
#3 		visits = visits_cookie + 1
#3 		response.set_cookie('last_visit', str(datetime.now()))
#3 	else:
#3 		visits = 1
#3 		response.set_cookie('last_visit', last_visit_cookie)

#3 	response.set_cookie('visits', visits)

##3 update to session-based cookie for visits counting
def get_server_side_cookie(request, cookie, default_val = None):
	val = request.session.get(cookie)
	if not val:
		val = default_val
	return val

def visitor_cookie_handler(request):
	visits = int(get_server_side_cookie(request, 'visits', '1'))
	last_visit_cookie = get_server_side_cookie(request, 'last_visit', str(datetime.now()))
	last_visit_time = datetime.strptime(last_visit_cookie[:-7], '%Y-%m-%d %H:%M:%S')

	if (datetime.now() - last_visit_time).days > 0:
		visits = visits + 1
		request.session['last_visit'] = str(datetime.now())
	else:
		request.session['last_visit'] = last_visit_cookie

	request.session['visits'] = visits



def track_url(request):
	page_id = None
	url = '/rango/'
	if request.method == 'GET':
		if 'page_id' in request.GET:
			page_id = request.GET['page_id']
			try:
				page = Page.objects.get(id = page_id)
				page.views = page.views + 1
				page.save()
				url = page.url
			except:
				pass
	return redirect(url)






























