def solve(x: str) -> bool:
    sm: int = min(map(int,x))
    return sm % 2 == 1

x: str = input()
result = solve(x)
print(result)

