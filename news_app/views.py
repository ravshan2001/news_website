from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from .models import News, Category
from .forms import ContactForm
from django.views.generic import TemplateView, ListView
# Create your views here.


def news_list(request):
    # news_list = News.objects.all()
    # news_list = News.published.all()

    news_list = News.objects.filter(status=News.Status.Published)

    context = {
        "news_list": news_list
    }

    return render(request, "news/news_list.html", context)

def newsDetailPage(request,news):
    news = get_object_or_404(News, slug=news, status=News.Status.Published)
    context = {
        "news":news
    }

    return render(request, "news/news_detail_page.html", context)

# def homePageView(request):
#     categories = Category.objects.all()
#     news_list = News.published.all().order_by('-published_time')[:5]
#     local_main = News.published.filter(category__name='mahalliy').order_by('published_time')[0]
#     local_news = News.published.all().filter(category__name='mahalliy').order_by('published_time')[1:5]
#
#     context = {
#         "news_list": news_list,
#         "categories":categories,
#         "local_news": local_news,
#         "local_main": local_main
#     }
#
#     return render(request, "news/index.html", context)

# HomePageView ni class orqali berish
class HomePageView(ListView):
    model = News
    template_name = 'news/index.html'
    context_object_name = 'news'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        context['news_list'] = News.published.all().order_by('-published_time')[:5]
        context['mahalliy_xabarlar'] = News.published.filter(category__name='mahalliy').order_by('-published_time')[:5]
        context['sport_xabarlar'] = News.published.filter(category__name='sport').order_by('-published_time')[:5]
        context['texnologik_xabarlar'] = News.published.filter(category__name='texnologik').order_by('-published_time')[:5]
        context['xorij_xabarlar'] = News.published.filter(category__name='xorijiy').order_by('-published_time')[:5]

        return context

# def contactPageView(request):
#     form = ContactForm(request.POST or None)
#     if request.method == "POST" and form.is_valid():
#         form.save()
#         return HttpResponse("<h1>Biz bilan bog'langaningiz uchun tashakkur!</h1>")
#     context = {
#         "form":form
#     }
#     return render(request, 'news/contact.html', context)

class ContactPageView(TemplateView):
    template_name = "news/contact.html"

    def get(self,request, *args, **kwargs):
        form = ContactForm()
        context = {
            "form": form
        }
        return render(request, 'news/contact.html',context)

    def post(self, request, *args, **kwargs):
        form = ContactForm(request.POST)
        if request.method == "POST" and form.is_valid():
            form.save()
            return HttpResponse("<h1>Biz bilan bog'langaningiz uchun rahmat</h1>")
        context = {
            "form": form
        }

        return render(request, 'news/contact.html', context)


# Viewslar
class LocalNewsView(ListView):
    model = News
    template_name = 'news/navbar/local.html'
    context_object_name = 'mahalliy_xabarlar'

    def get_queryset(self):
        news = self.model.published.all().filter(category__name = 'mahalliy')
        return news

class ForeignNewsView(ListView):
    model = News
    template_name = 'news/navbar/foreign.html'
    context_object_name = 'xorij_xabarlar'

    def get_queryset(self):
        news = self.model.published.all().filter(category__name = 'xorijiy')
        return news

class TechnologyNewsView(ListView):
    model = News
    template_name = 'news/navbar/technology.html'
    context_object_name = 'texnologik_xabarlar'

    def get_queryset(self):
        news = self.model.published.all().filter(category__name = 'texnologik')
        return news

class SportNewsView(ListView):
    model = News
    template_name = 'news/navbar/sport.html'
    context_object_name = 'sport_xabarlar'

    def get_queryset(self):
        news = self.model.published.all().filter(category__name = 'sport')
        return news


def errorPageView(request):
    return render(request, 'news/navbar/404.html')

def aboutPageView(request):
    return render(request, 'news/about.html')