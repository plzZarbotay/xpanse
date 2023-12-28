import numpy as np
from numpy import log as ln
from numpy import cos as cos
from numpy import sqrt
from numpy import radians as convert
import time
import math
from progress.bar import IncrementalBar
from progress.bar import Bar
import random

def tsialkovsky_rocket_velocity(F, M_0, I_sp, g_0, t):
    return -g_0 * I_sp * ln(g_0 * I_sp * M_0 - F * t) + g_0 * I_sp * ln(g_0 * I_sp * M_0)

def specific_impulse(F, delta_m, g_0):
    return F / (delta_m * g_0)

def velocity(V0, a, t):
    return V0 + a*t

def delta_velocity(M_t, M_0, I_sp, g_0):
    return -g_0 * I_sp * ln(1 - M_t / M_0)

def burn_time(delta_V, M_0, F, I_sp, g_0):
    return (g_0 * I_sp * M_0 * (1 - math.e**(-delta_V / (g_0 * I_sp)))) / F
    
def aerodynamic_resistance(p,v,Ca,A):
    # Из опен фоам
    return (1/2)*p*v**2*Ca*A
def lift(Cl,p,v,S):
    return Cl / 2 * p * v**2 * S
def lift_wing(Cl,p,v):
    return Cl / 2 * p * v**2
def wheel_friction_force(m,g_0):
    return 0.7 * m * g_0
def acceleration_condtion(m,a,F,D,Ftr,g_0):
    return m*a == (F - D - wheel_friction_force(m,g_0))
def approach_acceleration(Ft,m,D,g0):
    return ((Ft - 0.7 * m * g0) - D) / m
def acceleration_condtion_force(Ft,D,m):
    return ((Ft - D)*cos(convert(10)))/m

#------------- КРАСИВОЕ НАЧАЛО ------------
print("Выбор режима:")
print("0 - Скоростной")
print("1 - Медленный")
mode = input()
if mode == '1':
    print('Подготавливаю симмуляцию...')
    bar = Bar('Собираем данные', max=39)
    for i in range(39):
        time.sleep(random.uniform(0.2,0.5))
        bar.next()
    bar.finish()
    bar = Bar('Прокладываю маршрут', max=21)
    for i in range(21):
        time.sleep(random.uniform(0.2,0.5))
        bar.next()
    bar.finish()
    bar = Bar('Последние подготовления', max=19)
    for i in range(19):
        time.sleep(random.uniform(0.2,0.5))
        bar.next()
    bar.finish()
# -----------------------------------------

#  ---- Общий конфиг ----   
g_0 = 9.81 # 
p_air = 1.2255 # плотность воздуха (кг/м³)
F = 363000 # тяга двигателя (Н)
Cd = 2.424121 # коэффициент сопротивления
M_0 = 24805  # начальная масса ракеты (кг)
I_sp = 6024  # удельный импульс (сек)
t = 450  # время прожига/секунда

# --- 0 Этап ( Конфиг ) ---
# Разгон
M_t = 11000  # начальная масса ракеты (кг)
V0_r = 0
g_0 = 9.81 # 
p_air = 1.2255 # плотность воздуха (кг/м³)
seconds = [0,1,2,3,5,6,7,15,18,19,19.87, 20]
delta_M = 15 # кг/c
A = 3.94 # Площадь поперечного сечения аппарата (м^2)

rocket_speed = tsialkovsky_rocket_velocity(F, M_0, I_sp, g_0, t)
print("Характерестическая скорость: ", rocket_speed)

# Этап разгона
# График ускорение/секунда , скорость секунда
# Запускаем симмуляцию разгона
print('Разгон')
current_rocket_speed = 0
for second in seconds:
    M_0 = M_0 - delta_M
    D = aerodynamic_resistance(p_air,current_rocket_speed,Cd,A)
    a_r = approach_acceleration(F,M_0,D,g_0)
    current_rocket_speed = velocity(V0_r,a_r,second)
    # Посчитаем Аэродинамическое сопротивление
    print(f'Текущая скорость ракеты разгон: {current_rocket_speed } м/с')

print("-------------------------")
print("-------------------------")
print("Разгон закончен! Данные:")
print("-------------------------")
print(f'Масса ракеты: {M_0} кг')
print("Условия отрыва выполнены!")
print(f'Скорость при отрыве: {current_rocket_speed}')
print(f'Ускорение при отрыве: {a_r}')
print("-------------------------")
print("-------------------------")

# --- 1 Этап (Конфиг) ---
#Параметры ракеты ( ПОДСТАВИТЬ ЗНАЧЕНИЯ)
S_wing_area = 16 # площадь 2 крыльев (м^2)
M_t = 11000# масса топлива ракеты (кг)
g_0 = 9.81 # 
V0 = current_rocket_speed 
seconds = [0,10,15,20,30,50,60, 70,90, 120, 150, 160]
air_speed = 150 # м/с
# Запускаем симмуляцию взлета
po_massive = [1.2,1.2,1.2, 1,1, 0.8, 0.8, 0.53, 0.53, 0.32, 0.17, 0.09, 0.05 ]
current = 0
for second in seconds:
    M_0 = M_0 - delta_M
    #print(M_0)
    D = aerodynamic_resistance(po_massive[current], air_speed,Cd,A)
    a = acceleration_condtion_force(F,D,M_0)
    current_rocket_speed = velocity(V0,a,second)
    air_speed += 8*current
    print(f'Текущая скорость ракеты: {current_rocket_speed } м/с')
    current += 1

print("=========================")
print("-------------------------")
print("Взлет (Этап I/II) закончен! Данные:")
print("-------------------------")
print(f'Масса ракеты: {M_0} кг')
print(f'Скорость: {current_rocket_speed}')
print(f'Ускорение: {a_r}')
print(f'Сопротивление: {D}')
print("=========================")



# --- 2 Этап (Конфиг) ---
#Параметры ракеты ( ПОДСТАВИТЬ ЗНАЧЕНИЯ
F = 510000 #Тяга ракеты (Н)
g_0 = 9.81 # 
V0 = current_rocket_speed 
seconds = [0, 10, 15, 20, 25, 30]
air_speed = 2500 # м/с
# Запускаем симмуляцию взлета
po_massive = [0.05, 0.035, 0.025, 0.013, 0.0072, 0.0065]
current = 0
for second in seconds:
    M_0 = M_0 - delta_M
    #print(M_0)
    D = aerodynamic_resistance(po_massive[current], air_speed,Cd,A)
    a = acceleration_condtion_force(F,D,M_0)
    #print("a->",a,"D->",D)
    current_rocket_speed = velocity(V0,a,second)
    air_speed += 80*current
    print(f'Текущая скорость ракеты: {current_rocket_speed } м/с')
    current += 1

print("=========================")
print("-------------------------")
print("Взлет (Этап II/II) закончен! Данные:")
print("-------------------------")
print(f'Масса ракеты: {M_0} кг')
print(f'Скорость: {current_rocket_speed}')
print(f'Ускорение: {a}')
print(f'Сопротивление: {D}')
print("=========================")

print("-------------------------")
print("Симмуляция успешно завершена!")
print("-------------------------")




























"""
print(seconds )
rocket_speed = tsialkovsky_rocket_velocity(F, M_0, I_sp, g_0, t)
#rocket_speed_tested = delta_velocity(M_t, mass_rocket, I_sp, g_0)
specific_impulse_data = specific_impulse(F, mass_rocket, g_0)
seconds = [6, 7, 15, 19, 27, 29, 34, 35, 42]
t_p = burn_time(rocket_speed,M_0,F, I_sp,g_0)
if int(M_0*a_r) >= int(F - D - wheel_friction_force(M_0,g_0)):
    print('Условие разгона выполнено!')
print(f'DV: {rocket_speed } м/с')
print(f'Burn Time: {t_p}')
for second in seconds:
    M_0 = M_0 - delta_M
    current_rocket_speed = velocity(V0,a,second)
    print(f'Текущая скорость ракеты: {current_rocket_speed } м/с')
    
current_rocket_speed = velocity(V0,a,180)
print(f'Текущая скорость ракеты: {current_rocket_speed } м/с')

print(Конец! (Шутка(нет)))"""
