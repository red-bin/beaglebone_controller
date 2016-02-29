#!/usr/bin/python2.7

from psd_tools import PSDImage

ASSETDIR='/opt/projects/python/beaglebone/assets'
psd_file_loc = "%s/assets.psd" % ASSETDIR
psd = PSDImage.load(psd_file_loc)

for layer in psd.layers:
    layer_pos_str = "%s_%s_%s_%s" % layer.bbox
    layer_name = layer.name
    layer_filename = "%s_%s.png" % (layer_name, layer_pos_str)

    layer_as_pil = layer.as_PIL()

    layer_file_loc = "%s/%s" % (ASSETDIR, layer_filename)
    layer_as_pil.save(layer_file_loc)
