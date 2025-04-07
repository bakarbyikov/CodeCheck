from math import acos, degrees

def f(a, b, c):
    A = acos((b**2 + c**2 - a**2) / (2 * b * c))
    B = acos((a**2 + c**2 - b**2) / (2 * a * c))
    C = acos((a**2 + b**2 - c**2) / (2 * a * b))
    
    return [round(degrees(i), 6) for i in (A, B, C)]

print(*f(*map(float, input().split())))
