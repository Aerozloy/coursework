# Генетический алгоритм
from random import random, randint, sample  # импортируем инструменты из библиотеки рандом
from copy import deepcopy  # импортируем инструмент из библиотеки копи
drivers = [
    {"name": "Водитель 1", "start_time": 6, "type": "white"},
    {"name": "Водитель 2", "start_time": 7, "type": "white"},
    {"name": "Водитель 3", "start_time": 8, "type": "black"},
    {"name": "Водитель 4", "start_time": 10, "type": "white"},
    {"name": "Водитель 5", "start_time": 11, "type": "black"},
    {"name": "Водитель 6", "start_time": 13, "type": "black"},
    {"name": "Водитель 7", "start_time": 16, "type": "white"},
    {"name": "Водитель 8", "start_time": 18, "type": "black"},
]
shift_duration = 9
rush_hour = [(7, 9), (17, 19)]
interval_between_breaks = 3
population_size = 50  # размер популяции
generations = 100  # количество генераций
mutation_rate = 0.1  # шанс мутации


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


def creating_drivers_timetable(motorist):  # функция создания расписания водителей
    timetable = {}  # инициализируем пустой словарь для дальнейшего использования
    start_of_shift = motorist['start_time']  # инициализируем переменную - начало смены
    end_of_shift = (start_of_shift + shift_duration) % 24  # инициализируем переменную - конец смены
    shift_hours = [(start_of_shift + i) % 24 for i in range(shift_duration)]  # инициализируем переменную - часы смены

    breaks = break_distribution(shift_hours, motorist['type'])  # инициализируем переменную с перерывами

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


def randomize_schedule():
    return [{**chauffeur, 'start_time': randint(6, 18)} for chauffeur in drivers]


def suitability(schedule):
    penalty, peak_hours_coverage = 0, 0
    for chauffeur in schedule:
        shift = creating_drivers_timetable(chauffeur)
        for hour, activity in shift.items():
            if is_peak_hour(hour) and activity == 'Работает в час пик':
                peak_hours_coverage += 1
            if activity == 'Break' and is_peak_hour(hour):
                penalty += 10
    return peak_hours_coverage - penalty


def crossover(parent1, parent2):
    return [deepcopy(d1 if random() > 0.5 else d2) for d1, d2 in zip(parent1, parent2)]


def mutate(schedule):
    return [{**operator, 'start_time': randint(6, 18)} if random() < mutation_rate else operator for operator in
            schedule]


def genetic_algorithm():
    population = [randomize_schedule() for _ in range(population_size)]

    for generation in range(generations):
        population.sort(key=lambda s: -suitability(s))
        print(f"Generation {generation}, Best Fitness: {suitability(population[0])}")

        new_population = population[:10]
        while len(new_population) < population_size:
            parent1, parent2 = sample(population[:20], 2)
            child = mutate(crossover(parent1, parent2))
            new_population.append(child)

        population = new_population

    return population[0]


best_schedule = genetic_algorithm()  # Выбираем лучшее расписание с помощью генетического алгоритма
print("\nЛучшее расписание")
for driver in best_schedule:  # Перебираем водителей из лучшего расписания
    print(driver['name'], "Начал в", driver['start_time'], "00")
