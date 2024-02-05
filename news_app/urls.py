from django.urls import path
from .views import news_list, newsDetailPage, HomePageView, ContactPageView, errorPageView,aboutPageView, \
    LocalNewsView, SportNewsView, TechnologyNewsView, ForeignNewsView

urlpatterns = [
    path("news/", news_list, name = 'news_list'),
    path("", HomePageView.as_view(), name = 'home_page'),
    path("contact-us/", ContactPageView.as_view(), name='contact_page'),
    path("404/", errorPageView, name='error_page'),
    path("about/", aboutPageView, name='about_page'),
    path("news/<slug:news>/", newsDetailPage, name = 'news_detail_page'),
    path("local/", LocalNewsView.as_view(), name = 'local_news_page'),
    path("foreign/", ForeignNewsView.as_view(), name='foreign_news_page'),
    path("technology/", TechnologyNewsView.as_view(), name='technology_news_page'),
    path("sport/", SportNewsView.as_view(), name='sport_news_page')

]
