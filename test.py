def second_outer(*dargs, **dkwargs): 
    def outer(func):
        def inner(*args, **kwargs):
            attempts = dkwargs["attempts"]
            while attempts > 0:
                try:
                    return func(*args, **kwargs)
                except Exception as err:
                    print(f"Error: {err}")
                    attempts -= 1
        return inner
    return outer


@second_outer(attempts = 5)
def div(a, b):
    return a / b

print(div(1, 2))