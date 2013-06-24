#!/usr/bin/env python
# coding: utf-8
# casper@2013/05/27

from django.db import models
# from django.db import connection

class Product(models.Model):
    """
    产品
    """
    title = models.CharField(max_length=100, verbose_name="名称")
    description = models.TextField(verbose_name="描述")
    price = models.DecimalField(max_digits=8, decimal_places=2,null=True,verbose_name="价格")

    def __unicode__(self):
        return self.title

class images(models.Model):
    title = models.CharField(max_length=200, null=True, verbose_name="标题")
    image_url = models.CharField(max_length=200, verbose_name="图片地址")
    product = models.ForeignKey(Product)

    def __unicode__(self):
        return self.image_url

class ContactGroup(models.Model):
    name = models.CharField(max_length=100)
    
    def __unicode__(self):
        return "%s(%s)" % (self.name, self.member_count())
    
    def member_count(self):
        return self.contact_set.count()
    
class Contact(models.Model):
    """
    联系人
    """
    email = models.CharField(max_length=100)
    name = models.CharField(max_length=100, null=True)
    depart = models.CharField(max_length=255, null=True)
    address = models.CharField(max_length=255, null=True)
    telphone = models.CharField(max_length=100, null=True)

    contact_group = models.ForeignKey(ContactGroup)

    def __unicode__(self):
        return self.email

class Poll(models.Model):
    """
    调查
    """
    title = models.CharField(max_length=100)
    comments = models.CharField(max_length=200, null=True)
    pub_date = models.DateTimeField('Date published')
    template = models.TextField()

    # 多对多 Product & contacts
    products = models.ManyToManyField(Product)
    contact_group_list = models.ManyToManyField(ContactGroup)
    # todo: status = 
    class Meta:
        ordering = ['-pub_date']

    def __unicode__(self):
        return self.title

    def null_answer(self):
        return self.answer_set.filter(update_date__isnull=True)

    def not_null_answer(self):
        return self.answer_set.filter(update_date__isnull=False)

    def progress(self):
        """ 进展 """
        total = self.answer_set.count()
        completed = self.answer_set.filter(update_date__isnull=False).count()
        progress_percent = 0
        if total != 0:
            progress_percent = completed * 100 / total
        # print "total:%s completed:%s progress_percent:%s" %(total, completed, progress_percent)
        return progress_percent
    
#     def sum(self, product_id):
#         cursor = connection.cursor()
#         cursor.execute("""
#             select ifnull(sum(b.count),0) cnt
#   from pollapp_answer a, pollapp_answeritem b
#  where a.id = b.answer_id
#    and a.poll_id = %s
# group by b.product_id = %s""", [self.id, product_id])
#         cnt = cursor.fetchone()
#         if cnt:
#             return cnt[0]
#         else:
#             return 0
#     
#     def count(self):
#         ret = {}
#         for product in self.products.all():
#             ret[product] = self.sum(product_id=product.id)
#         print "product=%s,count=%s" %(product.title, ret[product])
#         return ret
    
class Answer(models.Model):
    """ 回复 """
    poll = models.ForeignKey(Poll)
    contact = models.ForeignKey(Contact)
    code = models.CharField(max_length=100)
    update_date = models.DateTimeField('Answer updated', null=True)
    
    def __unicode__(self):
        return "%s" % self.contact.name 

class AnswerItem(models.Model): 
    """ 产品+数量 """
    answer = models.ForeignKey(Answer)
    product = models.ForeignKey(Product)
    count = models.IntegerField(default=0)

    def __unicode__(self):
        return "product:%s, count:%s" % (self.product.title, self.count)