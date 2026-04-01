#player class that has the moving functions
import turtle

class Player(turtle.Turtle):
    def __init__(self):
        super().__init__()
        turtle.register_shape("player.gif")
        self.color("blue")
        self.speed(0)
        self.shape("player.gif")
        self.pu()
        self.goto(0,-250)

        #moving
        self.playerspeed = 40

    def move_Left(self):
        x = self.xcor()
        x -= self.playerspeed 
        if x < -450:
            x = -450 #keeps it within the window
        self.setx(x) #moves the turtle

    def move_Right(self):
        x = self.xcor()
        x += self.playerspeed
        if x > 450:
            x = 450 #keeps it within the window
        self.setx(x)