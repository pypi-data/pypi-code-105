import re,math
regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'

def is_validEmail(email):
    #Comparing Email with the regex
    if re.fullmatch(regex, email):
        return True
    else:
        return False 


def quadRoots(x2coeff,xcoeff,constant):
    if(x2coeff!=0):
        #Calculating the Discriminant
        discriminant = (xcoeff**2)-(4*x2coeff*constant)
        
        #Calculating the Square root , mkaing it easier to use in future
        sqrt_val = math.sqrt(abs(discriminant)) 

        #if Discriminant is greater than 0 ( roots are Real and Unequal)
        if discriminant > 0: 
            root1 = (-xcoeff+sqrt_val)/(2 * x2coeff)
            root2 = (-xcoeff-sqrt_val)/(2 * x2coeff)
            return root1,root2 

        #if Discriminant is equal 0 ( roots are Real and equal)
        elif discriminant == 0: 
            root1 = root2 = -xcoeff/(2 * x2coeff)
            return root1,root2

        #if Discriminant is less than 0 ( roots are imaginary)
        else:
            root1 = str(-xcoeff/(2 * x2coeff))+" + i"+str(sqrt_val) 
            root2 = str(-xcoeff/(2 * x2coeff))+" - i"+str(sqrt_val) 
        return root1,root2
    else:
        raise Exception("Invalid Roots")


#Normal Half Pyramids

def halfPyramid(rows,character=None,iteration=None):
    for i in range(1,rows+1):
        for j in range(1,i+1):

            #To display the Numbers without frequent iteration
            if character is None:
                print(j,end=" ")

            #To display the characters without frequent iteration
            elif (iteration=="Entire"):
                ascii_value = ord(character)
                print(character,end=" ")
                character = chr(ascii_value+1)

            #To display the characters with frequent iteration
            elif (iteration=="Half"):
                ascii_value = ord(character)
                print(character,end=" ")

            #To display Unique character or Numbers(as char)
            else:
                print(character,end=" ")

        if (iteration=="Half"):
            character = chr(ascii_value+1)
        print("\n")

    
def reverseHalfPyramid(rows,character=None,iteration=None):
    for i in range(rows,0,-1):
        for j in range(rows,i-1,-1):
            #To display the Numbers without frequent iteration
            if character is None:
                print(j,end=" ")

            #To display the characters without frequent iteration
            elif (iteration=="Entire"):
                ascii_value = ord(character)
                print(character,end=" ")
                character = chr(ascii_value-1)

            #To display the characters with frequent iteration
            elif (iteration=="Half"):
                ascii_value = ord(character)
                print(character,end=" ")

        if (iteration=="Half"):
            character = chr(ascii_value-1)
        print("\n")



#Inverted Half Pyramids
def invertedHalfPyramid(rows,character=None,iteration=None):
    for i in range(rows,0,-1):
        for j in range(1,i+1):

            #To display the Numbers without frequent iteration
            if character is None:
                print(j,end=" ")

            #To display the characters without frequent iteration
            elif (iteration=="Entire"):
                ascii_value = ord(character)
                print(character,end=" ")
                character = chr(ascii_value+1)

            #To display the characters with frequent iteration
            elif (iteration=="Half"):
                ascii_value = ord(character)
                print(character,end=" ")

            #To display Unique character or Numbers(as char)
            else:
                print(character,end=" ")

        if (iteration=="Half"):
            character = chr(ascii_value+1)
        print("\n")

    
def invertedReverseHalfPyramid(rows,character=None,iteration=None):
    for i in range(1,rows+1):
        for j in range(rows,i-1,-1):
            #To display the Numbers without frequent iteration
            if character is None:
                print(j,end=" ")

            #To display the characters without frequent iteration
            elif (iteration=="Entire"):
                ascii_value = ord(character)
                print(character,end=" ")
                character = chr(ascii_value-1)

            #To display the characters with frequent iteration
            elif (iteration=="Half"):
                ascii_value = ord(character)
                print(character,end=" ")

        if (iteration=="Half"):
            character = chr(ascii_value-1)
        print("\n")

#Full Pyramid
def fullPyramid(rows,character=None):
    k = count= count1=0
    for i in range(1, rows+1):
        for space in range(1,(rows-i)+1):
            print(end="  ")
            count+=1

        while k!=((2*i)-1):
            #To display the character
            if character is not None:
                print(character, end=" ")
                k += 1
            else:
                #To display the Numbers
                if count<=rows-1:
                    print(i+k, end=" ")
                    count+=1
                else:
                    count1+=1
                    print(i+k-(2*count1), end=" ")
                k += 1
        count1 = count = k = 0
        print()


#Inverted Full Pyramid
def InvertedfullPyramid(rows,character=None):
    k = count= count1=0
    for i in range(rows,0,-1):
        for space in range(1,(rows-i)+1):
            print(end="  ")
            count+=1

        while k!=((2*i)-1):
            #To display the character
            if character is not None:
                print(character, end=" ")
                k += 1
            else:
                #To display the Numbers
                if count<=rows-1:
                    print(i+k, end=" ")
                    count+=1
                else:
                    count1+=1
                    print(i+k-(2*count1), end=" ")
                k += 1
        count1 = count = k = 0
        print()


#Pascal Triangle
def pascalTrinagle(rows,inverted=False):
    coef = 1
    if inverted is False:
        start = step = 1
        end = rows + 1
    else:
        start = rows 
        step = -1 
        end = 0

    for i in range(start,end,step):
        for space in range(1, rows-i+1):
            print(end=" ")
        for j in range(0, i):
            if j==0 or i==0:
                coef = 1
            else:
                coef = coef * (i - j)//j
            print(coef, end = " ")
        print()



#Floyd Triangle
def floydTriangle(rows):
    iter_value = 1
    for i in range(1,rows+1):
        for j in range(1,i+1):
            print(iter_value,end=" ")
            iter_value += 1
        print("\n")


print(quadRoots(1,1,1))

