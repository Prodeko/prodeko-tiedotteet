from django.shortcuts import render, render_to_response, redirect, HttpResponseRedirect, get_object_or_404, HttpResponse
from django.http import HttpResponseNotFound, HttpResponseForbidden, JsonResponse
from django.conf import settings
from django.template import RequestContext, Context
from django.template.loader import render_to_string, get_template
from datetime import datetime, timedelta
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.utils import timezone
from django.utils.html import strip_tags
from django.contrib import messages
from django.core.mail import EmailMultiAlternatives
from django.core.mail.backends.smtp import EmailBackend


from info.models import *
from info.forms import *


def index(request):
	""" the public main page """
	visible_messages = Message.visible_objects.order_by('end_date')
	categories = Category.objects.filter(messages__in=visible_messages).distinct().order_by('order')
	return render_to_response('content.html',{
			'categories': categories
		}, context_instance=RequestContext(request))

def control_panel(request):
	""" site for publishing new messages """
	if not request.user.is_superuser:
		return HttpResponseForbidden()
	form = PublishForm()
	latest_messages = Message.objects.filter(visible=True).order_by('-pk')[:10]
	if request.method == 'POST':
		form = PublishForm(request.POST)
		if form.is_valid():
			form.save()
			messages.success(request, 'Uusi tiedote tallennettu')
			return redirect(control_panel)
	return render_to_response('control/cp.html',{
			'form': form,
			'latest_messages': latest_messages,
		}, context_instance=RequestContext(request))

def control_messages(request, filter, category):
	""" control panel - list messages """
	if not request.user.is_superuser:
		return HttpResponseForbidden()
	if filter == 'now':
		messages = Message.objects.filter(end_date__gte=timezone.now()).order_by('-pk')
		filter_label = 'Nykyiset'
	elif filter == 'new':
		messages = Message.objects.filter(start_date__gte=timezone.now()-timedelta(days=7)).order_by('-pk')
		filter_label = 'Uudet'
	elif filter == 'upcoming':
		messages = Message.objects.filter(start_date__gte=timezone.now()).order_by('-pk')
		filter_label = 'Tulevat'
	elif filter == 'old':
		messages = Message.objects.filter(end_date__lt=timezone.now()).order_by('-pk')
		filter_label = 'Menneet'
	else:
		messages = Message.objects.all().order_by('-pk')
		filter_label = 'Kaikki'

	categories = Category.objects.filter(messages__in=messages).distinct().order_by('order')

	for c in categories:
		if str(c.pk) == category:
			messages = messages.filter(category=c)

	paginator = Paginator(messages, 100) # 100 messages per page
	page = request.GET.get('page')
	try:
		messages = paginator.page(page)
	except PageNotAnInteger:
		messages = paginator.page(1)
	except EmptyPage:
		messages = paginator.page(paginator.num_pages)
	queries_without_page = request.GET.copy()
	if 'page' in queries_without_page.keys():
		del queries_without_page['page']

	return render_to_response('control/messages.html',{
			'messages': messages,
			'categories': categories,
			'filter': filter,
			'filter_label': filter_label,
		}, context_instance=RequestContext(request))

def categories(request):
	""" control panel - edit categories """
	if not request.user.is_superuser:
		return HttpResponseForbidden()
	categories = Category.objects.all()
	cforms = [CategoryForm(prefix=str(x), instance=x) for x in categories]
	nform = CategoryForm()
	if request.method == "POST":
		cforms = [CategoryForm(request.POST, prefix=str(x), instance=x) for x in categories]
		if all([cf.is_valid() for cf in cforms]):
			for cf in cforms:
				category = cf.save()
				if category.title == "":
					category.delete()
			return redirect('/cp/categories/')
	return render_to_response('control/categories.html',{
			'categories':categories,
			'cforms':cforms,
			'nform':nform,
		}, context_instance=RequestContext(request))

def new_category(request):
	""" control panel - add new category """
	if not request.user.is_superuser:
		return HttpResponseForbidden()
	if request.method == "POST":
		form = CategoryForm(request.POST)
		if form.is_valid():
			form.save()
	return redirect('/cp/categories/')


def tags(request):
	""" control panel - edit tags """
	if not request.user.is_superuser:
		return HttpResponseForbidden()
	tags = Tag.objects.all()
	form = TagForm()
	if request.method == "POST":
		form = TagForm(request.POST)
		if form.is_valid():
			tag = form.save()
			return redirect('/cp/tags/')
	return render_to_response('control/tags.html',{
			'tags':tags,
			'form':form,
		}, context_instance=RequestContext(request))

def delete_tag(request, pk):
	if not request.user.is_superuser:
		return HttpResponseForbidden()
	if request.method == 'POST':
		tag = get_object_or_404(Tag, pk=pk)
		tag.delete()
	return redirect('/cp/tags/')


def email(request):
	""" email template """
	visible_messages = Message.visible_objects.order_by('end_date')
	categories = Category.objects.filter(messages__in=visible_messages).distinct().order_by('order')
	return render_to_response('email.html',{
 		'categories': categories
 		}, context_instance=RequestContext(request))

def delete_message(request, pk):
	if not request.user.is_superuser:
		return HttpResponseForbidden()
	if request.method == 'POST':
		message = get_object_or_404(Message, pk=pk)
		message.delete()
	return redirect('/cp/messages/all/all/')

def hide_message(request, pk):
	if not request.user.is_superuser:
		return HttpResponseForbidden()
	if request.method == 'POST':
		message = get_object_or_404(Message, pk=pk)
		if message.visible:
			message.visible = False
		else:
			message.visible = True
		message.save()
	return redirect('/cp/messages/all/all/')

def edit_message(request, pk):
	if not request.user.is_superuser:
		return HttpResponseForbidden()
	form = EditForm(instance=get_object_or_404(Message, pk=pk))
	messages = {}
	if request.method == 'POST':
		form = EditForm(request.POST, instance=get_object_or_404(Message, pk=pk))
		if form.is_valid():
			form.save()
			messages['success'] = 'Tiedote päivitetty'

	return render_to_response('control/editor.html',{
			'form': form,
			'messages': messages,
		}, context_instance=RequestContext(request))


def control_panel_email(request):
	""" control panel - send email page for sending emails and editing mail configurations """
	if not request.user.is_superuser:
		return HttpResponseForbidden()
	config, created = MailConfiguration.objects.get_or_create(pk=1)
	config_form = MailConfigurationForm(instance=config)
	send_form = SendEmailForm()
	if request.method == "POST":
		config_form = MailConfigurationForm(request.POST, instance=config)
		if config_form.is_valid():
			config_form.save()
			return redirect(control_panel_email)
	return render_to_response('control/email.html',{
			'config': config,
			'config_form': config_form,
			'send_form': send_form,
		}, context_instance=RequestContext(request))

def send_email(request):
	""" send infro letter via email """
	if not request.user.is_superuser:
		return HttpResponseForbidden()
	if request.method == "POST":
		form = SendEmailForm(request.POST)
		if form.is_valid():
			# create html body
			visible_messages = Message.visible_objects.order_by('end_date')
			categories = Category.objects.filter(messages__in=visible_messages).distinct().order_by('order')
			config = MailConfiguration.objects.get(pk=1)
			template = get_template('email.html')
			context = Context({
				'categories': categories,
			})
			text_content = strip_tags(template.render(context))
			html_content = template.render(context)
			# backend configuration
			backend = EmailBackend(
				host=config.host,
				port=config.port,
				username=config.username,
				password=config.password,
				use_tls=config.use_tls,
				fail_silently=config.fail_silently
			)
			# create the email
			email = EmailMultiAlternatives(
				subject=form.cleaned_data["subject"],
				body=text_content,
				from_email=config.username,
				to=form.cleaned_data["to"].split(","),
		        connection=backend
			)
			# attach html content
			email.attach_alternative(html_content, "text/html")
			# send
			try:
				email.send()
				return JsonResponse({
		            'success' : True,
		        })
			except:
				return JsonResponse({
					'success' : False,
					'errors': {'mail':'failed to send'},
				})
		return JsonResponse({
			'success' : False,
			'errors': dict(form.errors.items()),
		})
	return HttpResponseForbidden()
