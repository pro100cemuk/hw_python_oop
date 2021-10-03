import datetime as dt


class Record:

    def __init__(self, amount, comment, date=None):
        format_date = '%d.%m.%Y'
        self.amount = amount
        self.comment = comment
        if date is None:
            self.date = dt.date.today()
        else:
            self.date = dt.datetime.strptime(date, format_date).date()


class Calculator:

    def __init__(self, limit):
        self.limit = limit
        self.records = []

    def add_record(self, record):
        self.records.append(record)

    def get_today_stats(self):
        today_amount = [record.amount for record in self.records
                        if record.date == dt.date.today()]
        return sum(amount for amount in today_amount)

    def get_week_stats(self):
        week = dt.date.today() - dt.timedelta(days=7)
        week_amount = [record.amount for record in self.records
                       if week < record.date <= dt.date.today()]
        return sum(amount for amount in week_amount)

    def get_calculate(self):
        return (self.limit - self.get_today_stats())


class CashCalculator(Calculator):
    USD_RATE = 60.00
    EURO_RATE = 70.00

    def get_today_cash_remained(self, currency):
        self.currency = currency
        self.currencies = {
            'rub': (1.00, 'руб'),
            'eur': (self.EURO_RATE, 'Euro'),
            'usd': (self.USD_RATE, 'USD')
        }
        result = abs(self.get_calculate() / self.currencies[self.currency][0])
        cur_name = self.currencies[self.currency][1]
        txt = 'Денег нет, держись'
        if self.get_today_stats() < self.limit:
            return f'На сегодня осталось {result:.2f} {cur_name}'
        elif result == 0:
            return f'{txt}'
        else:
            return f'{txt}: твой долг - {result:.2f} {cur_name}'


class CaloriesCalculator(Calculator):

    def get_calories_remained(self):
        result = self.get_calculate()
        txt1 = ('Сегодня можно съесть что-нибудь ещё, '
                'но с общей калорийностью не более')
        txt2 = 'Хватит есть!'
        if result <= 0:
            return f'{txt2}'
        else:
            return f'{txt1} {result} кКал'
