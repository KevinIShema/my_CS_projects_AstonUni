


# using breakpoints in the code to check if they are working as intended 

def div(x,y):
    breakpoint()
    z = x/y
    return z
def values():
    a = int(input("enter the first number: "))
    b =int(input("enter the seconf number: "))
    u = div(a,b)
    breakpoint()
    return u
k = values()
print("the result of division is :",round(k,2))