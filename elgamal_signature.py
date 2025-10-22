import random
import math
from itertools import count


def digit_sum(n):   #хеш: сумма цифр числа
    return sum(int(d) for d in str(n))

def mod_inverse(a, m):  #обратный элемент по модулю m
    if math.gcd(a, m) != 1:
        raise ValueError(f"обратный не существует: НОД({a}, {m}) != 1")
    return pow(a, -1, m)

def factor_phi(phi):    #разложение на простые множители
    factors = set()
    while phi % 2 == 0:
        factors.add(2)
        phi //= 2
    for i in range(3, int(phi**0.5) + 1, 2):
        while phi % i == 0:
            factors.add(i)
            phi //= i
    if phi > 1:
        factors.add(phi)
    return factors

def is_primitive_root(g, p):    #является ли примитивным корнем
    phi = p - 1
    primes = factor_phi(phi)
    return all(pow(g, phi // q, p) != 1 for q in primes)

def find_primitive_root(p):     #поиск примитивного корня
    for g in count(2):
        if g >= p:
            raise ValueError("примитивный корень не найден")
        if is_primitive_root(g, p):
            return g

#генерация ключей

p = 107  #простое число
print(f"p = {p}")

g = find_primitive_root(p)  #примитивный корень
print(f"g = {g}")

x = random.randint(2, p - 2)    #секретный ключ
y = pow(g, x, p)    #открытый ключ 
print(f"секретный ключ x = {x}")
print(f"открытый ключ y = {y}")
print(f"публичные параметры: y={y}, g={g}, p={p}\n")

#сообщения

M1 = 12345
M2 = 67890

m1 = digit_sum(M1)
m2 = digit_sum(M2)

print(f"сообщение 1: M = {M1}, хеш m = {m1}")
print(f"сообщение 2: M = {M2}, хеш m = {m2}")

#подпись

phi = p - 1

#выбираем k
def random_prime(phi):
    while True:
        k = random.randint(2, phi - 1)
        if math.gcd(k, phi) == 1:
            return k

k1 = random_prime(phi)
k2 = random_prime(phi)

print(f"\nсекретные k: k1 = {k1}, k2 = {k2}")

r1 = pow(g, k1, p)
r2 = pow(g, k2, p)


s1 = ((m1 - x * r1) % phi * mod_inverse(k1, phi)) % phi
s2 = ((m2 - x * r2) % phi * mod_inverse(k2, phi)) % phi

print(f"\nподписи:")
print(f"M1: (r1={r1}, s1={s1})")
print(f"M2: (r2={r2}, s2={s2})")

#передача(с ошибкой)

received_M1 = M1
received_M2 = 67891  #повреждено

print(f"\nполучено:")
print(f"M1 = {received_M1}, подпись ({r1}, {s1})")
print(f"M2 = {received_M2}, подпись ({r2}, {s2})")

#проверка(получатель)

def verify(M, r, s, y, g, p):
    m = digit_sum(M)
    left = (pow(y, r, p) * pow(r, s, p)) % p
    right = pow(g, m, p)
    return left == right, left, right, m

print("\n")
print("проверка подписей")

valid1, l1, r1v, m1v = verify(received_M1, r1, s1, y, g, p)
print(f"сообщение 1: M = {received_M1}, m = {m1v}")
print(f"y^r * r^s = {l1} (mod {p})")
print(f"g^m = {r1v} (mod {p})")
print(f"подпись {'верна' if valid1 else 'неверна'}")

valid2, l2, r2v, m2v = verify(received_M2, r2, s2, y, g, p)
print(f"\nсообщение 2: M = {received_M2}, m = {m2v}")
print(f"y^r * r^s = {l2} (mod {p})")
print(f"g^m = {r2v} (mod {p})")
print(f"подпись {'верна' if valid2 else 'неверна'}")

print("\nвывод: повреждение второго сообщения обнаружено")