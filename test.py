for num in range(1,101):
    string = ""
    if num % 3 == 0:
        string = string + "Fizz"
    if num % 4 == 0:
        string = string + "Buzz"
    if num % 4 != 0 and num % 3 != 0:
        string = string + str(num)
    print(string)