from kivy.app import App
from kivy.core.audio import SoundLoader
from kivy.lang import Builder
from kivy.properties import StringProperty, NumericProperty, ListProperty
from kivy.uix.widget import Widget
from random import choice
from functools import partial

KV = '''
#:import random_rand kivy.utils.get_random_color

<Board>:
    canvas.before:
        Rectangle:
            pos: self.pos
            size: self.size
            source: 'assets/bg.jpg'
    GridLayout:
        id: grid
        cols: 3
        rows: 3
        spacing: dp(4)
        padding: dp(10)
        on_children: root.arrange_buttons()

<MagicButton@Button>:
    symbol: ''
    font_size: dp(48)
    color: self.color
    background_color: (0,0,0,0)
    on_press:
        if self.symbol == '':
            self.symbol = root.parent.parent.current_player
            root.parent.parent.on_tile(self.index)
    canvas.after:
        PushMatrix
        Color:
            rgba: self.color + [1]
        Ellipse:
            size: (self.width*0.2, self.height*0.2)
            pos: (self.center_x - self.width*0.1 + self.anim_x,
                  self.center_y - self.height*0.1 + self.anim_y)
        PopMatrix

BoxLayout:
    orientation: 'vertical'
    spacing: dp(10)
    padding: dp(10)
    Board:
        id: board
    BoxLayout:
        size_hint_y: None
        height: dp(50)
        Button:
            text: 'Restart'
            on_press: board.reset()
        ToggleButton:
            id: mode
            text: 'AI Mode'
            state: 'down'
            on_state:
                board.ai_mode = (self.state == 'down')
'''

class Board(Widget):
    ai_mode = True
    current_player = StringProperty('X')
    board = ListProperty([''] * 9)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.snd_place = SoundLoader.load('assets/chime.wav')
        self.snd_win = SoundLoader.load('assets/win.wav')
        self.snd_lose = SoundLoader.load('assets/lose.wav')

    def arrange_buttons(self):
        grid = self.ids.grid
        if len(grid.children) == 0:
            for i in range(9):
                btn = Builder.template('MagicButton',index=i)
                btn.color = get_random_color()
                btn.anim_x = 0
                btn.anim_y = 0
                grid.add_widget(btn)

    def on_tile(self, idx):
        btn = self.ids.grid.children[8 - idx]
        btn.anim_x = choice([-10,10])
        btn.anim_y = choice([-10,10])
        if self.snd_place: self.snd_place.play()
        self.board[idx] = self.current_player
        if self.check_win(self.current_player):
            if self.snd_win: self.snd_win.play()
            self.end_game(f"Player {self.current_player} wins!")
            return
        if '' not in self.board:
            if self.snd_lose: self.snd_lose.play()
            self.end_game("Draw!")
            return
        self.current_player = 'O' if self.current_player == 'X' else 'X'
        if self.ai_mode and self.current_player == 'O':
            self.ai_move()

    def ai_move(self):
        avail = [i for i, v in enumerate(self.board) if v=='']
        idx = choice(avail)
        btn = self.ids.grid.children[8 - idx]
        btn.dispatch('on_press')

    def check_win(self, p):
        wins = [(0,1,2),(3,4,5),(6,7,8),
                (0,3,6),(1,4,7),(2,5,8),
                (0,4,8),(2,4,6)]
        return any(all(self.board[i]==p for i in combo) for combo in wins)

    def end_game(self, message):
        from kivy.uix.popup import Popup
        from kivy.uix.boxlayout import BoxLayout
        from kivy.uix.label import Label
        from kivy.uix.button import Button
        content = BoxLayout(orientation='vertical')
        content.add_widget(Label(text=message, font_size=48))
        btn = Button(text='OK', size_hint=(1,0.3))
        content.add_widget(btn)
        popup = Popup(title='Game Over', content=content, size_hint=(0.7,0.4))
        btn.bind(on_press=lambda *a: popup.dismiss())
        popup.bind(on_dismiss=lambda *a: self.reset())
        popup.open()

    def reset(self):
        self.board = [''] * 9
        for btn in self.ids.grid.children:
            btn.symbol = ''
        self.current_player = 'X'

class TTTApp(App):
    def build(self):
        return Builder.load_string(KV)

if __name__ == '__main__':
    TTTApp().run()
