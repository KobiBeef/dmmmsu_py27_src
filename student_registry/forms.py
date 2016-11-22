from django import forms
from django.contrib.auth.models import User
from student_registry.models import Page, Category, UserProfile

class CategoryForm(forms.ModelForm):
	name = forms.CharField(max_length=128, help_text="Enter Category Name:")
	views = forms.IntegerField(widget=forms.HiddenInput(), initial=0)
	likes = forms.IntegerField(widget=forms.HiddenInput(), initial=0)
	slug = forms.CharField(widget=forms.HiddenInput(), required=False)

	class Meta:
		model = Category
		fields = ('name', )

class PageForm(forms.ModelForm):
	title = forms.CharField(max_length=128, help_text="Enter Page Title:")
	url = forms.URLField(max_length=200, help_text="Enter Page URL")
	views = forms.IntegerField(widget=forms.HiddenInput(), initial=0)

	# clean() method overriden
	def clean(self):
		# what does this line do again?.. LOL
		cleaned_data = self.cleaned_data
		url = cleaned_data.get('url')
		if url and not url.startswith('http://'):
			url = 'http://' + url
			cleaned_data['url'] = url

		# You must always end the clean() method by returning the reference to 
		# the cleaned_data dictionary
		return cleaned_data

	class Meta:
		model = Page
		fields = ('title', 'url', 'views',)
		exclude = ('category',)

class UserForm(forms.ModelForm):
	password = forms.CharField(widget=forms.PasswordInput())

	class Meta:
		model = User
		fields = ('username', 'email', 'password')

class UserProfileForm(forms.ModelForm):
	class Meta:
		model = UserProfile
		fields = ('website', 'picture')