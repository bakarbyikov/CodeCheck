def solve(x: str) -> bool:
    if len(x) != 4 or int(x) < 0:
        return None
    even: bool = any(int(i) % 2 == 0 for i in x)
    odd: bool = any(int(i) % 2 for i in x)   
    return even and odd

x: str = input()
result = solve(x)
print(result)

