from django import template
from student_registry.models import Category

register = template.Library()

@register.inclusion_tag('student_registry/cats.html')
def get_category_list(cat=None):
	return {'cats': Category.objects.all(), 'active_category': cat}