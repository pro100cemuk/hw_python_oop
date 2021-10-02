import datetime as dt


class Record:
    DATE_NOW = dt.datetime.now().date()

    def __init__(self, amount, comment, date=None):
        format_date = '%d.%m.%Y'
        self.amount = amount
        self.comment = comment
        if date is None:
            self.date = self.DATE_NOW
        else:
            self.date = dt.datetime.strptime(date, format_date).date()


class Calculator:
    DATE_NOW = dt.datetime.now().date()

    def __init__(self, limit):
        self.limit = limit
        self.records = []

    def add_record(self, record):
        self.records.append(record)

    def get_today_stats(self):
        sum_day = 0
        for record in self.records:
            if record.date == self.DATE_NOW:
                sum_day += record.amount
        return sum_day

    def get_week_stats(self):
        sum_week = 0
        week = self.DATE_NOW - dt.timedelta(days=7)
        for record in self.records:
            if week < record.date <= self.DATE_NOW:
                sum_week += record.amount
        return sum_week


class CashCalculator(Calculator):
    USD_RATE = 60.00
    EURO_RATE = 70.00

    def __init__(self, limit):
        super().__init__(limit)
        self.currencies = {
            'rub': (1, 'руб'),
            'usd': (self.USD_RATE, 'USD'),
            'eur': (self.EURO_RATE, 'Euro')
        }

    def get_today_cash_remained(self, currency):
        today_stats = self.get_today_stats()
        result = abs((self.limit - today_stats) / self.currencies[currency][0])
        cur_name = self.currencies[currency][1]
        txt = 'Денег нет, держись'
        if today_stats < self.limit:
            return f'На сегодня осталось {result:.2f} {cur_name}'
        elif today_stats == self.limit:
            return f'{txt}'
        else:
            return f'{txt}: твой долг - {result:.2f} {cur_name}'


class CaloriesCalculator(Calculator):

    def get_calories_remained(self):
        today_stats = self.get_today_stats()
        result = self.limit - today_stats
        txt1 = 'Сегодня можно съесть что-нибудь ещё, но с общей калорийностью'
        txt2 = 'не более'
        txt3 = 'Хватит есть!'
        if today_stats >= self.limit:
            return f'{txt3}'
        else:
            return f'{txt1} {txt2} {result} кКал'
