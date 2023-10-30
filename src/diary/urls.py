from django.urls import path
from diary import views


app_name = 'diary'
urlpatterns = [
    path('account_delete_success', views.account_delete_success, name='account_delete_success'),
    path('account_delete', views.account_delete,name='account_delete'),
    path('base', views.base,name='base'),
    path('calendar_month', views.calendar_month,name='calendar_month'),
    path('calender_week', views.calender_week,name='calender_week'),
    path('create_diary_confirmation', views.create_diary_confirmation,name='create_diary_confirmation'),
    path('create_diary/', views.create_diary,name='create_diary'),
    path('diary_delete', views.diary_delete,name='diary_delete'),
    path('diary_graph', views.diary_graph,name='diary_graph'),
    path('diary_home', views.diary_home,name='diary_home'),
    path('diary_update', views.diary_update,name='diary_update'),
    path('help_calender', views.help_calender,name='help_calender'),
    path('help_diary_edit', views.help_diary_edit,name='help_diary_edit'),
    path('help_diary', views.help_diary,name='help_diary'),
    path('help_graph', views.help_graph,name='help_graph'),
    path('help', views.help,name='help'),
    path('home_top', views.home_top,name='home_top'),
    path('loading', views.loading,name='loading'),
    path('logout_success', views.logout_success,name='logout_success'),
    path('logout',views.logout,name='logout'),
    path('member_information_edit_cancel', views.member_information_edit_cancel,name='member_information_edit_cancel'),
    path('member_information_edit_check', views.member_information_edit_check,name='member_information_edit_check'),
    path('member_information_edit_comp', views.member_information_edit_comp,name='member_information_edit_comp'),
    path('member_information_edit', views.member_information_edit,name='member_information_edit'),
    path('member_information', views.member_information,name='member_information'),
    path('month_graph', views.month_graph,name='month_graph'),
    path('positive_conversion', views.positive_conversion,name='positive_conversion'),
    path('setting', views.setting,name='setting'),
    path('today_counseling', views.today_counseling,name='today_counseling'),
    path('today_diary_detail_', views.today_diary_detail_,name='today_diary_detail_'),
    path('week_graph', views.week_graph,name='week_graph'),
]