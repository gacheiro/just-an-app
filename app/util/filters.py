
def weekday(date):
    return {
        0: 'segunda-feira',
        1: 'terça-feira',
        2: 'quarta-feira',
        3: 'quinta-feira',
        4: 'sexta-feira',
        5: 'sábado',
        6: 'domingo',
    }[date.weekday()]


def datetimeformat(value, format='(%d/%m/%Y) às %H:%M'):
    return value.strftime(format)
