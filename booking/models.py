from django.db import models

# Create your models here.
class Airport(models.Model):
    code = models.CharField(max_length=5, unique=True, verbose_name="IATA код")
    name = models.CharField(max_length=200, verbose_name="Назва аеропорту")
    city = models.CharField(max_length=100, verbose_name="Місто")
    country = models.CharField(max_length=100, verbose_name="Країна")

    class Meta:
        verbose_name = "Аеропорт"
        verbose_name_plural = "Аеропорти"
        ordering = ['city', 'code']

    def __str__(self):
        return f"{self.city} ({self.code})"

class Airline(models.Model):
    name = models.CharField(max_length=200, verbose_name="Назва авіакомпанії")
    code = models.CharField(max_length=5, unique=True, verbose_name="IATA код")
    country = models.CharField(max_length=100, verbose_name="Країна")

    class Meta:
        verbose_name = "Авіакомпанія"
        verbose_name_plural = "Авіакомпанії"
        ordering = ['name']

    def __str__(self):
        return f"{self.name} ({self.code})"

class Flight(models.Model):
    flight_number = models.CharField(max_length=10, unique=True, verbose_name="Номер рейсу")
    airline = models.ForeignKey(Airline, on_delete=models.CASCADE, verbose_name="Авіакомпанія")
    departure_airport = models.ForeignKey(Airport, on_delete=models.CASCADE, related_name='departure', verbose_name="Відправлення")
    arrival_airport = models.ForeignKey(Airport, on_delete=models.CASCADE, related_name='arrival', verbose_name="Прибуття")
    departure_time = models.DateTimeField(verbose_name="Час відправлення")
    arrival_time = models.DateTimeField(verbose_name="Час прибуття")
    aircraft_type = models.CharField(max_length=50, blank=True, null=True, verbose_name="Тип літака")
    price = models.DecimalField(max_digits=8, decimal_places=2,  verbose_name="Базова ціна")

    class Meta:
        verbose_name = "Рейс"
        verbose_name_plural = "Рейси"
        ordering = ['departure_time']

    def __str__(self):
        return f"{self.airline} {self.flight_number}: {self.departure_airport} - {self.arrival_airport}"

class Passenger(models.Model):
    first_name = models.CharField(max_length=50, verbose_name="Ім'я")
    last_name = models.CharField(max_length=50, verbose_name="Прізвище")
    date_of_birth = models.DateField(verbose_name="Дата народження")
    passport_number = models.CharField(max_length=20, unique=True, verbose_name="Номер паспорта")
    nationality = models.CharField(max_length=50, verbose_name="Громодянство")
    email = models.EmailField(max_length=254, verbose_name="Електронна пошта")
    phone = models.CharField(max_length=20, verbose_name="Телефон")

    class Meta:
        verbose_name = "Пасажир"
        verbose_name_plural = "Пасажири"
        ordering = ['last_name', 'first_name']

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

class Booking(models.Model):
    flight = models.ForeignKey(Flight, on_delete=models.CASCADE, verbose_name="Рейс")
    passenger = models.ForeignKey(Passenger, on_delete=models.CASCADE, verbose_name="Пасажир")
    booking_date = models.DateTimeField(auto_now_add=True, verbose_name="Дата бронювання")
    seat_number = models.CharField(max_length=10, verbose_name="Номер місця")
    travel_class = models.CharField(
        max_length=20,
        choices=[('Business', 'Бізнес'), ('Economy', 'Економ'), ("First", "Перший клас")],
        default='Economy',
        verbose_name="Клас подорожі"
    )
    status = models.CharField(
        max_length=20,
        choices=[('Booked', 'Заброньовано'), ('Checked-in', 'Реєстрація завершена'), ('Cancelled', 'Скасовано')],
        default='Booked',
        verbose_name="Статус"
    )

    class Meta:
        verbose_name = "Бронювання"
        verbose_name_plural = "Бронювання"
        ordering = ['-booking_date']

    def __str__(self):
        return f"Бронювання {self.id} - {self.passenger} на рейс {self.flight}"

class Payment(models.Model):
    booking = models.ForeignKey(Booking, on_delete=models.CASCADE, verbose_name="Бронювання")
    payment_date = models.DateTimeField(auto_now_add=True, verbose_name="Дата оплати")
    amount = models.DecimalField(max_digits=8, decimal_places=2, verbose_name="Сума оплати")
    method = models.CharField(
        max_length=20,
        choices=[('Card', 'Карта'), ('PayPal', 'PayPal'), ('Cash', 'Готівка')],
        verbose_name="Метод оплати"
    )
    status = models.CharField(
        max_length=20,
        choices=[('Paid', 'Оплачено'), ('Pending', 'В очікуванні'), ('Failed', 'Помилка')],
        default='Pending',
        verbose_name="Статус"
    )

    class Meta:
        verbose_name = "Оплата"
        verbose_name_plural = "Оплати"
        ordering = ['-payment_date']

    def __str__(self):
        return f"Оплата {self.id} - {self.amount} ({self.status})"

class Ticket(models.Model):
    booking = models.OneToOneField("Booking", on_delete=models.CASCADE, verbose_name="Бронювання")
    ticket_number = models.CharField(max_length=20, unique=True, verbose_name="Номер квитка")
    issue_date = models.DateTimeField(auto_now_add=True, verbose_name="Дата видачі")
    is_active = models.BooleanField(default=True, verbose_name="Дійсний квиток")

    class Meta:
        verbose_name = "Квиток"
        verbose_name_plural = "Квитки"
        ordering = ["-issue_date"]

    def __str__(self):
        return f"Квиток {self.ticket_number} ({self.booking.passenger})"