import kivy
from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.widget import Widget
from kivy.properties import NumericProperty
from kivy.clock import Clock
from kivy.graphics import Color, Rectangle  # Import Color and Rectangle
from random import randint, choice
from functools import partial

kivy.require('2.0.0')

class GameTile(Label):
    value = NumericProperty(0)

    def __init__(self, **kwargs):
        super(GameTile, self).__init__(**kwargs)
        self.update_tile()
        self.bind(pos=self.update_tile, size=self.update_tile)

    def update_tile(self, *args):
        if self.value > 0:
            self.text = str(self.value)
        else:
            self.text = ""
        self.background_color = {
            0: (0.7, 0.7, 0.7, 1),
            2: (0.9, 0.9, 0.9, 1),
            4: (0.8, 0.8, 0.6, 1),
            8: (0.8, 0.6, 0.4, 1),
            16: (0.8, 0.4, 0.2, 1),
            32: (0.8, 0.3, 0.1, 1),
            64: (0.8, 0.2, 0, 1),
            128: (0.7, 0.1, 0, 1),
            256: (0.6, 0, 0, 1),
            512: (0.5, 0, 0, 1),
            1024: (0.4, 0, 0, 1),
            2048: (0.3, 0, 0, 1)
        }.get(self.value, (0.2, 0, 0, 1))
        self.canvas.before.clear()
        with self.canvas.before:
            Color(rgba=self.background_color)
            Rectangle(size=self.size, pos=self.pos)

class Game2048(App):
    def build(self):
        self.title = '2048 Game'
        root = BoxLayout(orientation='vertical')
        self.score_label = Label(text='Score: 0', font_size=24, size_hint_y=None, height=50)
        root.add_widget(self.score_label)
        self.grid = GridLayout(rows=4, cols=4, spacing=10, padding=10)
        root.add_widget(self.grid)
        self.restart_button = Button(text='Restart', size_hint_y=None, height=50)
        self.restart_button.bind(on_press=self.restart_game)
        root.add_widget(self.restart_button)
        self.tiles = [[None for _ in range(4)] for _ in range(4)]
        self.restart_game()
        return root

    def restart_game(self, *args):
        self.score = 0
        self.update_score()
        self.grid.clear_widgets()
        for row in range(4):
            for col in range(4):
                self.tiles[row][col] = GameTile(value=0)
                self.grid.add_widget(self.tiles[row][col])
        self.add_random_tile()
        self.add_random_tile()

    def add_random_tile(self):
        empty_tiles = [(r, c) for r in range(4) for c in range(4) if self.tiles[r][c].value == 0]
        if not empty_tiles:
            return
        row, col = choice(empty_tiles)
        self.tiles[row][col].value = choice([2, 4])
        self.tiles[row][col].update_tile()

    def update_score(self):
        self.score_label.text = f'Score: {self.score}'

    def on_start(self):
        self._keyboard = self.root_window.request_keyboard(self._keyboard_closed, self)
        self._keyboard.bind(on_key_down=self._on_keyboard_down)

    def _keyboard_closed(self):
        self._keyboard.unbind(on_key_down=self._on_keyboard_down)
        self._keyboard = None

    def _on_keyboard_down(self, keyboard, keycode, text, modifiers):
        if keycode[1] in ['left', 'right', 'up', 'down']:
            self.move(keycode[1])
        return True

    def move(self, direction):
        def slide(row):
            new_row = [i for i in row if i != 0]
            new_row += [0] * (4 - len(new_row))
            for i in range(3):
                if new_row[i] == new_row[i + 1]:
                    new_row[i] *= 2
                    new_row[i + 1] = 0
                    self.score += new_row[i]
                    self.update_score()
            new_row = [i for i in new_row if i != 0]
            new_row += [0] * (4 - len(new_row))
            return new_row

        rotated = False
        if direction in ['up', 'down']:
            self.tiles = [list(x) for x in zip(*self.tiles)]
            rotated = True
        if direction in ['right', 'down']:
            self.tiles = [row[::-1] for row in self.tiles]
        for i in range(4):
            self.tiles[i] = slide([tile.value for tile in self.tiles[i]])
            for j in range(4):
                self.tiles[i][j] = GameTile(value=self.tiles[i][j])
        if direction in ['right', 'down']:
            self.tiles = [row[::-1] for row in self.tiles]
        if rotated:
            self.tiles = [list(x) for x in zip(*self.tiles)]
        self.grid.clear_widgets()
        for row in range(4):
            for col in range(4):
                self.grid.add_widget(self.tiles[row][col])
        self.add_random_tile()

if __name__ == '__main__':
    Game2048().run()
