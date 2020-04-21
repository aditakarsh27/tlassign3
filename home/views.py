from django.contrib.auth import authenticate, login
from django.contrib.auth import logout
from .forms import ItemForm, UserForm
from django.shortcuts import render, get_object_or_404, redirect
from .models import Item
from django.db.models import Q

def index(request):
    if not request.user.is_authenticated:
        return render(request, 'login.html')
    else:
        items = Item.objects.all()
        query = request.GET.get("q")
        if query:
            items = Item.objects.filter(
                Q(name__icontains=query) |
                Q(description__icontains=query)
            ).distinct()
        return render(request, 'index.html', {'items': items})


def detail(request, item_id):
    if not request.user.is_authenticated:
        return render(request, 'login.html')
    else:
        item=get_object_or_404(Item,pk=item_id)
        return render(request, 'detail.html', {'item' : item})

def login_user(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                return redirect('home:index')
            else:
                return render(request, 'login.html', {'error_message': 'Your account has been disabled'})
        else:
            return render(request, 'login.html', {'error_message': 'Invalid login'})
    return render(request, 'login.html')


def register(request):
    form = UserForm(request.POST or None)
    if form.is_valid():
        user = form.save(commit=False)
        username = form.cleaned_data['username']
        password = form.cleaned_data['password']
        user.set_password(password)
        user.save()
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                return redirect('home:index')
    context = {
        "form": form,
    }
    return render(request, 'register.html', context)

def logout_user(request):
    logout(request)
    form = UserForm(request.POST or None)
    context = {
        "form": form,
    }
    return redirect('home:login_user')

def create_item(request):
    if not request.user.is_authenticated:
        return render(request, 'login.html')
    else:
        form = ItemForm(request.POST or None)
        if form.is_valid():
            item = form.save(commit=False)
            item.user = request.user
            item.save()
            return redirect('home:index')
        context = {
            "form": form,
        }
        return render(request, 'create_item.html', context)


def delete_item(request, item_id):
    item = Item.objects.get(pk=item_id)
    item.delete()
    return redirect('home:index')

def edit_item(request, item_id):
    if not request.user.is_authenticated:
        return render(request, 'login.html')
    else:
        item = get_object_or_404(Item, pk=item_id)
        form = ItemForm(request.POST or None, instance=item)
        if form.is_valid():
            item.user = request.user
            item.save()
            return redirect('home:index')
        return render(request, 'create_item.html', {"form": form})
