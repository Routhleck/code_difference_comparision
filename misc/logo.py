import turtle as t
import random
import math
from alphabet import alphabet

def displayMessage(message, fontSize ,color ,x ,y ,t ,charSpace):
    t.color(color)
    message=message.upper()
  
    for character in message:
        if character in alphabet:
            letter=alphabet[character]
            t.penup()
            for dot in letter:
                t.goto(x + dot[0]*fontSize, y + dot[1]*fontSize)
                t.pendown()
        # character 'I' takes up less space
        if character == 'I':
            x += fontSize / 2
        else: 
            x += fontSize

def background(turtle):
    # sidelength and diameter
    l = 500
    d =  math.sqrt(l * l - 2 * l * l * math.cos(math.radians(89)) + l * l)

    turtle.penup()
    turtle.setpos(0, d/2)
    turtle.pendown()
    # print circle
    turtle.color('gray')
    turtle.begin_fill()
    turtle.circle(-d/2)
    turtle.end_fill()

    turtle.right(45.5)
  # print pattern
    for i in range(0,91):
        if i % 2 == 0:
            turtle.pencolor('red')
        else:
            turtle.pencolor('black')

        turtle.forward(l)
        turtle.right(91)
    

def logo():
    t.pensize(2)
    t.speed(speed=0)
    background(t)

    t.pensize(9)
    charSpace = 5
    fontSize = 58
    displayMessage("PYGIATOR", fontSize, 'red', -230, -(fontSize/2), t, charSpace)

    ## The following code snippet can be used to save the logo 
    # ts = t.getscreen()
    # ts.getcanvas().postscript(file="./misc/logo.svg")

    t.Screen().exitonclick()

logo()