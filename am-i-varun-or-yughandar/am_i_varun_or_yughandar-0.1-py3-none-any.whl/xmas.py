import time
from random import randint,randrange,choice



for i in range(1,85):
    print('')

space = ''

for i in range(1,80):
    count= randint(1,100)
    while(count > 0):
        space += ' '
        count -=1

    if(i%10==0):
        print(space + 'Happy Christmas...!!🎂')

    elif(i%9==0):
        print(space + '⛄')

    elif(i%9==0):
        print(space + 'Stay Blessed..⛄')


    elif(i%5==0):
        print(space + 'Marry Christmas....🥳')


    elif(i%8==0):
        print(space + '✨')      


    elif(i%7==0):
        print(space + '🎉')


    elif(i%6==0):
        print(space + 'huhuu its Xmas🎄')

    else:
        print(space + '🎊')

    space = ''
    time.sleep(0.2)
my_col = ['red','purple','blue','green','orange','yellow']
'''
import turtle
screen= turtle.Screen()
turtle.title('Its me Varun')
screen.setup(width=1.0, height=1.0)
screen.bgcolor('black')
screen.tracer(0)
t= turtle.Turtle()
t.hideturtle()
t.speed(0)


for x in range(180):
    t.pencolor(my_col[x%6])
    t.width(x//100+1)
    t.forward(x)
    t.left(59)
t.clear()
'''
#turtle.bye()

import xmas_turtle
import christmas
import conversation
xmastree = christmas.christ()
conv = conversation.santa_n_varun()
abc = xmas_turtle.abcdef()


