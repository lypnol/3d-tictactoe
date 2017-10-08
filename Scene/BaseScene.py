from vpython import *


WIDTH, HEIGHT = 580, 700

class BaseScene:
    def __init__(self):
        self.scene = canvas(width=WIDTH, height=HEIGHT)
        self.scene.userzoom = False
        self.scene.visible = False
        self.objects = None

    def show(self):
        if not self.objects:
            self.objects = self.init_objects()
        for obj in self.objects:
            obj.visible = True
        self.scene.waitfor('draw_complete')
        self.scene.visible = True
        self.scene.select()

    def hide(self):
        self.scene.visible = False
        for obj in self.objects:
            obj.visible = False
        self.scene.delete()

    def init_objects(self):
        return []
