from kivy.uix.image import Image


class Sprite(Image):

    def __init__(self, **kwargs):
        kwargs.setdefault('allow_stretch', True)
        kwargs.setdefault('keep_ratio', False)
        super(Sprite, self).__init__(**kwargs)
