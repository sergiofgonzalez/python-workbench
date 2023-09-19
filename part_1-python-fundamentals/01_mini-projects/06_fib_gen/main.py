def fib():
    yield 0
    aux_0 = 0
    aux_1 = 1
    while True:
        yield aux_1 + aux_0
        aux_0, aux_1 = aux_1, aux_0 + aux_1


for n in fib():
    if n > 100:
        break
    print(n)
