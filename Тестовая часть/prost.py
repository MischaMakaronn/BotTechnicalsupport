# Для того, чтобы определить,
# являются ли два числа взаимно простыми,
# нужно найти их наибольший общий делитель
# (НОД) и проверить, равен ли он единице
def equals(a, b):
    if a == 0 :
        return b
    elif b == 0 :
        return a
    else :
        return equals(b, a % b)

def nod(a, b) :
    if equals(a, b) == 1 :
        return True
    else :
        return False
a = int(input("Введите первое число: "))
b = int(input("Введите второе число: "))
if nod(a,b):
  print(f"Числа {a} и {b} взаимно простые.")
else:
  print(f"Числа {a} и {b} не взаимно простые.")