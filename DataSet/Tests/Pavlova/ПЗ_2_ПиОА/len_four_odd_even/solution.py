def solve(x: str) -> bool:
    if len(x) != 4 or int(x) < 0:
        return None
    sm = sum(int(i) % 2 for i in x)
    return 0 < sm < 4

x: str = input()
result = solve(x)
print(result)

