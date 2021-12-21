def obtenerPrimos(x):
    for numero in range(2,x + 1):
        primo = True
        for i in range(2,numero):
            if (numero % i == 0):
                primo = False
        if primo:
            print (numero)
    return True




       

