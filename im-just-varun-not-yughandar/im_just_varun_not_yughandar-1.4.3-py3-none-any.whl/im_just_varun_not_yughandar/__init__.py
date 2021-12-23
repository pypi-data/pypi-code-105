from turtle import *
import turtle
from random import randint
import time


def create_rectangle(turtle, color, x, y, width, height):
    turtle.penup()
    turtle.color(color)
    turtle.fillcolor(color)
    turtle.goto(x, y)
    turtle.pendown()
    turtle.begin_fill()

    turtle.forward(width)
    turtle.left(90)
    turtle.forward(height)
    turtle.left(90)
    turtle.forward(width)
    turtle.left(90)
    turtle.forward(height)
    turtle.left(90)

    # fill the above shape
    turtle.end_fill()
    # Reset the orientation of the turtle
    turtle.setheading(0)

def create_circle(oogway, x, y, radius, color):
    oogway.penup()
    oogway.color(color)
    oogway.fillcolor(color)
    oogway.goto(x, y)
    oogway.pendown()
    oogway.begin_fill()
    oogway.circle(radius)
    oogway.end_fill()

def christ():

    BG_COLOR = "#0080ff"
    oogway = Turtle()
    oogway.speed(6)
    screen = oogway.getscreen()
    screen.bgcolor(BG_COLOR)
    screen.title("Merry Christmas")
    screen.setup(width=1.0, height=1.0)

    y = -100
    create_rectangle(oogway, "red", -15, y-60, 30, 60)

    width = 240
    oogway.speed(6)
    while width > 10:
        width = width - 10
        height = 10
        x = 0 - width/2
        create_rectangle(oogway, "green", x, y, width, height)
        y = y + height

    oogway.speed(6)
    oogway.penup()
    oogway.color('yellow')
    oogway.goto(-20, y+10)
    oogway.begin_fill()
    oogway.pendown()
    for i in range(5):
        oogway.forward(40)
        oogway.right(144)
    oogway.end_fill()

    tree_height = y + 40

    create_circle(oogway, 230, 180, 60, "white")
    create_circle(oogway, 220, 180, 60, BG_COLOR)

    oogway.speed(10)
    number_of_stars = randint(20,30)

    for _ in range(0,number_of_stars):
        x_star = randint(-(screen.window_width()//2),screen.window_width()//2)
        y_star = randint(tree_height, screen.window_height()//2)
        size = randint(5,20)
        oogway.penup()
        oogway.color('white')
        oogway.goto(x_star, y_star)
        oogway.begin_fill()
        oogway.pendown()
        for i in range(5):
            oogway.forward(size)
            oogway.right(144)
        oogway.end_fill()

    # print greeting message
    oogway.speed(1)
    oogway.penup()
    msg = "Merry Christmas to ALL"
    oogway.goto(0, -200) 
    oogway.color("white")
    oogway.pendown()
    oogway.write(msg, move=False, align="center", font=("Arial", 15, "bold"))
    oogway.hideturtle()
    time.sleep(4)
    
    turtle.bye()
    return 'Done'


#convesation
def santa_n_varun():
    
    screen= turtle.Screen()
    turtle.title('Santa vs Varun')
    screen.setup(width=1.0, height=1.0)
    screen.bgcolor('black')
    screen.tracer(0)
    tt = turtle.Turtle()
    
    my_col = ['red','purple','blue','green','orange','yellow']
    
    tt.color('blue')
    tt.hideturtle()
    tt.speed(10)
    tt.penup()
    
    #varunn
    tt.right(180)
    tt.forward(200)
    tt.right(90)
    tt.pendown()
    #tt.right(90)
    tt.forward(100)
    tt.right(90)
    tt.circle(30)
    tt.right(90)
    tt.forward(40) #head to hands
    tt.left(45)
    tt.forward(60)
    tt.backward(60)
    tt.right(90)
    tt.forward(60)
    tt.backward(60)
    tt.right(315)
    tt.forward(110) #hands to legs
    tt.left(45)
    tt.forward(60)
    tt.backward(60)
    tt.right(90)
    tt.forward(60)
    tt.backward(60)
    tt.penup()
    tt.goto(-180,-60)
    tt.pendown()
    tt.write('Varun')
    
    #santa
    tt2 = turtle.Turtle()
    tt2.color('red')
    tt2.hideturtle()
    tt2.speed(6)
    tt2.penup()
    
    #tt2.right(180)
    tt2.forward(200)
    tt2.left(90)
    tt2.pendown()
    #tt.right(90)
    tt2.forward(100)
    tt2.right(90)
    tt2.circle(30)
    tt2.right(90)
    tt2.forward(40) #head to hands
    tt2.left(45)
    tt2.forward(60)
    tt2.backward(60)
    tt2.right(90)
    tt2.forward(60)
    tt2.backward(60)
    tt2.right(315)
    tt2.forward(110) #hands to legs
    tt2.left(45)
    tt2.forward(60)
    tt2.backward(60)
    tt2.right(90)
    tt2.forward(60)
    tt2.backward(60)
    tt2.penup()
    tt2.goto(220,60)
    tt2.pendown()
    tt2.write('Santa')

    #conversation #santa
    tt3 = turtle.Turtle()
    tt3.color('green')
    tt3.hideturtle()
    tt3.speed(0)
    tt3.penup()
    tt3.goto(220,180)
    tt3.pendown()
    tt3.write('Hello Yugandharr')
    time.sleep(2)
    tt3.clear()

    #conversation #santa
    tt4 = turtle.Turtle()
    tt4.color('red')
    tt4.hideturtle()
    
    tt4.penup()
    tt4.goto(-220,180)
    tt4.pendown()
    tt4.write('OMG OMGG Santa is it real or am i dreaming')
    time.sleep(3)
    tt3.speed(6)
    tt4.speed(6)
    
    tt4.clear()
    tt3.write('Yes My child')
    time.sleep(3)
    tt3.clear()
    tt4.write('Thank god I have lot of items \n in my amazon and flipkart cart for you')
    time.sleep(4)
    tt4.clear()
    tt3.write('Dont Expect too much my dear yugandhar \n we too have budjet problems')
    time.sleep(4)
    tt3.clear()
    tt4.write('oho noooo , \n Firstly  santa please don"t call me as yugandhar \n just use VARUN')
    time.sleep(4)
    tt4.clear()
    tt3.write('Why my child')
    time.sleep(3)
    tt3.clear()
    tt4.write('Yughandhar is old santa \n Varun is in trending now,\n i think you dont understand these words')
    time.sleep(4)
    tt4.clear()    
    tt3.write('Its ok my child')
    time.sleep(3)
    tt3.clear()    
    tt4.write('Santa Its too boring now')
    time.sleep(3)
    tt4.clear()    
    tt3.write('Please dont ask any girls contacts my child')
    time.sleep(3)
    tt3.clear()
    tt4.write('uff.....')
    time.sleep(3)
    tt4.clear()
    tt3.write('Shall we play a game varun')
    time.sleep(3)
    tt3.clear()
    tt4.write('huhuu im too excited santa lets start')
    time.sleep(3)
    tt4.clear()
    tt3.write('But you need to tell truth only , this game is like truth or dare')
    time.sleep(4)
    tt3.clear()
    tt4.write('haha santa i think you dont know that Varun only tells TRUTH')
    time.sleep(4)
    tt4.clear()
    tt3.write('What is your opinion about SAHAS')
    time.sleep(3)
    tt3.clear()
    tt4.write('hmmm... Have u watched Bahubali santa')
    time.sleep(3)
    tt4.clear()
    tt3.write('Yes My dear')
    time.sleep(3)
    tt3.clear()
    tt4.write('Have u remember KATTAPPA Character')
    time.sleep(2)
    tt4.clear()
    tt3.write('Yes....')
    time.sleep(2)
    tt3.clear()
    tt4.write('Sahas Replicates KATTAPA ,\n He always says he will help \n but at last i think u know that')
    time.sleep(4)
    tt4.clear()

    tt3.write('Hohooo  What about SAINATH')
    time.sleep(2.5)
    tt3.clear()
    tt4.write('Whenever i think about sainath \n my mind says he was like \n chota sahas')
    time.sleep(4)
    tt4.clear()

    tt3.write('OMG...!!,  What about SAI PRASAD my child')
    time.sleep(4)
    tt3.clear()
    tt4.write('If i convert like MONK \n then the main reason was SAI, \n Sometimes I"m really scared about that')
    time.sleep(4)
    tt4.clear()

    tt3.write('Im sry dear...!!,  What do you think about Vineetha')
    time.sleep(3)
    tt3.clear()
    tt4.write('He is like one type of psycho')
    time.sleep(3)
    tt4.clear()

    tt3.write('hohoo  Why are you pronouncing with "HE"')
    time.sleep(3)
    tt3.clear()
    tt4.write('i too have serious doubts on that')
    time.sleep(3)
    tt4.clear()


    #Vinnetha
    tt5 = turtle.Turtle()
    tt5.color('Yellow')
    tt5.hideturtle()
    tt5.speed(6)
    tt5.penup()
    
    #tt2.right(180)
    tt5.forward(0)
    tt5.left(90)
    tt5.pendown()
    #tt.right(90)
    tt5.forward(100)
    tt5.right(90)
    tt5.circle(30)
    tt5.right(90)
    tt5.forward(40) #head to hands
    tt5.left(45)
    tt5.forward(60)
    tt5.backward(60)
    tt5.right(90)
    tt5.forward(60)
    tt5.backward(60)
    tt5.right(315)
    tt5.forward(110) #hands to legs
    tt5.left(45)
    tt5.forward(60)
    tt5.backward(60)
    tt5.right(90)
    tt5.forward(60)
    tt5.backward(60)
    tt5.penup()
    tt5.goto(0,60)
    tt5.pendown()
    tt5.write('Vineetha')

    tt6 = turtle.Turtle()
    tt6.color('yellow')
    tt6.hideturtle()
    
    tt6.penup()
    tt6.goto(0,180)
    tt6.pendown()
    tt6.write('Em matladutunnav Yughandar')
    time.sleep(3)
    tt6.clear()

    tt4.write('Ayyo sorry akka nuv ekkade vunnav ani teleeka \n Nijam cheppesaa')
    time.sleep(3)
    tt4.clear()

    tt6.write('Nee yenkamma , Cheptha cheptha naku time vasthadi Yughandhar')
    time.sleep(4)
    tt6.clear()

    tt4.write('sorry akka')
    time.sleep(3)
    tt4.clear()
    tt5.clear()

    tt3.write('Ok varun I need to GO,\n will meet you again, \n Always Keep this smile like this \n (i Hope you are smiling now)')
    time.sleep(4)
    tt3.clear()

    tt4.write('Ok santa Bye')
    time.sleep(3)
    tt4.clear()
    tt.clear()
    tt2.clear()
    print('successfullyy')
    turtle.bye()
    return 'Done'


#last mer
import turtle
import random


def abcdef():
        screen= turtle.Screen()
        turtle.title('name')
        screen.setup(width=1.0, height=1.0)
        screen.bgcolor('black')
        screen.tracer(0)

        tt = turtle.Turtle()
        tt.hideturtle()

        colors_pen = ['green', 'white', 'blue', 'yellow', 'pink', 'purple', 'violet', 'gray']
        colors_fill = ['green', 'blue', 'white', 'yellow', 'pink','purple', 'violet', 'gray']
        tt.speed('fastest')

        def gg():
            for i in range (16):
                x, y = random.randrange (-350, 350), random.randrange (-230,230)
                ttl= turtle.Turtle () # create a new pen
                ttl.color(random.choice (colors_pen))
                #x= '\U0001f600'
                name = 'Marry Christmas \n Varun'
                ttl.write(name,font=('chiller',95, 'italic bold'), align="center")
                #ttl.penup() # up the pen
                #tt1.goto(15,60)
                #tt1.pendown()
                #ttl.write('Marry Christmas \n marry christmas',font=('chiller',60, 'italic bold'))
                ttl.clear()
                tt.penup() # up the pen
                tt.goto(x,y) # 
                tt.pendown() #down the pen
                tt.begin_fill() # ar
                tt.color(random.choice (colors_fill))
                for i in range(6): 
                    tt.forward(36)
                    tt.right(144)
                tt.end_fill() # 

        for _ in range(10): 
            gg()
            tt.clear() # clear the tt pen (stars)

        
            

        tt.clear()
        turtle.bye()
        return 'Done'
        #conversation.santa_n_varun()
        #turtle.mainloop()



def im_varun_only():
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
            print(space + 'Happy Christmas...!!ðŸŽ‚')

        elif(i%9==0):
            print(space + 'â›„')

        elif(i%9==0):
            print(space + 'Stay Blessed..â›„')


        elif(i%5==0):
            print(space + 'Marry Christmas....ðŸ¥³')


        elif(i%8==0):
            print(space + 'âœ¨')      


        elif(i%7==0):
            print(space + 'ðŸŽ‰')


        elif(i%6==0):
            print(space + 'huhuu its XmasðŸŽ„')

        else:
            print(space + 'ðŸŽŠ')

        space = ''
        time.sleep(0.2)
    my_col = ['red','purple','blue','green','orange','yellow']
    
    xmastree =christ()
    conv = santa_n_varun()
    abc = abcdef()






