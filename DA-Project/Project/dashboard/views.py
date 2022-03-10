from django.shortcuts import render, redirect, get_object_or_404
import datetime
from order.models import Order, OrderItem
from django.http import JsonResponse
from shop.models import Variation
import json
from shop.forms import *
from shop.models import *
from django.contrib import messages
from news.models import News
from news.forms import NewsForm
import datetime
from account.decorators import admin_only

# Create your views here.

@admin_only
def dashboard(request):
    return render(request, "dashboard/dashboard_home.html", {"nav":"dashboard"})

def by_week(request):
    week = []
    today = datetime.date.today()
    last_monday = today - datetime.timedelta(days=today.weekday())
    for day in range(7):
        
        date = (last_monday + datetime.timedelta(days=day))

        a = Order.objects.filter(created_at__date=date).count()
        week.append({
            "day": date.strftime("%A"),
            "quantity": Order.objects.filter(created_at__date=date).count()
        })
    return JsonResponse(week, safe=False)

@admin_only
def dashboard_order(request):
    return render(request, "dashboard/dashboard_order.html", {"nav":"order"})

@admin_only
def dashboard_product(request):
    nav = "product"
    form_variation = VariationForm()
    context = {"nav": nav, "form_variation": form_variation}
    return render(request, "dashboard/dashboard_product.html", context)

@admin_only
def create_product(request):
    nav = "product"
    form_product = ProductForm()
    form_version = VersionForm()
    try:
        if request.method == "POST":
            if request.POST.get("save") == "add-product":
                form_product = ProductForm(request.POST)
                if form_product.is_valid():
                    data = form_product.cleaned_data
                    product_exists = Product.objects.filter(version__exact=data['version'], capacity__exact=data['capacity']).exists()
                    if product_exists == False:
                        product = Product.objects.create(version=data['version'], capacity=data['capacity'], price=data['price'], is_active=data['is_active'])
                    product.save()
                    return redirect("db_update_product")
            elif request.POST.get("save") == "add-version":
                form_version = VersionForm(request.POST)
                if form_version.is_valid():
                    data = form_version.cleaned_data
                    version_exists = Version.objects.filter(
                                                            category__exact=data["category"],
                                                            series__exact=data["series"],
                                                            name__iexact=data['name'],
                                                            ).exists()
                    if version_exists == False:
                        version = Version.objects.create(category=data["category"],
                                                        series=data["series"],
                                                        name=data["name"],
                                                        image=data["image"],
                                                        description=data["description"],
                                                        )
                        version.save()
                        return redirect("/dashboard/product/create/")
        else:
            form_product = ProductForm()
            form_version = VersionForm()
    except:
        pass
    context = {"form_product": form_product, "form_version": form_version, "nav":nav}
    return render(request, "dashboard/db_create_product.html", context)

@admin_only
def update_product(request, pk=None):
    nav = "product"
    context = {}
    try:
        obj = get_object_or_404(Product, id=pk)
        form = ProductForm(request.POST or None, instance = obj)
        if request.method == "POST":
            if form.is_valid():
                form.save()
                messages.success(request, 'Cập nhật thành công')
            else:
                messages.error(request, "Cập nhật không thành công")
        context['form'] = form
        context['nav'] = nav
    except:
        pass
    return render(request, "dashboard/db_update_product.html", context)

@admin_only
def list_versions(request):
    nav = "versions"
    context = {"nav": nav}
    return render(request, 'dashboard/db_list_version.html', context)

@admin_only
def create_version(request):
    nav = "versions"
    form_version = VersionForm()
    form_series = SeriesForm()
    form_category = CategoryForm()
    if request.method == "POST":
        if request.POST.get("save") == "add-series":
            form_series = SeriesForm(request.POST)
            if form_series.is_valid():
                form_series.save()
                messages.success(request, 'Thêm thành công')
            else:
                form_series = SeriesForm()

        if request.POST.get("save") == "add-category":
            form_category = CategoryForm(request.POST, request.FILES)
            if form_category.is_valid():
                form_category.save()
                messages.success(request, 'Thêm thành công')
            else:
                form_category = CategoryForm()
    context = {"form_version":form_version, "nav": nav,
                "form_series": form_series, "form_category": form_category,
            }
    return render(request, 'dashboard/db_create_version.html', context)


@admin_only
def create_version_api(request):
    data = request.POST
    files = request.FILES
    messages = ""
    version_exists = Version.objects.filter(
                                                category__exact=data["category"],
                                                series__exact=data["series"],
                                                name__iexact=data['name'],
                                                ).exists()

    if version_exists == False:                                     
        version = Version.objects.create( category_id=data['category'],
                                        series_id=data['series'],
                                        name=data['name'],
                                        image=files['image'],
                                        description=data['description']
                                        )
        version.save()
        message = "Thêm Thành Công"
    else:
        message = "Thêm không thành công"
    return JsonResponse(message, safe=False)

@admin_only
def update_version(request, pk=None):
    nav = "versions"
    context = {}
    try:
        obj = get_object_or_404(Version, id=pk)
        form = VersionForm(request.POST or None, request.FILES or None, instance = obj)
        if request.method == "POST":
            form = VersionForm(request.POST, request.FILES, instance = obj)
            if form.is_valid():
                form.save()
                messages.success(request, 'Cập nhật thành công')
            else:
                messages.error(request, "Cập nhật không thành công")
        context['form'] = form
        context['nav'] = nav
    except:
        pass
    return render(request, "dashboard/db_update_version.html", context)

@admin_only
def create_variation(request):
    form = VariationForm()
    context = {"form": form}
    return render(request, "dashboard/db_create_variation.html", context)

@admin_only
def list_series(request):
    nav = "series"
    context = {"nav": nav}
    return render(request, 'dashboard/db_list_series.html', context)

@admin_only
def create_series(request):
    nav = "series"
    form_series = SeriesForm()
    context = {"form_series": form_series, "nav": nav}
    return render(request, 'dashboard/db_create_series.html', context)

@admin_only
def update_series(request, pk=None):
    nav = "series"
    try:
        obj = get_object_or_404(Series, id=pk)
        form_series = SeriesForm(request.POST or None, instance = obj)
        if request.method == "POST":
            form_series = VersionForm(request.POST, instance = obj)
            if form_series.is_valid():
                form_series.save()
                messages.success(request, 'Cập nhật thành công')
            else:
                messages.error(request, "Cập nhật không thành công")
    except:
        form_series = SeriesForm()
    context = {"nav":nav, "form_series": form_series}
    return render(request, 'dashboard/db_update_series.html', context)

@admin_only
def list_category(request):
    nav = "categories"
    context = {"nav": nav}
    return render(request, "dashboard/db_list_category.html", context)

@admin_only
def create_category(request):
    nav = "categories"
    form = CategoryForm()
    if request.method == "POST":
        category_exists = Category.objects.filter(name__iexact=request.POST['name']).exists()
        if category_exists == False:
            form = CategoryForm(request.POST, request.FILES)
            if form.is_valid():
                form.save()
                messages.success(request, 'Create Success')
            else:
                messages.error(request, "Create not Success")
        else:
            form = CategoryForm()
            messages.error(request, f"Category {request.POST['name']} is available")
    else:
        form = CategoryForm()
    context = {"nav": nav, "form": form}
    return render(request, "dashboard/db_create_category.html", context)

@admin_only
def update_category(request, pk=None):
    nav = "categories"
    try:
        obj = get_object_or_404(Category, id=pk)
        form = CategoryForm(request.POST or None, instance = obj)
        if request.method == "POST":
            category_exists = Category.objects.filter(name__iexact=request.POST['name']).exists()
            if category_exists == False:
                forms = CategoryForm(request.POST, instance = obj)
                if form.is_valid():
                    forms.save()
                    messages.success(request, 'Update Success')
                else:
                    messages.error(request, "Update not Success")
            else:
                form = CategoryForm(request.POST, instance = obj)
                messages.error(request, f"Category {request.POST['name']} is available")
    except:
        form_series = SeriesForm()
    context = {"nav": nav, "form": form}
    return render(request, "dashboard/db_update_category.html", context)

@admin_only
def list_customers(request):
    nav = "customer"
    context = {"nav": nav}
    return render(request, "dashboard/db_list_customer.html", context)


@admin_only
def dashboard_json(request):
    data = {}
    data['total_orders'] = Order.objects.all().count()
    data['orders_delivered'] = Order.objects.filter(status='Accepted').count()
    data['orders_pending'] = Order.objects.filter(status='Pending').count()

    return JsonResponse(data, content_type="application/json", safe=False)

@admin_only
def get_bill(request, pk=None):
    order = Order.objects.get(id=pk)
    orderitems = order.orderitem_set.all()
    context = {'order': order, 'orderitems': orderitems}
    return render(request, 'dashboard/bill.html', context)

@admin_only
def review_rating(request):
    nav = "comments"
    comments = ReviewRating.objects.all().order_by("-updated_at")
    context = {'nav': nav, "comments": comments}
    return render(request, 'dashboard/comments.html', context)

@admin_only
def review_rating_detail(request, pk=None):
    nav = "comments"
    obj = get_object_or_404(ReviewRating, id=pk)
    form = ReviewRatingForm(instance=obj)
    context = {'nav': nav, "form": form}
    return render(request, 'dashboard/db_detail_comment.html', context)

@admin_only
def db_list_news(request):
    nav = "news"
    context = {'nav': nav}
    return render(request, 'dashboard/db_list_news.html', context)

@admin_only
def db_create_news(request):
    nav = "news"
    form = NewsForm()
    if request.method == "POST":
        form = NewsForm(request.POST, request.FILES)
        if form.is_valid():
            news = form.save(commit=False)
            news.user = request.user
            news.save()
            messages.success(request, 'Create Success')
        else:
            messages.error(request, "Create not Success")
    else:
        form = NewsForm()
    context = {'nav': nav, 'form': form}
    return render(request, 'dashboard/db_create_news.html', context)

@admin_only
def db_update_news(request, pk=None):
    nav = "news"
    obj = get_object_or_404(News, id=pk)
    form = NewsForm(instance=obj)
    if request.method == 'POST':
        form = NewsForm(request.POST, request.FILES, instance=obj)
        if form.is_valid():
            form.save()
            messages.success(request, 'Create Success')
        else:
            messages.error(request, "Create not Success")
    else:
        form = NewsForm(instance=obj)
    context = {"nav": nav, "form": form}
    return render(request, 'dashboard/db_update_news.html', context)

@admin_only
def view_report_orders(request):
    nav = "report"
    date = datetime.date.today()
    start_week = date - datetime.timedelta(date.weekday())
    end_week = start_week + datetime.timedelta(7)
    orders_by_week = Order.objects.filter(created_at__range=[start_week, end_week]).count()
    orders_by_month = Order.objects.filter(created_at__month=date.month).count()
    orders_by_year = Order.objects.filter(created_at__year=date.year).count()
    context = {"nav":nav, 'orders_by_week': orders_by_week, "orders_by_month": orders_by_month, "orders_by_year": orders_by_year}
    return render(request, "dashboard/dashboard_report.html", context)


def by_month(request):
    orders_by_months = []
    months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
    for month in range(1, 13):
        orders_by_months.append({
            "month": months[month-1],
            "quantity": Order.objects.filter(created_at__month=month).count()
        })
    return JsonResponse(orders_by_months, safe=False)
