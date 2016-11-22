from django.shortcuts import render
from student_registry.models import Category, Page
from student_registry.forms import CategoryForm, PageForm
from django.http import HttpResponse

# Create your views here.
# Initial views
def index(request):
	category_list = Category.objects.order_by('-likes')
	context_dict = {'categories': category_list}
	return render(request, 'student_registry/index.html', context_dict)

#######################################################################################
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
	return render(request, 'student_registry/category.html', context_dict)

def category_test(request, category_name_slug):
    context_dict = {}
    try:
        category = Category.objects.get(slug=category_name_slug)
        context_dict['category_name'] = category.name
        context_dict['category_name_slug'] = category_name_slug
        pages = Page.objects.filter(category=category)
        context_dict['pages'] = pages
        context_dict['category'] = category
    except Category.DoesNotExist:
        pass
    # Go render the response and return it to the client.
    print context_dict
    return render(request, 'student_registry/category_test.html', context_dict)
#######################################################################################

def about(request):
	return render(request, 'student_registry/about.html')

def contact(request):
	return HttpResponse("Contact us Page")

def manage(request):
	return HttpResponse("Manage Page")

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

#######################################################################################
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
	return render(request, 'student_registry/add_page.html', context_dict)

def add_page_test(request, category_name_slug):
    try:
        cat = Category.objects.get(slug=category_name_slug)
    except Category.DoesNotExist:
    	cat = None

    if request.method == 'POST':
        form = PageForm(request.POST)
        if form.is_valid():
            if cat:
                page = form.save(commit=False)
                page.category = cat
                page.views = 0
                page.save()
                return category_test(request, category_name_slug)
        else:
            print form.errors
    else:
        form = PageForm()
    # made the change here
    context_dict = {'form':form, 'category': cat, 'category_name_slug': category_name_slug}
    return render(request, 'student_registry/add_page_test.html', context_dict)
#######################################################################################