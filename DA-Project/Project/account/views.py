from .models import User
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .forms import RegistrationForm, UserForm
from django.contrib.auth.decorators import login_required
from .decorators import unauthenticated_user
from django.contrib.auth.models import Group

@unauthenticated_user
def loginPage(request):
    if request.method=='POST':
        email = request.POST['email']
        password = request.POST['password']
        user = authenticate(request, email=email, password=password)
        if user is not None:
            login(request, user)
            next_url = request.GET.get('next')
            if next_url:
                return redirect(next_url)
            else:
                return redirect('shop:home')
        else:
            messages.error(request, 'Email hoặc mật khẩu không chính xác')
            return redirect('account:login')
    return render(request, 'account/login.html')


@unauthenticated_user
def registerPage(request):
    form = RegistrationForm()
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            full_name = form.cleaned_data['full_name']
            phone = form.cleaned_data['phone']
            address = form.cleaned_data['address']
            password = form.cleaned_data['password']
            user = User.objects.create_user(
                email=email,
                full_name=full_name,
                password=password,
            )
            user.active = True
            user.save()
            group, created = Group.objects.get_or_create(name="customer")
            user.groups.add(group)

            messages.success(request, 'Bạn đã đăng ký thành công')
            return redirect('account:login')
    context = {'form':form}
    return render(request, 'account/register.html', context)


@login_required
def logoutPage(request):
    logout(request)
    return redirect('account:login')


def update(request):
    if request.user.is_authenticated:
        context = {}
        obj = get_object_or_404(User, email=request.user)
        form = UserForm(request.POST or None, instance = obj)
        if form.is_valid():
            form.save()
            messages.success(request, 'Bạn đã cập nhật thành công')
            return redirect('account:update')
    context = {'form': form}
    return render(request, 'account/update-account.html', context)