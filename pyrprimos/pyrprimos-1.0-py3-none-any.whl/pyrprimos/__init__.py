"""Programa en Python y R para el calculo de número primos hasta un numero dado
    by: Torres Espinosa, Jose Antonio"""

from rpy2.robjects import r

#Comentado para correr como funcion, sin comentar correria como programa
"""print("Se calcularan los numeros primos entre 1 y n")
#Se pide el valor de n al usuario y se pasa dicho valor a R
n = int(input("Introduce el valor de n: "))
print("Los numeros primos entre 1 y " + n + "son: ")"""

def primenumbers(n):
    r.assign('n',n)
    #Tras conocer el rango se calulan los primos en R
    r('''
        #Al dividir entre uno el modulo siempre es 0 por lo que se imprime antes de la funcion de calculo
        print(1)
        #Recorre el resto de numeros i hasta n
        for (i in 2:n){
            aux <- 2
            #While buscara los divisores de i
            #Cuando el valor de aux sea igual a i el bucle acabara, o cuando encuentre otro divisor
            while((i%%aux) != 0){
                aux <<- aux + 1
            }
            #Si el bucle acaba cuando i==aux, i es primo pues no podia dividirlo otro numero
            if(i == aux){
                print(i)
            }
        }
    ''')