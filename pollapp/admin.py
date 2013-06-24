# coding=utf-8

from django.contrib import admin
from pollapp.models import Poll, ContactGroup, Contact, Product, Answer, AnswerItem, images

class AnswerItemInline(admin.StackedInline):
	model = AnswerItem

class AnswerAdmin(admin.ModelAdmin):
	inlines = [AnswerItemInline]
	
class AnswerInline(admin.StackedInline):
	model = Answer
		
class PollAdmin(admin.ModelAdmin):
	inlines = [AnswerInline]
	# 定制列表字段
	list_display = ('title', 'pub_date')
	# 搜索
	search_fields = ['title']
	# 日期折叠
	date_hierarchy = 'pub_date'

class ContactInline(admin.StackedInline):
	model = Contact
		
class ContactGroupAdmin(admin.ModelAdmin):
	inlines = [ContactInline]
	list_display = ('name',)	

class ImageInline(admin.StackedInline):
	model = images
	
class ProductAdmin(admin.ModelAdmin):
	inlines = [ImageInline]
	list_display = ('title','description','price')
	
admin.site.register(Poll, PollAdmin)
admin.site.register(Answer, AnswerAdmin)
admin.site.register(ContactGroup, ContactGroupAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(AnswerItem)