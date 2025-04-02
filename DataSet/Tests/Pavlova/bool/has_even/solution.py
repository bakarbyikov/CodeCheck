def solve(x: str) -> bool:
    sm: int = sum((int(i)+1)%2  for i in x)
    return sm > 0

x: str = input()
result = solve(x)
print(result)

