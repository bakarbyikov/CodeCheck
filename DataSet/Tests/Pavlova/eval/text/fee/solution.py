def f(x):
    x *= 1 - 0.12 - 0.01 - 0.01 + 0.45
    return round(x, 6)


print(f(float(input())))
