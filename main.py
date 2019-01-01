import kivy
kivy.require('1.10.0')

from kivy.app import App
from kivy.uix.widget import Widget
from kivy.properties import NumericProperty, ReferenceListProperty,\
    ObjectProperty
from kivy.vector import Vector
from kivy.clock import Clock
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.lang import Builder
from kivy.core.text import LabelBase
from kivy.core.audio import SoundLoader

sound1 = SoundLoader.load('Brkovi- Opasno se drogiram.wav')
sound2 = SoundLoader.load('bounce.wav')
sound3 = SoundLoader.load('applause.wav')


LabelBase.register(name='Emulogic', fn_regular = 'Emulogic.ttf')



class PongPaddle(Widget):
    score = NumericProperty(0)
    last_pos = 0
    touched = False

    def bounce_ball(self, ball, bodovi, player1):
        if self.collide_widget(ball):
            
            if sound2:
                sound2.play()

            vx, vy = ball.velocity
            offset = (ball.center_y - self.center_y) / (self.height / 2)
            vel = Vector(-1 * vx, vy)
            if (vx*vx + vy*vy)<105:
                vel = vel * 1.1
            if player1.touched:
                ball.velocity = vel.x, vel.y - offset * 4 
            ball.velocity = vel.x, vel.y + offset
            #print(ball.size, type(ball.size))
            list_ball_size = list(ball.size)
            if list_ball_size[0]>20:
                ball.size = [i * 0.9 for i in list_ball_size]
            bodovi.amount = bodovi.amount - 10
            
                



class PongBall(Widget):
    velocity_x = NumericProperty(0)
    velocity_y = NumericProperty(0)
    velocity = ReferenceListProperty(velocity_x, velocity_y)

    def move(self):
        self.pos = Vector(*self.velocity) + self.pos

class PongGame(Widget):

    ball = ObjectProperty(None)
    player1 = ObjectProperty(None)
    player2 = ObjectProperty(None)
    level = NumericProperty(1)
    poruka = ObjectProperty(None)
    bodovi = ObjectProperty(None)
    def serve_ball(self, vel=(8, 0)):
        self.ball.center = self.center
        self.ball.velocity = vel

    def update(self, dt):
        self.ball.move()
        # bounce of paddles
        self.player1.bounce_ball(self.ball, self.bodovi, self.player1)
        self.player2.bounce_ball(self.ball, self.bodovi, self.player1)

        # bounce ball off bottom or top
        if (self.ball.y < self.y) or (self.ball.top > self.top):
            self.ball.velocity_y *= -1

        # went of to a side to score point?
        if self.ball.x < self.x:
            self.player2.score += 1
            self.ball.size= [150,150]
            self.serve_ball(vel=(8, 0))
        if self.ball.x > self.width:
            self.player1.score += 1
            self.ball.size= [150,150]
            self.serve_ball(vel=(-8, 0))
        if self.player1.score >= 3:
            self.level += 1
            if sound1:
                sound1.stop()
            self.poruka.msg = "Level {}".format(self.level)
            self.player1.score = 0
            self.player2.score = 0
        if self.player2.score > 3:
            self.parent.manager.current = 'highlight_screen'
            Clock.unschedule(self.update)
            #App.get_running_app().stop()
        if self.level==1:
            self.ball.img="drazen.jpg"
        if self.level==2:
            self.ball.img="vukoja.jpg"
        if self.level==3:
            self.ball.img="igor.jpg"
        if self.level==4:
            if sound3:
                sound3.play()

            self.parent.manager.current = 'highlight_screen'
            Clock.unschedule(self.update)
            #App.get_running_app().stop()

        self.player1.touched = False
        self.player2.center_y += (self.ball.center_y - self.player2.center_y)/25



    def on_touch_move(self, touch):
        self.player1.last_pos = self.player1.center_y
        if touch.x < self.width / 2:
            self.player1.center_y = touch.y
            self.player1.touched = True
    




# Declare both screens
class MenuScreen(Screen):
    pass


class GameScreen(Screen):
#    def printaj(self):
#        print("Huhuhu")
    def start_game(self):
#        print(self.game)
        if sound1:
            sound1.play()
        self.game = PongGame()
        self.add_widget(self.game)
        self.game.serve_ball()
        Clock.schedule_interval(self.game.update, 1.0 / 60.0)
    def restart_game(self):
        sound1.stop()
        self.remove_widget(self.game)
        self.remove_widget(self.game.ball)
        self.remove_widget(self.game.player1)
        self.remove_widget(self.game.player2)
        self.remove_widget(self.game.bodovi)




    def close_game(self):
        App.get_running_app().stop()


class HighlightScreen(Screen):
    pass


class ScreenManagement(ScreenManager):
    pass

t = Builder.load_file('screen.kv')


class MyApp(App):
    def build(self):
        self.title = 'Odmetnici odrzavanja'
        self.icon = 'logo.png'
        return t



if __name__ == '__main__':
    MyApp().run()

