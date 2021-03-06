from django.db import models
from django.template.defaultfilters import slugify
from django.contrib.auth.models import User

# Create your models here.
class Category(models.Model):
	name = models.CharField(max_length=128, unique=True)
	likes = models.IntegerField(default=0)
	views = models.IntegerField(default=0)
	slug = models.SlugField()

	def save(self, *args, **kwargs):
		if self.id is None:
			self.slug = slugify(self.name)
		self.slug = slugify(self.name)
		super(Category, self).save(*args, **kwargs)

	def __str__(self):
		return self.name

	class Meta():
		verbose_name = "Category"
		verbose_name_plural = "Categories"

class Page(models.Model):
	category = models.ForeignKey(Category)
	title = models.CharField(max_length=128)
	url = models.URLField(max_length=200)
	views = models.IntegerField(default=0)

	def __str__(self):
		return self.title

	class Meta():
		verbose_name = "Page"
		verbose_name_plural = "Pages"

class UserProfile(models.Model):
	user = models.OneToOneField(User)
	website = models.URLField(blank=True)
	picture = models.ImageField(upload_to='profile_image', blank=True)

	def __str__(self):
		return self.user.username