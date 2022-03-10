from django.shortcuts import render, get_object_or_404
from .models import News
# Create your views here.

def list_news(request):
    newss = News.objects.all().order_by("-updated_at")
    context = {"newss": newss}
    return render(request, 'shop/news.html', context)

def detail_news(request, slug=None):
    news = get_object_or_404(News, slug=slug)
    context = {"news": news}
    return render(request, 'shop/detail_news.html', context)

