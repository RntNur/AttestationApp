from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from app.models import Tours, Favourite
from .cart import Cart
from .forms import CartAddProductForm

# Обработчик для раздела "Избранное"
def favourite_list(request):
    if request.user.is_authenticated:
        favourites = Favourite.objects.filter(user=request.user)
        favourite_tours = [favourite.tour for favourite in favourites]
    else:
        return redirect('login')

    return render(request, 'favourite_list.html', {'tours': favourite_tours})

# Обработчик для кнопки добавления/удаления в "Избранное"
@require_POST
def favourite_add(request, pk):
    if request.user.is_authenticated:
        tour = get_object_or_404(Tours, id=pk)
        favourite, created = Favourite.objects.get_or_create(user=request.user, tour=tour)

        if created:
            is_favourite = True
        else:
            favourite.delete()
            is_favourite = False
        return JsonResponse({'is_favourite': is_favourite})

    else:
        return JsonResponse({'error': 'Пользователь не авторизован'})

# Добавление объекта в корзину
@require_POST
def cart_add(request, pk):
    cart = Cart(request)
    product = get_object_or_404(Tours, id = pk)
    form = CartAddProductForm(request.POST)
    if form.is_valid():
        cd = form.cleaned_data
        cart.add(product = product,
                 quantity = cd['quantity'],
                 update_quantity = cd['update'])
    return redirect('cart')

# Обработчик для отображения раздела "Корзина"
def cart_detail(request):
    cart = Cart(request)
    return render(request, 'cart.html', {'cart': cart})


# Удаление объекта в корзине
def cart_remove(request, pk):
    cart = Cart(request)
    product = get_object_or_404(Tours, id = pk)
    cart.remove(product)
    return redirect('cart')

# Обработчик кнопки очистить корзину
def cart_remove_all(request, products=None):
    cart = Cart(request)
    if products == 'all':
        cart.clear()
    return redirect('cart')

# Обработчик кнопки "оформить заказ"
def order(request):
    return render(request, 'order.html')



