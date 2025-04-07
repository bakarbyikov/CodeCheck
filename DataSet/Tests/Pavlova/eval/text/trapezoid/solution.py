from math import cos, radians, sin


def f(a, b, alpha):
    alpha_rad = radians(alpha)

    S = (a + b) * (a - b) * sin(alpha_rad) / (4 * cos(alpha_rad))
    return round(S, 6)


print(f(*map(float, input().split())))
