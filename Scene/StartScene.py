from vpython import *
import time

from Scene.BaseScene import BaseScene


class StartScene(BaseScene):
    def __init__(self, remote=False):
        BaseScene.__init__(self)
        self.scene.userspin = False
        self.remote = remote

    def wait_for_start(self):
        while True:
            ev = self.scene.waitfor('click')
            game_type = self.on_click(ev)
            if game_type:
                return game_type

    def init_objects(self):
        self.start_button_local = box(pos=vector(0, 1.2, 0), size=vector(8, 2, 1))
        self.start_button_remote = None if not self.remote else box(pos=vector(0, -1.2, 0), size=vector(8, 2, 1))
        self.start_label_local = label(pos=self.start_button_local.pos, xoffset=0, yoffset=0, text='Local Game', color=color.black, opacity=0, line=False, height=20, box=False)
        self.start_label_remote = None if not self.remote else label(pos=self.start_button_remote.pos, xoffset=0, yoffset=0, text='Remote Game', color=color.black, opacity=0, line=False, height=20, box=False)
        self.title = text(pos=vector(0, 5, 0), text='Morpion 3D', align='center', color=color.green, billboard=True, depth=0.5)
        return filter(lambda x: x is not None, [self.start_button_local, self.start_button_remote, self.start_label_local, self.start_label_remote, self.title])

    def on_click(self, evt):
        obj = self.scene.mouse.pick
        if obj == self.start_button_local:
            self.started = True
            return 'local'
        elif obj == self.start_button_remote and self.remote:
            self.started = True
            return 'remote'
