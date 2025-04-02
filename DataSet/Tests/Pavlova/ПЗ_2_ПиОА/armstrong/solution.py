def solve(x: str) -> bool:
    if len(x) != 3:
        return None
    sm: int = sum(int(i) ** 3 for i in x)
    return sm == int(x)

# x: str = input()
# result = solve(x)
# print(result)
for i in range(1000):
    if solve(str(i)):
        print(i)