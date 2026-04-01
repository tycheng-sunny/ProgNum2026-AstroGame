import turtle, random

class Enemy(turtle.Turtle):
    def __init__(self):
        super().__init__()
        turtle.register_shape("enemy.gif")
        self.color("red")
        self.shape("enemy.gif")
        self.pu()

        x = random.randint(-450,450) 
        y = random.randint(180,250)
        self.goto(x,y)
        self.speedamt=1
        
