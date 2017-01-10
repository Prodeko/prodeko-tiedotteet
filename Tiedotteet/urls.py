from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.contrib.auth import views as auth_views
from rest_framework.urlpatterns import format_suffix_patterns
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from info import views, views_api

urlpatterns = patterns('',

	# Authentication
    url(r'^login/$', auth_views.login, {'template_name': 'login.html'}, name='login'),
    url(r'^logout/$', auth_views.logout, {'next_page': '/'}, name='logout'),

	# ckeditor
	(r'^ckeditor/', include('ckeditor.urls')),

	# Admin
	url(r'^admin/', include(admin.site.urls)),
	url(r'^new/$', views.new, name='new'),

	# Control panel
	url(r'^cp/$', login_required(views.control_panel)),
	url(r'^cp/messages/(?P<pk>\d+)/edit/$', login_required(views.edit_message), name="edit"),
	url(r'^cp/messages/(?P<pk>\d+)/delete/$', login_required(views.delete_message)),
	url(r'^cp/messages/(?P<pk>\d+)/hide/$', login_required(views.hide_message), name="delete"),
	url(r'^cp/publish/$', require_POST(views.PublishFormView.as_view()), name='publish'),
	url(r'^cp/messages/(?P<filter>\w+)/(?P<category>\w+)/$', login_required(views.control_messages)),
	url(r'^cp/categories/$', login_required(views.categories), name='categories'),
	url(r'^cp/categories/new/$', login_required(views.new_category), name='new_category'),

	# index
	url(r'^$', views.index, name='index'),

	# email
	url(r'^email/', views.email),

	# API
	url(r'^api/content/$', views_api.ContentList.as_view()),
	url(r'^api/messages/$', views_api.MessageList.as_view()),

)

urlpatterns = format_suffix_patterns(urlpatterns)
