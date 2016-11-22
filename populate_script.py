import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'dmmmsu_py27_src.settings')

import django
django.setup()

from student_registry.models import Category, Page

def populate():
	python_category = add_category('Python')

	add_page(category=python_category,
		title="Official Python Tutorial",
		url="http://docs.python.org/2/tutorial/")

	add_page(category=python_category, 
		title="How to Think like a Computer Scientist",
		url="http://www.greenteapress.com/thinkpython/")

	add_page(category=python_category,
        title="Learn Python in 10 Minutes",
        url="http://www.korokithakis.net/tutorials/python/")

	django_category = add_category("Django")

	add_page(category=django_category,
        title="Official Django Tutorial",
        url="https://docs.djangoproject.com/en/1.5/intro/tutorial01/")

	add_page(category=django_category,
        title="Django Rocks",
        url="http://www.djangorocks.com/")

	add_page(category=django_category,
        title="How to Tango with Django",
        url="http://www.tangowithdjango.com/")

	framework_category = add_category("Other Frameworks")

	add_page(category=framework_category,
        title="Bottle",
        url="http://bottlepy.org/docs/dev/")

	add_page(category=framework_category,
        title="Flask",
        url="http://flask.pocoo.org")

	for category in Category.objects.all():
		for page in Page.objects.filter(category=category):
			print ("- {0} - {1}".format(str(category), str(page)))

def add_page(category, title, url, views=0):
	page = Page.objects.get_or_create(category=category, title=title)[0]
	page.url = url
	page.views = views
	page.save()
	return page

def add_category(name, likes=0, views=0):
	category = Category.objects.get_or_create(name=name, likes=likes, views=views)[0]
	category.save()
	return category

if __name__ == '__main__':
	print "Starting poputation script"
	populate()