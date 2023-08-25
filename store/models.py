from django.db import models
from datetime import datetime, timezone


class Staff(models.Model):
    director = 'DI'
    admin = 'AD'
    cook = 'CO'
    cashier = 'CA'
    cleaner = 'CL'

    POSITIONS = [
        (director, 'Директор'),
        (admin, 'Администратор'),
        (cook, 'Повар'),
        (cashier, 'Кассир'),
        (cleaner, 'Уборщик')
    ]

    full_name = models.CharField(max_length=255)
    position = models.CharField(max_length=2, choices=POSITIONS)
    labor_contract = models.IntegerField()

    def __str__(self):
        return f'{self.full_name}'


class Product(models.Model):
    name = models.CharField(max_length=255)
    price = models.FloatField(default=0.0)
    composition = models.TextField(default="Состав не указан")

    def __str__(self):
        return f'{self.name}'

    def get_last_name(self):
        return self.full_name.split()[0]



class Order(models.Model):
    time_in = models.DateTimeField(auto_now_add=True)
    time_out = models.DateTimeField(null=True)
    cost = models.FloatField(default=0.0)
    pickup = models.BooleanField(default=False)
    complete = models.BooleanField(default=False)
    staff = models.ForeignKey(Staff, on_delete=models.CASCADE)
    products = models.ManyToManyField(Product, through='ProductOrder')

    def get_duration(self):
        if self.complete:  # если завершён, возвращаем разность объектов
            return (self.time_out - self.time_in).total_seconds() // 60
        else:  # если ещё нет, то сколько длится выполнение
            return (datetime.now(timezone.utc) - self.time_in).total_seconds() // 60

    def finish_order(self):
        self.time_out = datetime.now()
        self.complete = True
        self.save()


class ProductOrder(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    amount = models.IntegerField(default=1)

    def product_sum(self):
        product_price = self.product.price
        return product_price * self.amount


    # 'Вспомним, что мы поле position определили как СhoiceField — поле с возможностью выбора. ' \
    # 'Знакомимся ещё с одной классной фишкой Django. Он автоматически добавляет метод вида get' \
    # '_FOO_display(), где FOO — это название поля. Здесь мы и можем видеть, зачем нам нужно было ' \
    # 'задавать кортеж. Первое значение фактически хранится в базе данных, а с помощью второго метода' \
    # ' можно получить любую другую строку, связанную с этим объектом!'