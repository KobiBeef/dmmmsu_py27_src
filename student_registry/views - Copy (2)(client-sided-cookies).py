from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from datetime import datetime
from student_registry.models import Category, Page
from student_registry.forms import CategoryForm, PageForm, UserForm, UserProfileForm

# Create your views here.
# NOTE THE KEYWORDS

def index(request):
	# testing cookies
	# request.session.set_test_cookie()

	# category_list = Category.objects.order_by('-likes')
	category_list = Category.objects.all()
	page_list = Page.objects.order_by('-views')

	context_dict = {'categories': category_list, 'page_list': page_list}
	# counting visitors
	visits = int(request.COOKIES.get('visits', '1'))
	reset_last_visit_time = False
	context_dict['visits'] = visits
	response = render(request, 'student_registry/index.html', context_dict)
	if 'last_visit' in request.COOKIES:
		last_visit = request.COOKIES['last_visit']
		last_visit_time = datetime.strptime(last_visit[:-7], "%Y-%m-%d %H:%M:%S")
		if (datetime.now() - last_visit_time).days > 0:
			visits = visits + 1
			reset_last_visit_time =True
	else:
		reset_last_visit_time = True
		# context_dict['visits'] = visits
		response = render(request, 'student_registry/index.html', context_dict)

	if reset_last_visit_time:
		response.set_cookie('last_visit', datetime.now())
		response.set_cookie('visits', visits)
	
	# for debugging purpose
	print ('view index(): context_dict')
	for key, value in context_dict.iteritems():
		print ('key: {0} - value: {1}'.format(key, value))

	return response

def category(request, category_name_slug):
	context_dict = {}
	try:
		# this is where the url got the category_name_slug
		category = Category.objects.get(slug=category_name_slug)
		# variable category_name here!
		context_dict['category_name'] = category.name
		context_dict['category_name_slug'] = category.slug
		pages = Page.objects.filter(category=category)
		context_dict['pages'] = pages
		context_dict['category'] = category
	except Category.DoesNotExist:
		pass
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

def manage(request):
	return HttpResponse("Manage Page")
def about(request):
	return render(request, 'student_registry/about.html')

def contact(request):
	return HttpResponse("Contact us Page")