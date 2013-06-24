from django import forms

class ContactForm(forms.Form):
	"""docstring for ContactForm"""
	email = forms.CharField(widget=forms.Textarea)
	contact_group_id = forms.CharField()
	group_name = forms.CharField()
	
	def clean_message(self):
		message = self.cleaned_data['email']
		num_words = len(self.email.split())
		if num_words < 1:
			raise forms.ValidationError("Need email")
		return message
