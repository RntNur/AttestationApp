from django.contrib import messages
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.views import LoginView
from django.http import HttpResponse
from django.utils.decorators import method_decorator
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.db.models import Sum
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.decorators.http import require_POST
from django.core.paginator import Paginator
from app.forms import ToursForm, CartForm, CartAddProductForm, ContactForm
from app.forms import UserRegistrationForm, LoginForm
from django.contrib.auth import login, authenticate, logout
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from app.models import Tours, Cart, CartItem, TourImage
from django.views.decorators.csrf import requires_csrf_token
from django.shortcuts import render

from django.http import JsonResponse
from .serializer import TourSerializer

from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import viewsets

from django.core.mail import send_mail, send_mass_mail
from django.conf import settings


# вывод списка по api для его редактирования
@api_view(['GET', 'POST'])
def tour_api_list(request):
    if request.method == 'GET':
        tour_list = Tours.objects.all()
        serializer = TourSerializer(tour_list, many = True)
        return Response({'tour_list': serializer.data})
    elif request.method == 'POST':
        serializer = TourSerializer(data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status = status.HTTP_201_CREATED)
        return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)


# функция обработки действий с данными продуктов через api
@api_view(['GET', 'PUT', 'DELETE'])
def tour_api_detail(request, pk, format=None):
    tour_obj = get_object_or_404(Tours, pk = pk)
    if tour_obj.exist:
        if request.method == 'GET':
            serializer = TourSerializer(tour_obj)
            return Response(serializer.data)
        elif request.method == 'PUT':
            serializer = TourSerializer(tour_obj, data = request.data)
            if serializer.is_valid():
                serializer.save()
                return Response({'message': 'Данные успешно изменены', 'tour': serializer.data})
            return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)
        elif request.method == 'DELETE':
            tour_obj.delete()
            return Response(status = status.HTTP_204_NO_CONTENT)
    else:
        return Response(status = status.HTTP_404_NOT_FOUND)


# главная страница
def index_template(request):
    return render(request, 'index.html')


# функция регистрации новго пользоввателя
def user_reg(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit = False)
            user.first_name = form.cleaned_data['first_name']
            user.last_name = form.cleaned_data['last_name']
            # Set the hashed password
            password = form.cleaned_data['password']
            user.set_password(password)
            user.save()
            return redirect('login')
    else:
        form = UserRegistrationForm()
    return render(request, 'registration.html', {'form': form})


# ОБработчик авторизации пользователя
class UserLoginView(LoginView):
    form_class = AuthenticationForm
    template_name = 'login.html'
    success_url = 'index'


# функция выйти-разлогиниться
def user_logout(request):
    logout(request)
    return redirect('login')


# функция страницы с контактными данными и обратной связью
def contacts(request):
    return render(request, 'contacts.html')


# Список продуктов
class TourList(ListView):
    model = Tours
    template_name = 'as_view/tourlist.html'
    context_object_name = 'tours'
    extra_context = {'title': 'Cписок туров'}
    paginate_by = 4

    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     context['images'] = TourImage.objects.filter(tour=self.object)
    #     context['cart_form'] = CartAddProductForm()
    #     return context


# Создание продукта
class TourCreate(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = Tours
    form_class = ToursForm
    template_name = 'as_view/touradd.html'
    context_object_name = 'tour_add'
    extra_context = {'title': 'Создание тура'}

    def test_func(self):
        return self.request.user.is_superuser

    def handle_no_permission(self):
        return redirect('tour_list')

    def form_valid(self, form):
        form.instance.author = self.request.user
        self.object = form.save()
        messages.success(self.request, f'Тур "{self.object.name}" успешно добавлен!')
        # Добавление дополнительных изображений к продукту
        if self.request.FILES.getlist('additional_images'):
            for img in self.request.FILES.getlist('additional_images'):
                TourImage.objects.create(tour = self.object, image = img)

        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('tour_detail', args = [self.object.pk])


# Обработчик раздела с деталями о продукте
class TourDetail(DetailView):
    model = Tours
    template_name = 'as_view/tourdetail.html'
    context_object_name = 'tour_info'
    extra_context = {'title': 'Детали тура'}
    success_url = reverse_lazy('tour_detail')

    def get_success_url(self):
        pk = self.kwargs.get('pk')
        return reverse_lazy('tour_detail', args = [pk])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['cart_form'] = CartAddProductForm()
        return context


# изменение карточки продукта
class TourUpdate(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Tours
    fields = ['name', 'description', 'price', 'photo', 'exist', 'category']
    template_name = 'as_view/touredit.html'
    context_object_name = 'form'
    extra_context = {'title': 'Изменение тура'}

    def test_func(self):
        return self.request.user.is_superuser

    def handle_no_permission(self):
        return redirect('tour_list')

    def get_success_url(self):
        pk = self.kwargs.get('pk')
        return reverse_lazy('tour_detail', args = [pk])

# удаление карточки продукта
class TourDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Tours
    success_url = reverse_lazy('tour_list')
    template_name = 'as_view/tours_confirm_delete.html'

    def test_func(self):
        return self.request.user.is_superuser

    def handle_no_permission(self):
        return redirect('tour_list')


# Обработчик для форма обратной связи
def contact_email(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            mail = send_mail(
                form.cleaned_data['subject'],
                form.cleaned_data['content'],
                settings.EMAIL_HOST_USER,
                ['rrnurullin777@gmail.com'],
                fail_silently = False
            )
            if mail:
                return redirect('index')
    else:
        form = ContactForm()
    return render(request, 'contacts.html', {'form': form})

@requires_csrf_token
def csrf_failure(request, reason=""):
    context = {'message': 'CSRF Token Failure'}
    return render(request, 'csrf_failure.html', context)


# def pagi(request):
#     all_posts = Tours.objects.all()
#     paginator = Paginator(all_posts, 4)  # Показывает 10 записей на странице
#
#     page_number = request.GET.get('page')
#     page_obj = paginator.get_page(page_number)

    # return render(request, 'as_view/tourlist.html', {'page_obj': page_obj})