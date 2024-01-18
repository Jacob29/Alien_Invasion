import time

i = 1

for num in range(1,101):   
    if i % 3 == 0:
        if i % 5 == 0:
            print(f"{i} = FizzBuzz")
        else:  
            print(f"{i} = Fizz")
    elif i % 5 == 0:
        print(f"{i} = Buzz")
    else:
        print(f"{i}")
    i = i + 1
    time.sleep(0.1)