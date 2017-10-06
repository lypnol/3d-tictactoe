from vpython import *
import itertools

from Scene.BaseScene import BaseScene
from Scene.utils import hex_to_color_vector


class GameScene(BaseScene):
    SPACING = 10
    BOX_SIZE = 4

    def __init__(self, n, x_color, o_color):
        BaseScene.__init__(self)
        self.n = n
        self.x_color = hex_to_color_vector(x_color)
        self.o_color = hex_to_color_vector(o_color)
        self.current_color = self.x_color
        self.on_select = None
        self.curve = None
        self.scene.bind('click', self.on_click)

    def box_id_to_pos(self, box_id):
        n = self.n
        pos_min = -(n-1) * self.SPACING / 2
        x, y, z = map(lambda i: i * self.SPACING + pos_min, box_id)
        return vector(x, y, z)

    def init_objects(self):
        n = self.n
        self.boxes = {}
        self.selected = set()
        for box_id in itertools.product([i for i in range(n)], repeat=3):
            self.boxes[box_id] = box(
                pos=self.box_id_to_pos(box_id),
                color=color.white,
                length=self.BOX_SIZE, height=self.BOX_SIZE, width=self.BOX_SIZE)
        return self.boxes.values()

    def draw_link(self, link):
        if self.curve is None:
            self.curve = curve([self.boxes[box_id].pos for box_id in link], color=self.current_color)

    def game_over(self, state):
        (result, points) = state
        # TODO Ce qu'on fait quand la partie est terminée
        # state: est ce qui est retourné par TicTacToe.check_end_game quand result est different de None
        pass

    def set_on_select(self, on_select):
        self.on_select = on_select

    def switch_colors(self):
        if self.current_color == self.o_color:
            self.current_color = self.x_color
        else:
            self.current_color = self.o_color

    def on_click(self, evt):
        obj = self.scene.mouse.pick
        for (x, y, z), box in self.boxes.items():
            if obj == box and (x, y, z) not in self.selected:
                box.color = self.current_color
                self.selected.add((x, y, z))
                self.on_select((x, y, z))
                break

    def select_box(self, box_id):
        x, y, z = box_id
        if (x, y, z) not in self.boxes:
            return
        box = self.boxes[(x, y, z)]
        box.color = self.current_color
        self.selected.add((x, y, z))
