def fib(n, preval):
    if preval[n]:
        return preval[n]
    if n <= 2:
        result = 1
    else:
        result = fib(n-1, preval) + fib(n-2, preval)
    preval[n] = result
    return result

print(fib(99, [0] * 100))
