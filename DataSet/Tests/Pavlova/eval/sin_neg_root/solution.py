from math import copysign, sin


def solve(x):
    if x == 0:
        return None
    root = copysign(abs(x) ** (1/3), x)
    return abs(sin((1 + root) / x))


res = solve(float(input()))
print(res and f"{res:.6f}")