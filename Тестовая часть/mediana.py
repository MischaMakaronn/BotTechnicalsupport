# Если количество элементов в списке четное,
# медианой считается среднее значение двух центральных элементов,
# если нечетное - центральный элемент
import statistics
from random import randint, randrange
numbers = []
for i in range(20):
    numbers.append(randint(-9999, 9999))

print("Список случайных чисел:", numbers )
print("Медиана списка равна:", statistics.median(numbers))