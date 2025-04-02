def solve(x: str) -> bool:
    sm = sum(int(i) % 2 for i in x)
    return 0 < sm < 4

x: str = input()
result = solve(x)
print(result)

