#!/usr/bin/python3 -B

def example(func):
    def wrapper():
        print('Step1')
        func()
        print('Step2')
    return wrapper

@example
def what():
    print('what')

print('Now lets run the test')
what()
