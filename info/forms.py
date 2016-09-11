# -*- coding: utf-8 -*-

from django.forms import Form, ModelForm, TextInput, Textarea, DateField, Select, CheckboxInput, CharField, NumberInput
from django.utils.translation import ugettext_lazy as _
from django.contrib.admin.widgets import AdminDateWidget
from info.models import Message, Category

class PublishForm(ModelForm):
	class Meta:
		model = Message
		fields = ['header', 'content', 'category', 'start_date', 'end_date', 'deadline_date', 'show_deadline', 'visible']
		labels = {
			'header': _('Otsikko'),
			'content': _('Sisältö'),
			'category': _('Kategoria'),
			'start_date': _('Alkaa'),
			'end_date': _('Loppuu'),
			'deadline_date': _('Deadline'),
			'show_deadline': _('Näytä deadline'),
			'visible': _('Näytetään'),
		}
		widgets = {
			'header': TextInput(attrs={'class': 'form-control input-md'}),
			'content': Textarea(attrs={'id': 'foo'}),
			'start_date': AdminDateWidget(attrs={'class': 'form-control input-md'}),
			'end_date': AdminDateWidget(attrs={'class': 'form-control input-md'}),
			'deadline_date': AdminDateWidget(attrs={'class': 'form-control input-md'}),
			'category': Select(attrs={'class': 'form-control'}),
			'show_deadline': CheckboxInput(),
			'visible': CheckboxInput(),
		}


class EditForm(ModelForm):
	class Meta:
		model = Message
		success_message = 'Tiedote päivitetty'
		fields = ['header', 'content', 'category', 'start_date', 'end_date', 'deadline_date', 'show_deadline', 'visible']
		labels = {
			'header': _('Otsikko'),
			'content': _('Content'),
			'category': _('Kategoria'),
			'start_date': _('Alkaa'),
			'end_date': _('Loppuu'),
			'deadline_date': _('Deadline'),
			'show_deadline': _('Näytä deadline'),
			'visible': _('Näytetään'),
		}
		widgets = {
			'header': TextInput(attrs={'class': 'form-control input-md'}),
			'content': Textarea(attrs={'id': 'foo'}),
			'start_date': AdminDateWidget(attrs={'class': 'form-control input-md'}),
			'end_date': AdminDateWidget(attrs={'class': 'form-control input-md'}),
			'deadline_date': AdminDateWidget(attrs={'class': 'form-control input-md'}),
			'category': Select(attrs={'class': 'form-control'}),
			'show_deadline': CheckboxInput(),
			'visible': CheckboxInput(),
		}

class CategoryForm(ModelForm):
	class Meta:
		model = Category
		fields = ['title', 'order',]
		labels = {
			'title': _('Kategoria'),
			'order': _('Järjestys'),
		}
		widgets = {
			'title': TextInput(attrs={'class': 'form-control'}),
			'order': NumberInput(attrs={'class': 'form-control'}),
		}
