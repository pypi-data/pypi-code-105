## Funcion para calcular los numeros primos entre 1 y n
## Comprueba si un numero es primo:
def es_primo(n):
    if n < 2:
        return False
    if n == 2:
        return True
    for i in range(2,n):
        if n%i ==0:
         return False
    return True


# Devuelve la secuencia de numeros primos entre 1 y n
def secuencia_primos(n): 
    for k in range(1,n+1):
        if es_primo(k)== True:
            print (f'{k} es primo')
