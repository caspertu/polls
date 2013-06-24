#!/usr/bin/env python
# coding: utf-8
# casper@2013/05/27

import os

from django.shortcuts import get_object_or_404, render, render_to_response
from django.template import RequestContext
from django.contrib.auth import authenticate, login, logout
from django.utils import timezone
from django.core import mail
from django.http import HttpResponseRedirect

from rest_framework import generics
from pollapp.serializers import ContactSerializer
from pollapp.models import Poll, Answer, AnswerItem, Contact, Product, ContactGroup
from pollapp.forms import ContactForm

class ContactList(generics.ListCreateAPIView):
    model = Contact
    serializer_class = ContactSerializer

class ContactDetail(generics.RetrieveUpdateDestroyAPIView):
    model = Contact
    serializer_class = ContactSerializer

def contact(request):

    # poll = request.session.get('poll', None)
    return render_to_response('pollapp/contact.html', 
        {'all_contact_list': Contact.objects.all(),
        'contact_list': Contact.objects.all(),
         'contact_group_list': ContactGroup.objects.all(),
         },
        context_instance=RequestContext(request))

def group_detail(request,pk=None):
    contact_list = Contact.objects.filter(contact_group=pk)
    return render_to_response('pollapp/contact.html', 
        {'contact_list': contact_list,
         'all_contact_list': Contact.objects.all(),
         'contact_group_list': ContactGroup.objects.all(),
         },
        context_instance=RequestContext(request))

def display_signin_page(request):
    return render_to_response('registration/login.html',
        {},
        context_instance=RequestContext(request))

def my_login(request):
    username = request.POST['username']
    password = request.POST['password']
    user = authenticate(username=username, password=password)
    print "username:%s %s" % (username, password)
    if user is not None:
        if user.is_active:
            login(request, user)
            return HttpResponseRedirect('/polls/list')
        else:
            # Return a 'disabled account' error message
            return display_signin_page(request)
    else:
        # Return an 'invalid login' error message.
        return display_signin_page(request)

def my_logout(request):
    logout(request)
    return display_signin_page(request)

def poll_list(request):
    """ 调查列表 """
    poll_list = Poll.objects.all()
#     for poll in poll_list:
#         for product in poll.products.all():
#             product.count = poll.sum(product.id)
#             print "%s:%s" %(product.title, product.count)
            
    return render_to_response('pollapp/poll.html', 
        {
        'poll_list': poll_list, 
        },
        context_instance=RequestContext(request)) 

def poll_analysis(request):
    """ 分析 """
    poll_list = Poll.objects.all
    return render_to_response('pollapp/analysis.html', 
        {
        'poll_list': poll_list, 
        'product_list': Product.objects.all(),
        },
        context_instance=RequestContext(request)) 

def poll_detail(request, pk):
    """ 调查详情 """
    poll = get_object_or_404(Poll, pk=pk)
    request.session['poll'] = poll
    return render_to_response('pollapp/detail.html',
        {'poll': poll,},
        context_instance=RequestContext(request))

def poll_guest_answer(request, code=None):
    """ 答复界面 
        /pollapp/s/code
    """
    print "code:%s" % code
#     poll = request.session.get('poll')
    answer = get_object_or_404(Answer, code=code)
    request.session['answer'] = answer
    return render_to_response('pollapp/poll_answer.html',
        {'poll': answer.poll,
        'contact': answer.contact,
        'answer': answer,
        },
        context_instance=RequestContext(request))

def poll_answer_update(request, code=None):
    answer = request.session.get('answer')
    answer.update_date = timezone.now()
    answer.save()

    product_id_list = request.POST.getlist('product')
    for product_id in product_id_list:
        print "product_id:%s, count:%s" % (product_id, request.POST.get(product_id))
        product = get_object_or_404(Product, pk=product_id)
        count = request.POST.get(product_id)

        if request.POST.get('update'):
            print 'answer.id:%s' %request.POST.get('s'+product_id)
            item = get_object_or_404(AnswerItem, pk=request.POST.get('s'+product_id))
            print 'item:%s' %item.answer
            count = request.POST.get(product_id, None)
            if count:
                item.count = count
            else:
                item.count = 0
            item.save()
        else:
            item = AnswerItem(answer=answer, product=product, count=count)
            item.save()
    
    return render(request, 'pollapp/poll_update.html', {'answer': answer, })

def poll_new(request):
    return render_to_response('pollapp/poll_new.html',
        {'product_list': Product.objects.all(),
         'contact_group_list': ContactGroup.objects.all(),},
        context_instance=RequestContext(request))

def create(request):
    return render_to_response('pollapp/poll.html', {'product_list': Product.objects.all()}, context_instance=RequestContext(request))

def poll_save(request):
    if request.method == 'POST':
        title = request.POST.get('title', None)
        comments = request.POST.get('comments', None)
        template = request.POST.get('template', None)
        now = timezone.now()
        poll = Poll(title=title, comments=comments, pub_date=now, template=template)
        poll.save()
    
        for key in request.POST:
            print "key:%s value:%s" %(key, request.POST.get(key))
#         print "request.POST.getlist('product')=%s" %request.POST.getlist('product')
    
        for pk in request.POST.getlist('product'):
            product = Product.objects.get(pk=pk)
            poll.products.add(product)
        
        for pk in request.POST.getlist('contact_group'):
            contact_group = ContactGroup.objects.get(pk=pk)
            poll.contact_group_list.add(contact_group)
    
        poll.save()
    
        message = u'您已经成功保存调查:%s' % title
        request.session['poll'] = poll
        
        return my_send_mail(request)

    return render_to_response('pollapp/poll.html', 
        {'poll': poll,
         'poll_list': Poll.objects.all(),
         'contact_list': Contact.objects.all(),
         'form': ContactForm(),
         'message': message,
        }, 
        context_instance=RequestContext(request))

# def contact(request):
#     contact_list = Contact.objects.all()
#     poll = request.session.get('poll', None)
#     form = ContactForm()
#     return render_to_response('pollapp/contact.html', 
#         {'contact_list': contact_list, 
#         'poll': poll,
#         'form': form, },
#         context_instance=RequestContext(request))

def contact_add(request):
    """ 
    新增联系人 
        格式: email, name \n
    """    
    if request.method == 'POST':
        # 调用send_mail
        if (request.POST.get('send_mail', None)):
            return my_send_mail(request)

        for key in request.POST:
            print "key:%s,value:%s" %(key, request.POST.get(key))

        form = ContactForm(request.POST)
        if form.is_valid():
            contact_group = None
            contact_group_id = form.cleaned_data['contact_group_id']
            if contact_group_id == "0":
                group_name = form.cleaned_data['group_name']
                contact_group = ContactGroup(name=group_name)
                contact_group.save()
                print "contact_group created %s" %contact_group.name
            else:
                contact_group = ContactGroup.objects.get(pk=contact_group_id)
                print "contact_group got %s" %contact_group.name
            lines = form.cleaned_data['email']
            str_contact_list = lines.split('\n')
            for str_contact in str_contact_list:
                print 'str_contact:%s' % str_contact
                email = str_contact
                name = ''

                if str_contact.find(',') > -1:
                    fields = str_contact.split(',')
                    email = fields[0]
                    name = fields[1]
                    address = fields[2]
                    depart = fields[3]
                    telphone = fields[4]
                    contact = Contact(contact_group=contact_group, email=email.strip(), name=name.strip(),
                                  address=address, depart=depart, telphone=telphone)
                    contact.save()
                    
    return render_to_response('pollapp/contact.html', 
        {'form': ContactForm(),
         'contact_group_list': ContactGroup.objects.all(),
         'all_contact_list': Contact.objects.all(),
         'contact_list': Contact.objects.all(),
         },
        context_instance=RequestContext(request))

def my_send_mail(request):
    """
        生成随机代码
        发送邮件
    """    
    poll = request.session.get('poll')
    answer_list = []
    for contact_group in poll.contact_group_list.all():
        for contact in contact_group.contact_set.all():
            code=''.join(map(lambda xx:(hex(ord(xx))[2:]),os.urandom(16)))
            answer = Answer(poll=poll, contact=contact, code=code)
            answer_list.append(answer)

    # todo: 批量保存
    for answer in answer_list:
        answer.save()

    connection = mail.get_connection()
    # 手动打开链接(connection)
    connection.open()

    # 使用该链接构造一个邮件报文
    email_list = []
    for answer in answer_list:
        str_url = "http://localhost:8000/polls/s/%s" % answer.code
        content = poll.template.replace('{url}', str_url)
        subject = u"采购需求调查:%s" %poll.title
        to = answer.contact.email
        email_list.append(mail.EmailMessage(subject=subject, body=content, from_email='xing.tang@rrd.com',
                          to=[to], connection=connection))

    mail_count = connection.send_messages(email_list)
    print "mail_count:%s" % mail_count

    connection.close()
    message = u'您已经成功保存调查:"%s",通知邮件已经发送给%s人.' % (poll.title, mail_count)
    request.session['poll'] = poll
        
    return render_to_response('pollapp/poll.html', 
        {'mail_count':mail_count,
         'message': message,
         'poll_list': Poll.objects.all(),
         },
        context_instance=RequestContext(request))
