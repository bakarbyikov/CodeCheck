def solve(x: str) -> bool:
    if len(x) != 3 or int(x) < 0:
        return None
    sm: int = sum(int(i) ** 3 for i in x)
    return sm == int(x)

x: str = input()
result = solve(x)
print(result)