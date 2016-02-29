#!/usr/bin/python2.7

import kivy
kivy.require('1.9.0') # replace with your current kivy version !
from psd_tools import PSDImage
import re

from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.image import Image
from kivy.uix.widget import Widget
from kivy.uix.effectwidget import EffectWidget
from kivy.properties import ObjectProperty
from kivy.uix.effectwidget import EffectWidget, AdvancedEffectBase, EffectBase

ASSETDIR='/opt/projects/python/beaglebone/assets'

buttonlist = { 'ac':1,
               'ac_status':2,
               'fanwave_status':3,
               'boxwave_status':4,
               'boxwave':5,
               'fanup':6,
               'tempup':7,
               'fandown':8,
               'tempdown':9,
               'temperature_x':10,
               'arrow_foot':11,
               'arrow_head':12,
               'fanspeed_x':13,
               'person':14,
               'dir_head':15,
               'dir_both':16,
               'dir_feet':17,
               'fanwave':18,
             }


class BeagleboneTemps(Widget):
    pass

class BeagleboneApp(App):
    def get_assets(self, dir=ASSETDIR):
        psd_file_loc = "%s/assets.psd" % ASSETDIR
        psd = PSDImage.load(psd_file_loc)

        x,y = psd.bbox[-2:]

        layers = {}
        for layer in psd.layers:
            layer_name = layer.name
            layer_as_pil = layer.as_PIL()

            layer_file_loc = "%s/%s.png" % (dir, layer_name)
            layer_as_pil.save(layer_file_loc)

            layers[layer_name] = {
                                'bbox':layer.bbox,
                                'loc':layer_file_loc }
        print "HEY",x,y
        return x,y, layers

    def send_signal(self, b):
        button_name = b.id
        print button_name

        if re.match("^fanspeed_[0-9]+$", button_name):
            new_fanspeed = button_name.split('_')[-1]
            print new_fanspeed

        if re.match("^temperature_[0-9]+$", button_name):
            new_temp = button_name.split('_')[-1]
            print new_temp 

    def add_layers(self, root, layers):
        for layer_name,layer in layers.items():
            x1,y1,x2,y2 = layer['bbox']
            layer_loc = layer['loc']

            button_widget = Button(background_normal=layer_loc, pos=(x1,y1))
            button_widget.id = layer_name
            button_widget.bind(on_press=self.send_signal)

            root.add_widget(button_widget)

    def build(self):
        root = BeagleboneTemps()
        width, height, layers = self.get_assets()

        root.width = width
        root.height = height

        self.add_layers(root, layers)

        return root


if __name__ == '__main__':
    BeagleboneApp().run()
