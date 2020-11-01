""" Define the URL patter for learning_logs."""
from django.urls import path
from .import views

app_name = 'learning_logs'
urlpatterns = [
#Home Page
path('', views.index, name= 'index'),
#topic page
path('topics/',views.topics,name='topics'),
#details page of a single opic
path('topics/<int:topic_id>',views.topic, name='topic'),
#details of a topic form
path('new_topic/',views.new_topic,name='new_topic'),
#details of entry related to topic
path('new_entry/<int:topic_id>/', views.new_entry, name='new_entry'),
#detail to edit entry made
path('edit_entry/<int:entry_id>/',views.edit_entry, name='edit_entry'),

]