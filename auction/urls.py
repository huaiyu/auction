from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^cate$', views.index, name='index'),
    url(r'^(?P<search_action>(buy|sell))_search$', views.search, name='search'),
    url(r'^(?P<search_action>(buy|sell))_search_result$', views.search_result, name='search_result'),
    url(r'^publish_buy$', views.publish_buy, name='publish_buy'),
    url(r'^publish_sell$', views.publish_sell, name='publish_sell'),
    url(r'^preview_buy$', views.preview_buy, name='preview_buy'),
    url(r'^decide_buy$', views.decide_buy, name='decide_buy'),
    url(r'^preview_sell$', views.preview_sell, name='preview_sell'),
    url(r'^decide_sell$', views.decide_sell, name='decide_sell'),
    url(r'^deal', views.deal, name='deal'),
]