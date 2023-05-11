from django.db import models
from django.urls import reverse, reverse_lazy
from django.contrib.auth.models import User


class Category(models.Model):
    name = models.CharField(max_length=120, verbose_name='Название')
    description = models.TextField(blank=True, null=True, verbose_name='Описание')

    class Meta:  # Класс для названия нашей модели в админке
        verbose_name = 'Категория'  # Название в единственном числе
        verbose_name_plural = 'Категории'  # Надпись во множественном числе

class Tours(models.Model):
    name = models.CharField(max_length=120, default='tour', verbose_name='Название')
    description = models.TextField(blank=True, null=True, verbose_name='Описание')
    price = models.FloatField(default=10, verbose_name='Стоимость')
    date_create = models.DateField(auto_now_add=True, verbose_name='Дата создания')
    date_update = models.DateTimeField(auto_now=True, null=True, verbose_name='Дата изменения')
    photo = models.ImageField(upload_to='static/img/gallery', verbose_name='Фотография')
    exist = models.BooleanField(default=True, verbose_name='Активно')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='tours')


    # CASCADE - удаляет дочернюю запись при удалении родительской
    # PROTECT - защищает от удаления родительской записи
    # SET_NULL - при удалении родителя ставит Null (null=True)
    # SET_DEFAULT - при удалении родителя ставит значение по умолчанию (параметр default необходим)
    # DO_NOTHING - при удалении родителя ничего не происходит
    def __str__(self):
        # Переопределение названия объекта
        return self.name

    def get_absolute_url(self):
        return reverse('tour_delete', args=[str(self.pk)])

    class Meta:  # Класс для названия нашей модели в админке
        verbose_name = 'Тур'  # Название в единственном числе
        verbose_name_plural = 'Туры'  # Надпись во множественном числе
        # ordering = ['name'] # Сортировка полей (по возрастанию)
        # ordering = ['-name']  # Сортировка полей (по убыванию)
        # ordering = ['name', 'price']  # Сортировка полей (по возрастанию)

class TourImage(models.Model):
    tour = models.ForeignKey(Tours, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='static/img/gallery')

class Favourite(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    tour = models.ForeignKey(Tours, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('user', 'tour')


class Cart(models.Model):
    owner = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name='Владелец')
    # Добавляем ForeignKey на Tours, чтобы хранить ссылку на конкретный тур
    items = models.ManyToManyField('Tours', through='CartItem', related_name='carts', verbose_name='Товары')

    def __str__(self):
        return f'Корзина {self.owner.username}'

    def get_total_quantity(self):
        return sum(item.quantity for item in self.items.all())

    def get_total_price(self):
        return sum(item.tour.price * item.quantity for item in self.items.all())

    def remove(self, product):
        cart_item = CartItem.objects.filter(cart = self, tour = product).first()
        if cart_item:
            cart_item.delete()

    def add(self, product, quantity, update_quantity=False):
        cart_item, created = CartItem.objects.get_or_create(cart = self, tour = product)
        if created:
            cart_item.quantity = quantity
        else:
            if update_quantity:
                cart_item.quantity = quantity
            else:
                cart_item.quantity += quantity
        cart_item.save()


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, verbose_name='Корзина')
    tour = models.ForeignKey('Tours', on_delete=models.CASCADE, verbose_name='Тур')
    quantity = models.PositiveIntegerField(default=1, verbose_name='Количество')

    def __str__(self):
        return f'{self.quantity} шт. {self.tour.name} в корзине {self.cart.owner.username}'









# ID (Django автоматически создаст)
# name
# description
# price
# date_create
# date_expired
# photo
# exist (Логическое удаление)
# class Supplier(models.Model):
#     title = models.CharField(max_length=150, verbose_name='Название поставщика')
#     agent_name = models.CharField(max_length=100, verbose_name='Имя агента поставщика')
#     agent_firstname = models.CharField(max_length=100, verbose_name='Фамилия агента поставщика')
#     agent_patronymic = models.CharField(max_length=100, verbose_name='Отчество агента поставщика')
#     exist = models.BooleanField(default=True, verbose_name='Сотрудничаем?')
#
#     def get_absolute_url(self):
#         return reverse('info_supp_view', kwargs={'supplier_id': self.pk})
#
#     def __str__(self):
#         return self.title
#
#     class Meta:  # Класс для названия нашей модельки в админке
#         verbose_name = 'Поставщик'  # Надпись в единственном числе
#         verbose_name_plural = 'Поставщики'  # Надпись во множественном числе
#         ordering = ['title']  # Сортировка полей
#
#
# class Order(models.Model):
#     date_create = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания заказа')
#     date_finish = models.DateTimeField(null=True, blank=True, verbose_name='Дата завершения заказа')
#     price = models.FloatField(null=True, verbose_name='Стоимость заказа')
#     address_delivery = models.CharField(max_length=150, verbose_name='Адрес доставки')
#     status = models.CharField(max_length=150, verbose_name='Статус',
#                               choices=[
#                                   ('1', 'Создан'),
#                                   ('2', 'Отменён'),
#                                   ('3', 'Согласован'),
#                                   ('4', 'В пути'),
#                                   ('5', 'Завершён')
#                               ]
#                               )
#
#     # fruits = models.ManyToManyField(Fruit) # обычное создание связи М к М, через техническую таблицу Fruit_order
#     fruits = models.ManyToManyField(Fruit, through='Pos_order')  # создание связи М к М, через таблицу Pos_order
#
#     def __str__(self):
#         return f"{self.date_create} {self.status} {self.price}"
#
#     class Meta:  # Класс для названия нашей модельки в админке
#         verbose_name = 'Заказ'  # Надпись в единственном числе
#         verbose_name_plural = 'Заказы'  # Надпись во множественном числе
#         ordering = ['date_create']  # Сортировка полей
#
#
# class Pos_order(models.Model):
#     fruit = models.ForeignKey(Fruit, on_delete=models.PROTECT, verbose_name='Фрукт')
#     order = models.ForeignKey(Order, on_delete=models.PROTECT, verbose_name='Заказ')
#     count_fruit = models.IntegerField(verbose_name='Количество фруктов')
#     price = models.FloatField(verbose_name='Общая цена фруктов')
#
#     def __str__(self):
#         return self.fruit.name + " " + self.order.address_delivery + " " + self.order.status
#
#     class Meta:  # Класс для названия нашей модельки в админке
#         verbose_name = 'Позиция'  # Надпись в единственном числе
#         verbose_name_plural = 'Позиции'  # Надпись во множественном числе
#         ordering = ['fruit', 'order', 'price']  # Сортировка полей
#
#
# class Chegue(models.Model):
#     date_print = models.DateTimeField(auto_now_add=True, verbose_name='Дата распечатки')
#     address_print = models.CharField(max_length=150, verbose_name='Место создания чека')
#     terminal = models.CharField(max_length=10, verbose_name='Код терминала')
#     order = models.OneToOneField(Order, on_delete=models.PROTECT, primary_key=True, verbose_name='Заказ')
#
#     # primary_key=False - Поле id и Поле order - раздельны
#     # primary_key=True - Поле order Первичный и Внешний ключ
#
#     def __str__(self):
#         return str(self.date_print) + " " + self.terminal
#
#     class Meta:  # Класс для названия нашей модельки в админке
#         verbose_name = 'Чек'  # Надпись в единственном числе
#         verbose_name_plural = 'Чеки'  # Надпись во множественном числе
#         ordering = ['terminal', 'date_print']  # Сортировка полей
