# -*- coding: utf-8 -*-

from django.forms import Form, ModelForm, TextInput, Textarea, DateField, Select, CheckboxInput, CharField, NumberInput, PasswordInput
from django.utils.translation import ugettext_lazy as _
from django.contrib.admin.widgets import AdminDateWidget
from info.models import Message, Category, Tag, MailConfiguration

class PublishForm(ModelForm):
	class Meta:
		model = Message
		fields = ['header', 'content', 'category', 'tags', 'start_date', 'end_date', 'deadline_date', 'show_deadline', 'visible']
		labels = {
			'header': _('Otsikko'),
			'content': _('Sisältö'),
			'category': _('Kategoria'),
			'tags': _('Tagit'),
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
			'tags': Select(attrs={'class': 'form-control selectpicker', 'multiple': '', 'title': 'Ei valittuja tageja'}),
			'show_deadline': CheckboxInput(),
			'visible': CheckboxInput(),
		}


class EditForm(ModelForm):
	class Meta:
		model = Message
		success_message = 'Tiedote päivitetty'
		fields = ['header', 'content', 'category', 'tags', 'start_date', 'end_date', 'deadline_date', 'show_deadline', 'visible']
		labels = {
			'header': _('Otsikko'),
			'content': _('Content'),
			'category': _('Kategoria'),
			'tags': _('Tagit'),
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
			'tags': Select(attrs={'class': 'form-control selectpicker', 'multiple': '', 'title': 'Ei valittuja tageja'}),
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

class TagForm(ModelForm):
	class Meta:
		model = Tag
		fields = ['title']
		labels = {
			'title': _('Uusi tagi'),
		}
		widgets = {
			'title': TextInput(attrs={'class': 'form-control'}),
		}


class MailConfigurationForm(ModelForm):
	class Meta:
		model = MailConfiguration
		fields = ['host', 'port', 'username', 'password', 'use_tls']
		labels = {
			'host': _('Palvelin (host)'),
			'port': _('Portti'),
			'username': _('Käyttäjätunnus (sähköpostiosoite)'),
			'password': _('Salasana'),
			'use_tls': _('TLS salaus päällä'),
		}
		widgets = {
			'host': TextInput(attrs={'class': 'form-control'}),
			'port': NumberInput(attrs={'class': 'form-control'}),
			'username': TextInput(attrs={'class': 'form-control'}),
			'password': PasswordInput(attrs={'class': 'form-control'}),
			'use_tls': CheckboxInput(),
		}

class SendEmailForm(Form):
	subject = CharField(widget=TextInput(attrs={'class': 'form-control'}), label="Otsikko")
	to = CharField(widget=TextInput(attrs={'class': 'form-control'}), label="Vastaanottajat (erottele pilkulla)")
