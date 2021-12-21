from tkinter import *
expression = ''
def GUI_MathCalculator():

 def press(num):
    global expression
    expression = expression + str(num)
    equation.set(expression)

 def equalPress():
     try:
         global expression
         total = str(eval(expression))
         equation.set(total)
         expression = ''

     except:
         equation.set('error')
         expression = ''

 def clear():
     global expression
     expression = ''
     equation.set('')

 if __name__=='__main__':
     gui = Tk()
     gui.configure(background = 'light grey')
     gui.title('Math Calculator')
     gui.geometry('399x169')
     equation = StringVar()
     expression_field = Entry(gui, textvariable = equation)
     expression_field.grid(columnspan = 4, ipadx = 70)

     button1 = Button(gui, text = '1', fg = 'black', bg = 'white',
                 command = lambda: press(1), height = 1, width = 7)
     button1.grid(row = 2, column = 0)

     button2 = Button(gui, text = '2', fg = 'black', bg = 'white',
                 command = lambda: press(2), height = 1, width = 7)
     button2.grid(row = 2, column = 1)

     button3 = Button(gui, text = '3', fg = 'black', bg = 'white',
                 command = lambda: press(3), height = 1, width = 7)
     button3.grid(row = 2, column = 2)

     button4 = Button(gui, text = '4', fg = 'black', bg = 'white',
                 command = lambda: press(4), height = 1, width = 7)
     button4.grid(row = 3, column = 0)

     button5 = Button(gui, text = '5', fg = 'black', bg = 'white',
                 command = lambda: press(5), height = 1, width = 7)
     button5.grid(row = 3, column = 1)

     button6 = Button(gui, text = '6', fg = 'black', bg = 'white',
                 command = lambda: press(6), height = 1, width = 7)
     button6.grid(row = 3, column = 2)

     button7 = Button(gui, text = '7', fg = 'black', bg = 'white',
                 command = lambda: press(7), height = 1, width = 7)
     button7.grid(row = 4, column = 0)

     button8 = Button(gui, text = '8', fg = 'black', bg = 'white',
                 command = lambda: press(8), height = 1, width = 7)
     button8.grid(row = 4, column = 1)

     button9 = Button(gui, text = '9', fg = 'black', bg = 'white',
                 command = lambda: press(9), height = 1, width = 7)
     button9.grid(row = 4, column = 2)

     button0 = Button(gui, text = '0', fg = 'black', bg = 'white',
                 command = lambda: press(0), height = 1, width = 7)
     button0.grid(row = 5, column = 0)

     plus = Button(gui, text = '+', fg = 'black', bg = 'white',
                  command = lambda: press('+'), height = 1, width = 7)
     plus.grid(row = 2, column =3)

     minus = Button(gui, text = '-', fg = 'black', bg = 'white',
                  command = lambda: press('-'), height = 1, width = 7)
     minus.grid(row = 3, column =3)
    
     multiply = Button(gui, text = '✕', fg = 'black', bg = 'white',
                  command = lambda: press('*'), height = 1, width = 7)
     multiply.grid(row = 4, column =3)

     divide = Button(gui, text = '÷', fg = 'black', bg = 'white',
                  command = lambda: press('/'), height = 1, width = 7)
     divide.grid(row = 5, column = 3)

     modulus = Button(gui, text = '|✕|', fg = 'black', bg = 'white',
                  command = lambda: press('%'), height = 1, width = 7)
     modulus.grid(row = 6, column = 1)

     exponent = Button(gui, text = 'xª', fg = 'black', bg = 'white',
                      command = lambda: press('**'), height = 1, width = 7 )
     exponent.grid(row = 6, column = 2)

     floor_divide = Button(gui, text = '⌊ ⌋', fg = 'black', bg = 'white',
                          command = lambda: press('//'), height = 1, width = 7 )
     floor_divide.grid(row = 6, column = 3)

     equal = Button(gui, text = '=', fg = 'black', bg = 'white',
                   command = equalPress, height = 1, width = 7 )
     equal.grid(row = 5, column = 2)

     clear = Button(gui, text = 'AC', fg = 'black', bg = 'white',
                   command = clear, height = 1, width = 7 )
     clear.grid(row = 5, column = '1')

     decimal = Button(gui, text = '.', fg = 'black', bg = 'white',
                     command = lambda: press('.'), height = 1, width = 7)
     decimal.grid(row = 6, column = 0)

     gui.mainloop()

def reset_No(c): 
     b = float(input('Type your second number__'))
     operator = input('Type your operator__')
     if(operator == '+'):
        c = c + b
        print(c)
     if(operator == '-'):
        c = c - b
        print(c)
     if(operator == 'x' or operator == 'X'):
        c = c * b
        print(c)
     if(operator == '/'):
        c = c / b
        print(c)
     if(operator == '*'):
        c = c ** b
        print(c)
     if(operator == '//'):
        c = c // b
        print(c)
     if(operator == '%'):
        c = c % b
        print(c)
     contin = input('quit?__')
     if(contin == 'yes'):
        print('quitting...')
        exit()
     elif(contin == 'no'):
       reset = input('Reset calculator?__')
     if reset == 'yes':
        reset_Yes()
     if reset == 'no':
        reset_No(c) 

def reset_Yes():
     print('resetting...')
     a = float(input('Type your first number__'))
     b = float(input('Type your second number__'))
     operator = input('Type your operator__')
     if(operator == '+'):
        c = a + b
        print(c)
     if(operator == '-'):
        c = a - b
        print(c)
     if(operator == 'x' or operator == 'X'):
        c = a * b
        print(c)
     if(operator == '/'):
        c = a / b
        print(c)
     if(operator == '*'):
        c = a ** b
        print(c)
     if(operator == '//'):
        c = a // b
        print(c)
     if(operator == '%'):
        c = a % b
        print(c)

     contin = input('quit?__')
     if(contin == 'yes'):
        print('quitting...')
        exit()
     elif(contin == 'no'):
        reset = input('Reset calculator?__')
     if reset == 'yes':
        reset_Yes()
     if reset == 'no':
        reset_No(c) 

def Text_MathCalculator():
 a = float(input('Type your first number__'))
 b = float(input('Type your second number__'))
 operator = input('Type your operator__')
 if(operator == '+'):
     c = a + b
     print(c)
 if(operator == '-'):
     c = a - b
     print(c)
 if(operator == 'x' or operator == 'X'):
     c = a * b
     print(c)
 if(operator == '/'):
     c = a / b
     print(c)
 if(operator == '*'):
     c = a ** b
     print(c)
 if(operator == '//'):
     c = a // b
     print(c)
 if(operator == '%'):
     c = a % b
     print(c)
 contin = input('quit?__')
 if(contin == 'yes'):
      print('quitting...')
      exit()
 elif(contin == 'no'):
        reset = input('Reset calculator?__')
        if reset == 'yes':
           reset_Yes()
        if reset == 'no':
           reset_No(c)
print('Hello! This is a Math Calculator:')
gui = input('Do you want a Graphical User Interaface(GUI) or Text Based User Interface?__ ')
if(gui == 'GUI'):
   print('Starting Graphical User Interface...')
   GUI_MathCalculator()
elif(gui == 'TUI'):
   print('Starting Text Based User Interface...')
   Text_MathCalculator()
else:
   print('Unrecognized Entry, Starting Text Based User Interface...')
   Text_MathCalculator()
