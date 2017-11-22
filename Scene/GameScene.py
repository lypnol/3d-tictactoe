from vpython import *
import itertools

from Scene.BaseScene import BaseScene
from Scene.utils import hex_to_color_vector


class GameScene(BaseScene):
    SPACING = 10
    BOX_SIZE = 4

    def __init__(self, n, x_color, o_color, remote_enabled=True):
        BaseScene.__init__(self)
        self.n = n
        self.remote_enabled = remote_enabled
        # color conversion to vector
        self.colors = {
            'x': hex_to_color_vector(x_color),
            'o': hex_to_color_vector(o_color)
        }
        # click event
        self.scene.bind('click', self.on_click)
        self.disable_actions = False
        # objets
        self.boxes = {}
        self.restart_button_local = None
        self.restart_button_remote = None
        self.restart_label_local = None
        self.restart_label_remote = None
        self.title = None
        self.selected = set()
        self.curve = None
        # external events handlers
        self._on_select = None
        self._on_restart = None

    def box_id_to_pos(self, box_id):
        """returns the position in space of a cube, given its id"""
        n = self.n
        pos_min = -(n-1) * self.SPACING / 2
        x, y, z = map(lambda i: i * self.SPACING + pos_min, box_id)
        return vector(x, y, z)

    def searching_for_opponent(self):
        self.hide_restart()
        self.disable_actions = True
        self.title.text = 'Waiting for opponent...'
        self.title.color = color.white
        self.title.visible = True

    def start_new_game(self):
        self.hide_restart()
        self.disable_actions = False
        self.title.visible = True

    def player_turn(self, player):
        self.title.text = "Your turn"
        self.title.color = self.colors[player]
        self.disable_actions = False

    def opponent_turn(self, player):
        self.title.text = "Opponent's turn"
        self.title.color = self.colors[player]
        self.disable_actions = True

    def init_objects(self):
        n = self.n
        self.title = label(pos=vector(0, 20, 0), xoffset=0, yoffset=0, text='Waiting for opponent...', align='center', color=color.white, opacity=0, line=False, height=25, box=False)
        self.restart_button_local = box(pos=vector(-8, -18, 0), size=vector(15, 4, 2))
        self.restart_button_remote = box(pos=vector(8, -18, 0), size=vector(15, 4, 2))
        self.restart_label_local = text(pos=vector(-8, -18, 1), align='center', text='Restart Local', color=color.black)
        self.restart_label_remote = text(pos=vector(8, -18, 1), align='center', text='Restart Remote', color=color.black)
        for box_id in itertools.product([i for i in range(n)], repeat=3):
            self.boxes[box_id] = box(
                pos=self.box_id_to_pos(box_id),
                color=color.white,
                length=self.BOX_SIZE, height=self.BOX_SIZE, width=self.BOX_SIZE)
        return [self.title, self.restart_button_local, self.restart_button_remote, self.restart_label_local, self.restart_label_remote] + list(self.boxes.values())

    def restart(self, game_type='local'):
        self.selected = set()
        for box_id, box in self.boxes.items():
            box.color = color.white
            if self.curve: self.curve.visible = False
        if self.on_restart: self.on_restart(game_type)

    def draw_link(self, link, player):
        if self.curve is None:
            self.curve = curve([self.boxes[box_id].pos for box_id in link], color=self.colors[player])
        else:
            self.curve.clear()
            for box_id in link:
                self.curve.append(self.boxes[box_id].pos)
            self.curve.color = self.colors[player]
            self.curve.visible = True

    def game_over(self, end_data):
        winner, points = end_data
        self.disable_actions = True
        if winner == 'NULL':
            self.title.text = 'Draw'
            self.title.color = white.color
        else:
            self.title.text = 'Player wins'
            self.draw_link(list(map(tuple, points)), winner)
        self.show_restart()

    def show_restart(self):
        self.restart_button_local.visible = True
        self.restart_button_remote.visible = self.remote_enabled
        self.restart_label_local.visible = True
        self.restart_label_remote.visible = self.remote_enabled

    def hide_restart(self):
        self.restart_button_local.visible = False
        self.restart_button_remote.visible = False
        self.restart_label_local.visible = False
        self.restart_label_remote.visible = False

    def on_opponent_left(self):
        """handle the event of the opponent's disconnection"""
        self.title.color = color.red
        self.title.text = 'Opponent left'
        self.disable_actions = True
        self.show_restart()

    def on_click(self, evt):
        obj = self.scene.mouse.pick
        if not self.disable_actions:
            for box_id, box in self.boxes.items():
                if obj == box and box_id not in self.selected:
                    if self.on_select is not None: self.on_select(box_id)
                    break
        else:
            if obj == self.restart_button_local:
                self.restart('local')
            elif obj == self.restart_button_remote and self.remote_enabled:
                self.restart('remote')
            if self.curve: self.curve.clear()

    def select_box(self, box_id, player):
        x, y, z = box_id
        if (x, y, z) not in self.boxes:
            return
        box = self.boxes[(x, y, z)]
        box.color = self.colors[player]
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
