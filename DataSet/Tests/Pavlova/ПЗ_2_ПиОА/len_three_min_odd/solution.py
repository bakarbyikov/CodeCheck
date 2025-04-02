def solve(x: str) -> bool:
    if len(x) != 3 or int(x) < 0:
        return None
    sm: int = min(map(int,x))
    return sm % 2 == 1

x: str = input()
result = solve(x)
print(result)

