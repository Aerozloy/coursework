# Метод в лоб
# инициализируем глобальные переменные
drivers = [
    {"name": "Водитель 1", "start_time": 6, "type": "white"},
    {"name": "Водитель 2", "start_time": 7, "type": "white"},
    {"name": "Водитель 3", "start_time": 8, "type": "black"},
    {"name": "Водитель 4", "start_time": 10, "type": "white"},
    {"name": "Водитель 5", "start_time": 11, "type": "black"},
    {"name": "Водитель 6", "start_time": 13, "type": "black"},
    {"name": "Водитель 7", "start_time": 16, "type": "white"},
    {"name": "Водитель 8", "start_time": 18, "type": "black"},
]  # Инициализируем переменную хранящую массив со словарем хранящим имя водителя, начало смены и тип водителя
rush_hour = [(7, 9), (17, 19)]  # инициализируем переменную с временем часов пик
shift_duration = 9  # Инициализируем переменную с длиной смены
interval_between_breaks = 3  # интервал между перерывами


def is_peak_hour(hour):  # функция проверки является ли время часом пик
    return any(start <= hour < end for start, end in rush_hour)


def break_distribution(shift_hours, driver_type):  # функция расчёта перерывов
    breaks = []  # инициализируем переменную с пустым массивом для хранения переменной
    not_rush_hour = [hour for hour in shift_hours if not is_peak_hour(hour)]  # не час пик

    if driver_type == "white":  # для водителей, работающих по белому
        for i, hour in enumerate(shift_hours):
            if hour in not_rush_hour and i >= 4:
                breaks.append(hour)  # добавляем перерыв в массив
                break  # завершаем цикл
    elif driver_type == "black":  # для водителей, работающих по черному
        first_break, second_break = 0, 0  # в перерывы засовываем нули для дальнейшего исправления
        for j, hour in enumerate(shift_hours):
            if hour in not_rush_hour and j >= 2:
                if first_break == 0:  # если первого перерыва нет
                    first_break = hour  # добавляем час перерыва в первый перерыв
                elif (hour - first_break) % 24 >= interval_between_breaks:
                    second_break = hour  # добавляем второй перерыв
                    break  # завершаем цикл
        if first_break:  # если есть первый перерыв
            breaks.append(first_break)  # добавляем его в массив перерывов
        if second_break:  # если есть второй перерыв
            breaks.append(second_break)  # добавляем его в массив перерывов
    return breaks  # возвращаем массив перерывов


def display_schedule(timetable):  # функция отображения распасиния
    for driver, hours in timetable.items():  # проходимся по водителям и их часам работы
        print(driver)
        for hour, activity in sorted(hours.items()):  # проходимся по часам и виду деятельности водителя
            print(hour, "00", activity)


def creating_drivers_timetable(driver):  # функция создания расписания водителей
    timetable = {}  # инициализируем пустой словарь для дальнейшего использования
    start_of_shift = driver['start_time']  # инициализируем переменную - начало смены
    end_of_shift = (start_of_shift + shift_duration) % 24  # инициализируем переменную - конец смены
    shift_hours = [(start_of_shift + i) % 24 for i in range(shift_duration)]  # инициализируем переменную - часы смены

    breaks = break_distribution(shift_hours, driver['type'])  # инициализируем переменную с перерывами

    for hour in shift_hours:  # перебираем часы из часов смены
        if hour == start_of_shift:  # если час равен началу смены
            timetable[hour] = 'Начало смены в часы пик' if is_peak_hour(hour) else 'Начало смены'
        elif hour in breaks:  # если час в перерыве
            timetable[hour] = 'Перерыв'
        elif is_peak_hour(hour):  # если час пик
            timetable[hour] = 'Работает в час пик'
        else:  # в остальных случаях
            timetable[hour] = 'Работает'

    timetable[end_of_shift] = 'Конец смены'
    return timetable  # возвращаем расписание


def schedule_creation():  # функция для создания общего расписания
    all_timetables = {}  # инициализируем словарь для дальнейшего хранения расписания водителей
    for driver in drivers:  # проходимся по всем 8 водителям
        all_timetables[driver['name']] = creating_drivers_timetable(driver)
    return all_timetables  # возвращаем расписание


schedule = schedule_creation()
display_schedule(schedule)  # запуск программы
