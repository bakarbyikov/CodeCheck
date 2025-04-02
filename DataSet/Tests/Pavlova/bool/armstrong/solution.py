def solve(x: str) -> bool:
    sm: int = sum(int(i) ** 3 for i in x)
    return sm == int(x)

x: str = input()
result = solve(x)
print(result)