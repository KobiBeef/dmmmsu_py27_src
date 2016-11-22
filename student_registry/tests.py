from django.test import TestCase
from student_registry.models import Category

# Create your tests here.

class CategoryMethodTests(TestCase):
	def test_ensure_views_are_positive(self):
		category = Category(name="Python", views=-1, likes=0)
		category.save()
		self.assertEqual((category.views >=0), True)

	def test_slug_line_creation(self):
		category = Category(slug='Random Category String')
		print (category.slug)
		category.save()
		self.assertEqual(category.slug, 'random-category-string')