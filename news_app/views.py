from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy
from django.http import HttpResponse
from .models import News, Category
from .forms import ContactForm, CommentForm
from django.views.generic import TemplateView, ListView, DeleteView, UpdateView, CreateView
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.mixins import LoginRequiredMixin
from news_project.custom_permissions import OnlyLoggedSuperUser
from django.contrib.auth.models import User
from django.db.models import Q
from hitcount.utils import get_hitcount_model
from hitcount.views import HitCountMixin

# Create your views here.

# @login_required
def news_list(request):
    # news_list = News.objects.all()
    # news_list = News.published.all()

    news_list = News.objects.filter(status=News.Status.Published)

    context = {
        "news_list": news_list
    }

    return render(request, "news/index.html", context)

# @login_required
def newsDetailPage(request,news):
    news = get_object_or_404(News, slug=news, status=News.Status.Published)

    context = {}
    hit_count = get_hitcount_model().objects.get_for_object(news)
    hits = hit_count.hits
    hitcontext = context['hitcount'] = {'pk' : hit_count.pk}
    hit_count_response = HitCountMixin.hit_count(request, hit_count)
    if hit_count_response.hit_counted:
        hits = hits+1
        hitcontext['hit_counted'] = hit_count_response.hit_counted
        hitcontext['hit_message'] = hit_count_response.hit_message
        hitcontext['total_hints'] = hits

    comments = news.comments.filter(active=True)
    comment_count = comments.count()
    new_comment = None

    if request.method == "POST":
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            new_comment.news = news
            new_comment.user = request.user
            new_comment.save()
            comment_form = CommentForm()
    else:
        comment_form = CommentForm()

    context = {
        "news": news,
        'comments': comments,
        'comment_count': comment_count,
        "new_comment": new_comment,
        "comment_form": comment_form
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

@login_required
def aboutPageView(request):
    return render(request, 'news/about.html')

# Delete and Update


class NewsUpdateView(OnlyLoggedSuperUser,UpdateView):
    model = News
    fields = ('title', 'body', 'image', 'category', 'status')
    template_name = 'crud/news_edit.html'

class NewsDeleteView(OnlyLoggedSuperUser,DeleteView):
    model = News
    template_name = 'crud/news_delete.html'
    success_url = reverse_lazy('home_page')

class NewsCreateView(OnlyLoggedSuperUser,CreateView):
    model = News
    template_name = 'crud/news_create.html'
    fields = ('title', 'slug', 'body', 'image', 'category', 'status')

@login_required
@user_passes_test(lambda u:u.is_superuser)
def admin_page_view(request):
    admin_users = User.objects.filter(is_superuser = True)

    context = {
        "admin_users": admin_users
    }
    return render(request, 'pages/admin_page.html', context)

class SearchResultList(ListView):
    model = News
    template_name = "news/search_result.html"
    context_object_name = "barcha_yangiliklar"

    def get_queryset(self):
        query = self.request.GET.get('q')
        return News.objects.filter(
            Q(title__icontains=query) | Q(body__icontains=query)
        )