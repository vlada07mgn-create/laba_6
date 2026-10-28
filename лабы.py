import numpy as np
#  Исходные данные
A = np.array([
    [4.003, 0.207, 0.519, 0.281],
    [0.416, 3.273, 0.326, 0.375],
    [0.297, 0.351, 2.997, 0.429],
    [0.412, 0.194, 0.215, 3.628]
])
B = np.array([0.425, 0.021, 0.213, 0.946])
eps = 0.001  # Заданная точность
n = len(B)
#  Приведение к итерационному виду (x = alpha * x + beta)
alpha = np.zeros((n, n))
beta = np.zeros(n)
for i in range(n):
    for j in range(n):
        if i != j:
            alpha[i][j] = -A[i][j] / A[i][i]
    beta[i] = B[i] / A[i][i]
#  Итерационный процесс
x_old = np.zeros(n)  # Начальное приближение
x_new = beta.copy()
print(f"{'Итерация':<10} | {'x1':<8} | {'x2':<8} | {'x3':<8} | {'x4':<8} | {'Погрешность'}")
print("-" * 70)
iteration = 0
while True:
    iteration += 1
    # Вычисление новых значений
    x_new = np.dot(alpha, x_old) + beta
    # Вычисление максимальной разности
    error = np.max(np.abs(x_new - x_old))
    # Вывод текущей итерации
    print(f"{iteration:<10} | {x_new[0]:.4f}   | {x_new[1]:.4f}   | {x_new[2]:.4f}   | {x_new[3]:.4f}   | {error:.4f}")
    # Проверка условия остановки
    if error < eps:
        break
    x_old = x_new.copy()
print("-" * 70)
print("\nРезультат (при eps = 0,001):")
print(f"x1 = {x_new[0]:.4f}")
print(f"x2 = {x_new[1]:.4f}")
print(f"x3 = {x_new[2]:.4f}")
print(f"x4 = {x_new[3]:.4f}")