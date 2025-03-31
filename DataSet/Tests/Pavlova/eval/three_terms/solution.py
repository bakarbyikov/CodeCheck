from math import cos, sin, sqrt


def solve(x, t):
    if sin(t) == 0:
        return None
    left = (1 + x**2 - 2*x*t) / sin(t) + 1
    right = sqrt(1 + sin(x)**2 + cos(x*t)**2)
    return left + right


x, t = map(float, input().split())
res = solve(x, t)
print(res and f"{res:.6f}")