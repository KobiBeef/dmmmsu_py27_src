from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.shortcuts import redirect
from datetime import datetime
from student_registry.models import Category, Page
from student_registry.forms import CategoryForm, PageForm, UserForm, UserProfileForm
from student_registry.bing_search import run_query

# FUNCTIONS
def get_category_list(max_results=0, starts_with=''):
	cat_list = []
	if starts_with:
		# built-in variable name__istartswith=
		cat_list = Category.objects.filter(name__istartswith=starts_with)

	if cat_list and max_results > 0:
		if cat_list.count() > max_results:
			cat_list = cat_list[:max_results]
	return cat_list

# Create your views here.
# NOTE THE KEYWORDS
def index(request):
	# testing cookies
	# request.session.set_test_cookie()

	category_list = Category.objects.order_by('-likes')
	# category_list = Category.objects.all()
	page_list = Page.objects.order_by('-views')
	context_dict = {'categories': category_list, 'page_list': page_list}
	
	# counting visitors
	visits = request.session.get('visits')
	if not visits:
		visits = 1

	reset_last_visit_time = False
	last_visit = request.session.get('last_visit')

	if last_visit:
		last_visit_time = datetime.strptime(last_visit[:-7], "%Y-%m-%d %H:%M:%S")
		if (datetime.now() - last_visit_time).days > 0:
			visits = visits + 1
			reset_last_visit_time = True
	else:
		reset_last_visit_time = True
	
	if reset_last_visit_time:
		request.session['last_visit'] = str(datetime.now())
		request.session['visits'] = visits

	context_dict['visits'] = visits
	response = render(request, 'student_registry/index.html', context_dict)
	return response

	# for debugging purpose
	print ('view index(): context_dict')
	for key, value in context_dict.iteritems():
		print ('key: {0} - value: {1}'.format(key, value))

	return response

def category(request, category_name_slug):
	context_dict = {}
	# if request.method == 'GET':
	# 	if 'category_id' in request.GET:
	# 		print ("im here")
			# print ("type of here: ", type(request.GET))

	# just transfered the search() to category()
	context_dict['result_list'] = None
	context_dict['query'] = None
	if request.method == "POST":
		query = request.POST['query'].strip()
		if query:
			result_list = run_query(query)
			context_dict['result_list'] = result_list
			context_dict['query'] = query
	try:
		# this is where the url got the category_name_slug
		category = Category.objects.get(slug=category_name_slug)
		# context_dict['category_id'] = category.id
		# variable category_name here!
		context_dict['category_name'] = category.name
		context_dict['category_name_slug'] = category.slug
		pages = Page.objects.filter(category=category)
		context_dict['pages'] = pages
		context_dict['category'] = category
	except Category.DoesNotExist:
		pass

	if not context_dict['query']:
		context_dict['query'] = category.name

	# for debugging purpose
	print ('view category(): context_dict')
	for key, value in context_dict.iteritems():
		print ('key: {0} - value: {1}'.format(key, value))

	return render(request, 'student_registry/category.html', context_dict)

def add_category(request):
	if request.method == 'POST':
		form = CategoryForm(request.POST)
		if form.is_valid():
			form.save(commit=True)
			# form.save()
			# cat = form.save(commit=True)
			# good for bug fixing
			# print (cat, cat.slug)
			return index(request)
		else:
			print form.errors
	else:
		form = CategoryForm()
		# variable form is here!
	return render(request, 'student_registry/add_category.html', {'form':form})

def add_page(request, category_name_slug):
	try:
		# category_name_slug assigned to slug or slug is assigned category_name_slug?
		cat = Category.objects.get(slug=category_name_slug)
		# NOTE:
		# I think this: has a naming conflict when calling the --
		# -- category(request, category_name_slug)
		# --> this: category = Category.objects.get(slug=category_name_slug)
		# Is pages creating the error?
		# re: pages is not creating the error naming of category is 
		pages = Page.objects.filter(category=cat)
	except Category.DoesNotExist:
		cat = None
	if request.method == 'POST':
		form = PageForm(request.POST)
		if form.is_valid():
			if category:
				# page is now form
				page = form.save(commit=False)
				page.category = cat
				page.views = 0
				page.save()
				return category(request, category_name_slug)
		else:
			print form.errors
	else:
		form = PageForm()
	context_dict = {'form':form, 'category':cat, 'pages': pages}
	# for debugging purpose
	print ('view add_page(): context_dict')
	for key, value in context_dict.iteritems():
		print ('key: {0} - value: {1}'.format(key, value))
	return render(request, 'student_registry/add_page.html', context_dict)

def register(request):
	# testing cookies
	# if request.session.test_cookie_worked():
	# 	print ">>> TEST COOKIE WORKED!"
	# 	request.session.delete_test_cookie()
		
	registered = False
	if request.method == 'POST':
		user_form = UserForm(data=request.POST)
		profile_form = UserProfileForm(data=request.POST)
		if user_form.is_valid() and profile_form.is_valid():
			# UserFrom()
			user = user_form.save()
			user.set_password(user.password)
			user.save()
			# UserProfileForm()
			profile = profile_form.save(commit=False)
			# UserForm() and UserProfileForm() connected
			profile.user = user
			if 'picture' in request.FILES:
				profile.picture = request.FILES['picture']
			profile.save()
			registered = True
		else:
			print (user_form.errors, profile_form_errors)
	else:
		user_form = UserForm()
		profile_form = UserProfileForm()
	return render(request, 'student_registry/register.html',
		{'user_form': user_form,
		 'profile_form': profile_form,
		 'registered': registered
		})

def user_login(request):
	if request.method == 'POST':
		# gotten from login.html
		# <input name="username">
		# <input name="password">
		username = request.POST.get('username')
		password = request.POST.get('password')
		user = authenticate(username=username, password=password)
		if user:
			if user.is_active:
				login(request, user)
				return HttpResponseRedirect('/student_registry/')
			else:
				return HttpResponse("Your account is disabled")
		else:
			print ("invalid log in details: {0}, {1}".format(username, password))
			return HttpResponse("invalid login details supplied")
	else:
		return render(request, 'student_registry/login.html',{})

@login_required
def restricted(request):
	# See settings.py variable LOGIN_URL
	return HttpResponse("YOU ARE LOGGED IN, can see this text")

@login_required
def user_logout(request):
	logout(request)
	return HttpResponseRedirect('/student_registry/')

def search(request):
	result_list = []
	if request.method == 'POST':
		# gotteng from search.html
		# gotten from '<input name='query'>'
		query = request.POST['query'].strip()
		if query:
			result_list = run_query(query)
	return render(request, 'student_registry/search.html', {'result_list':result_list})

def track_url(request):
	page_id = None
	# url = '/student_registry/'
	if request.method == 'GET':
		# each created Page in django has a built-in page_id?
		# dont know how 'page_id' is possible
		# if its because of the {% url %}?page_id={{page.id}} in category.html?
		if 'page_id' in request.GET:
			page_id = request.GET['page_id']
			print (page_id)
			try:
				page = Page.objects.get(id=page_id)
				page.views = page.views + 1
				page.save()
				url = page.url
			except:
				pass
	# redirect does not work
	# return redirect(url)
	return HttpResponseRedirect('/student_registry/')

@login_required
def like_category(request):
	cat_id = None
	if request.method == 'GET':
		if 'category_id' in request.GET:
			print ('category_id')
			cat_id = request.GET['category_id']
			print (cat_id)

	likes = 0
	if cat_id:
		cat = Category.objects.get(id=int(cat_id))
		if cat:
			likes = cat.likes + 1
			cat.likes = likes
			cat.save()

	# returns to the student_registry-ajax.js
	return HttpResponse(likes)

# still cant figure out how this works
def suggest_category(request):
	cat_list = []
	starts_with = ''
	if request.method == 'GET':
		starts_with = request.GET['suggestion']
	cat_list = get_category_list(8, starts_with)
	print ("test")
	return render(request, 'student_registry/cats.html', {'cat_list': cat_list})

def manage(request):
	return HttpResponse("Manage Page")

def about(request):
	return render(request, 'student_registry/about.html')

def contact(request):
	return HttpResponse("Contact us Page")