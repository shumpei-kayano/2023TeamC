from django.urls import path
from diary import views


app_name = 'diary'
urlpatterns = [
    path('account/delete/success', views.account_delete_success, name='account_delete_success'),
    path('account/delete', views.account_delete,name='account_delete'),
    path('base', views.base,name='base'),
    path('calendar/month', views.calendar_month,name='calendar_month'),
    path('calender/week', views.calender_week,name='calender_week'),
    path('create/diary/confirmation', views.create_diary_confirmation,name='create_diary_confirmation'),
    path('create/diary/confirmation/<int:pk>', views.create_diary_confirmation2,name='create_diary_confirmation'),
    path('create/diary', views.create_diary,name='create_diary'),
    path('create/diary/<int:pk>', views.create_diary,name='create_diary'),
    path('diary/delete/<int:pk>', views.diary_delete,name='diary_delete'),
    path('diary/graph', views.diary_graph,name='diary_graph'),
    path('diary/home', views.diary_home,name='diary_home'),
    path('diary/update/<int:pk>', views.diary_update,name='diary_update'),
    path('help/calender', views.help_calender,name='help_calender'),
    path('help/diary/edit', views.help_diary_edit,name='help_diary_edit'),
    path('help/diary', views.help_diary,name='help_diary'),
    path('help/graph', views.help_graph,name='help_graph'),
    path('help', views.help,name='help'),
    path('home/top', views.home_top,name='home_top'),
    path('home/top/<int:pk>', views.home_top2,name='home_top'),
    path('loading', views.loading,name='loading'),
    path('logout/success', views.logout_success,name='logout_success'),
    path('logout',views.logout,name='logout'),
    path('member/information_edit/cancel', views.member_information_edit_cancel,name='member_information_edit_cancel'),
    path('member/information/edit/check', views.member_information_edit_check,name='member_information_edit_check'),
    path('member/information/edit/comp', views.member_information_edit_comp,name='member_information_edit_comp'),
    path('member/information/edit', views.member_information_edit,name='member_information_edit'),
    path('member/information', views.member_information,name='member_information'),
    path('month/graph', views.month_graph,name='month_graph'),
    path('positive/conversion', views.positive_conversion,name='positive_conversion'),
    path('record/diary/graph', views.record_diary_graph,name='record_diary_graph'),
    path('record/diary/detail', views.record_diary_detail,name='record_diary_detail'),
    path('setting', views.setting,name='setting'),
    path('today/counseling', views.today_counseling,name='today_counseling'),
    path('today/counseling/graph', views.today_counseling_graph,name='today_counseling_graph'),
    path('today/diary/detail/<int:pk>', views.today_diary_detail,name='today_diary_detail'),
    path('today/diary/graph', views.today_diary_graph,name='today_diary_graph'),
    path('week/graph', views.week_graph,name='week_graph'),
]