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
        # couleurs
        self.x_color = hex_to_color_vector(x_color)
        self.o_color = hex_to_color_vector(o_color)
        self.current_color = self.x_color
        # click event
        self.scene.bind('click', self.on_click)
        self.disable_actions = False
        # objets
        self.boxes = {}
        self.title = None
        self.selected = set()
        self.curve = None
        # external events handlers
        self._on_select = None

    def box_id_to_pos(self, box_id):
        n = self.n
        pos_min = -(n-1) * self.SPACING / 2
        x, y, z = map(lambda i: i * self.SPACING + pos_min, box_id)
        return vector(x, y, z)

    def wait_for_opponent(self):
        self.disable_actions = True
        self.title.text = 'Waiting for opponent...'
        self.title.visible = True

    def component_is_ready(self):
        self.disable_actions = False
        self.title.text = 'Your turn'
        self.title.color = self.x_color
        self.title.visible = True

    def init_objects(self):
        n = self.n
        self.title = label(pos=vector(0, 20, 0), xoffset=0, yoffset=0, text='Waiting for opponent...', align='center', color=color.white, opacity=0, line=False, height=25, box=False)
        for box_id in itertools.product([i for i in range(n)], repeat=3):
            self.boxes[box_id] = box(
                pos=self.box_id_to_pos(box_id),
                color=color.white,
                length=self.BOX_SIZE, height=self.BOX_SIZE, width=self.BOX_SIZE)
        return [self.title] + list(self.boxes.values())

    def draw_link(self, link):
        if self.curve is None:
            self.curve = curve([self.boxes[box_id].pos for box_id in link], color=self.current_color)

    def game_over(self, end_data):
        (result, points) = end_data
        # TODO Ce qu'on fait quand la partie est terminée
        # end_data: est ce qui est retourné par TicTacToe.check_end_game quand result est different de None

    def switch_colors(self):
        if self.current_color == self.o_color:
            self.current_color = self.x_color
            self.title.text = 'Your turn'
        else:
            self.current_color = self.o_color
            self.title.text = 'Opponent turn'
        self.title.color = self.current_color

    def on_click(self, evt):
        obj = self.scene.mouse.pick
        if not self.disable_actions:
            for box_id, box in self.boxes.items():
                if obj == box and box_id not in self.selected:
                    box.color = self.current_color
                    self.selected.add(box_id)
                    if self.on_select is not None: self.on_select(box_id)
                    break

    def select_box(self, box_id):
        x, y, z = box_id
        if (x, y, z) not in self.boxes:
            return
        box = self.boxes[(x, y, z)]
        box.color = self.current_color
        self.selected.add((x, y, z))

    def _get_on_select(self):
        return self._on_select
    def _set_on_select(self, on_select):
        self._on_select = on_select

    def _get_on_restart(self):
        return self._on_restart
    def _set_on_restart(self, on_restart):
        self._on_restart = on_restart

    on_select = property(_get_on_select, _set_on_select)
    on_restart = property(_get_on_restart, _set_on_restart)
