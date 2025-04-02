def solve(x: str) -> bool:
    if len(x) != 5 or int(x) < 0:
        return None
    sm: int = sum((int(i)+1)%2  for i in x)
    return sm > 0

x: str = input()
result = solve(x)
print(result)

