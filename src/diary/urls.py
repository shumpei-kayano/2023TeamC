from django.urls import path
from diary import views

app_name = 'diary'
urlpatterns = [
    path('account_delete_success', views.account_delete_success, name='account_delete_success'),
    path('account_delete', views.account_delete,name='account_delete'),
    path('base', views.base,name='base'),
    path('calendar_month', views.calendar_month,name='calendar_month'),
    path('calender_week', views.calendar_month,name='calender_week'),
    path('create_diary_confirmation', views.calendar_month,name='create_diary_confirmation'),
    path('create_diary', views.calendar_month,name='create_diary'),
    path('diary_delete', views.calendar_month,name='diary_delete'),
    path('diary_graph', views.calendar_month,name='diary_graph'),
]