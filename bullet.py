import turtle
class Bullet(turtle.Turtle):
    def __init__(self):
        super().__init__()
        turtle.register_shape("missile.gif")
        self.shape("missile.gif")
        self.pu() #pin up
        self.goto(0,-240)
        self.speedamt=20
        self.state="Ready"


        