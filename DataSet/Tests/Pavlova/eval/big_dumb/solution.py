from math import cos, sin, sqrt


def f(x, t):
    top = sqrt(1 + x**2) - 2*x*t

    inner = sqrt(1 + sin(x)**2 + 0.3 * cos(x*t)**2)
    bottom = sqrt(1 + inner)

    if bottom == 0:
        return None

    return round(top/bottom, 6)


x, t = map(float, input().split())
print(f(x, t))
