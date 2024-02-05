from .models import News, Category
from django.utils import timezone

def latest_news(request):
    latest_news = News.published.all().order_by('-published_time')[:10]
    categories = Category.objects.all()
    time = timezone.now()

    context = {
        "latest_news": latest_news,
        "categories": categories,
        "time":time
    }

    return context