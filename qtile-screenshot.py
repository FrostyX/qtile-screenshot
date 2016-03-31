#!/usr/bin/python

import time
from gtk import gdk
from libqtile.command import Client


def print_screen():
    w = gdk.get_default_root_window()
    sz = w.get_size()
    print "The size of the window is %d x %d" % sz
    pb = gdk.Pixbuf(gdk.COLORSPACE_RGB,False,8,sz[0],sz[1])
    pb = pb.get_from_drawable(w,w.get_colormap(),0,0,0,0,sz[0],sz[1])
    return pb


def compose(pb1, pb2):
    pb3 = gdk.Pixbuf(gdk.COLORSPACE_RGB, False, 8, pb1.props.width + pb2.props.width, pb1.props.height)
    pb1.composite(pb3, 0, 0, pb1.props.width, pb1.props.height, 0, 0, 1.0, 1.0, gdk.INTERP_HYPER, 255)
    pb2.composite(pb3, pb1.props.width, 0, pb2.props.width, pb1.props.height, pb1.props.width, 0, 1.0, 1.0, gdk.INTERP_HYPER, 255)
    return pb3


def main():
    c = Client()
    current_screen = c.screen.info()["index"]
    current_group = c.group.info()["name"]

    shoots = []
    for group in c.groups():
        c.group[group].toscreen(0)
        time.sleep(0.1)
        shoots.append(print_screen())
    c.group[current_group].toscreen(0)

    img = shoots[0]
    for shoot in shoots[1:]:
        img = compose(img, shoot)

    img.save("/tmp/screenshot.png","png")


if __name__ == "__main__":
    main()
