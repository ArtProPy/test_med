from django.db import models


class Сlients(models.Model):
    name = models.CharField('Имя клиента', max_length=255)

    def __str__(self):
        return self.name

    class Meta:
        app_label = 'bills'
        verbose_name = 'Клиент'
        verbose_name_plural = 'Клиенты'


class Organisation(models.Model):
    name = models.CharField('Имя клиента', max_length=255)

    def __str__(self):
        return self.name

    class Meta:
        app_label = 'bills'
        verbose_name = 'Организация'
        verbose_name_plural = 'Организации'


class Service(models.Model):
    name = models.CharField('Название услуги', max_length=255)

    def __str__(self):
        return self.name

    class Meta:
        app_label = 'bills'
        verbose_name = 'Услуга'
        verbose_name_plural = 'Услуги'


class Bill(models.Model):
    client_name = models.ForeignKey(
        Сlients,
        on_delete=models.CASCADE,
        related_name='bills'
    )
    client_org = models.ForeignKey(
        Organisation,
        on_delete=models.CASCADE,
        related_name='bills'
    )
    num = models.PositiveIntegerField('Номер счёта')
    sum = models.FloatField('Сумма')
    date = models.DateField('Дата')

    def __str__(self):
        return f'{self.num:05} {self.client_name.name}'

    class Meta:
        app_label = 'bills'
        verbose_name = 'Счёт'
        verbose_name_plural = 'Счёта'


class ServiceBill(models.Model):
    service = models.ForeignKey(
        Service,
        on_delete=models.CASCADE,
        related_name='bills'
    )
    bill = models.ForeignKey(
        Bill,
        on_delete=models.CASCADE,
        related_name='services'
    )

    def __str__(self):
        return f'{self.service.name} - {self.bill.name}'

    class Meta:
        app_label = 'bills'
        verbose_name = 'Услуга-Счёт'
        verbose_name_plural = 'Услуги-Счёта'
