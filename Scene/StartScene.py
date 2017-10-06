from vpython import *
import time

from Scene.BaseScene import BaseScene


class StartScene(BaseScene):
    def __init__(self):
        BaseScene.__init__(self)
        self.scene.userspin = False
        self.started = False

    def wait_for_start(self):
        while not self.started:
            ev = self.scene.waitfor('click')
            self.on_click(ev)

    def init_objects(self):
        self.start_button = box(pos=vector(0, 0, 0), size=vector(8, 2, 1))
        self.start_label = label(pos=self.start_button.pos, xoffset=0, yoffset=0, text='New Game', color=color.black, opacity=0, line=False, height=20, box=False)
        self.title = text(pos=vector(0, 5, 0), text='Morpion 3D', align='center', color=color.green, billboard=True, depth=0.5)
        return [self.start_button, self.start_label, self.title]

    def on_click(self, evt):
        obj = self.scene.mouse.pick
        if obj == self.start_button:
            self.started = True
        else:
            self.start_button.color = color.white
