from django.shortcuts import render, render_to_response, redirect, HttpResponseRedirect, get_object_or_404, HttpResponse
from django.conf import settings
from django.template import RequestContext
from django.template.loader import render_to_string
from django.views.generic import DetailView
from django.views.generic.edit import FormView, UpdateView
from datetime import datetime, timedelta
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.utils import timezone
from django.core.mail import send_mail

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
	form = PublishForm()
	latest_messages = Message.objects.filter(visible=True).order_by('-pk')[:10]
	return render_to_response('control/cp.html',{
			'form': form,
			'latest_messages': latest_messages,
		}, context_instance=RequestContext(request))

def control_messages(request, filter, category):
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
	if request.method == "POST":
		form = CategoryForm(request.POST)
		if form.is_valid():
			form.save()
	return redirect('/cp/categories/')


def email(request):
	visible_messages = Message.visible_objects.order_by('end_date')
	categories = Category.objects.filter(messages__in=visible_messages).distinct().order_by('order')
	return render_to_response('email.html',{
 		'categories': categories
 		}, context_instance=RequestContext(request))

def delete_message(request, pk):
	if request.method == 'POST':
		message = get_object_or_404(Message, pk=pk)
		message.delete()
	return redirect('/cp/messages/all/all/')

def hide_message(request, pk):
	if request.method == 'POST':
		message = get_object_or_404(Message, pk=pk)
		if message.visible:
			message.visible = False
		else:
			message.visible = True
		message.save()
	return redirect('/cp/messages/all/all/')


def edit_message(request, pk):
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



class PublishFormView(FormView):
	template_name = 'control/cp.html'
	form_class = PublishForm
	success_url = '/cp/'
	form_valid_message = 'Validi'
	form_invalid_message = 'Invalidi'

	def form_valid(self, form):
		message = Message(
					header=form.cleaned_data['header'],
					content=form.cleaned_data['content'],
					category=form.cleaned_data['category'],
					start_date=form.cleaned_data['start_date'],
					end_date=form.cleaned_data['end_date'],
					deadline_date=form.cleaned_data['deadline_date'],
					show_deadline=form.cleaned_data['show_deadline'],
					visible=form.cleaned_data['visible']
			)
		message.save()
		return HttpResponseRedirect(self.get_success_url())
