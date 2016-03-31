#!/usr/bin/python

import time
import argparse
from gtk import gdk
from libqtile.command import Client

parser = argparse.ArgumentParser(
    prog = "qtile-screenshot",
    description="Make screenshot of all your groups"
)

# @TODO
parser.add_argument("--groups", "--desktops", "--workspaces",
    dest="groups",
    nargs="*",
    type=str,
    default=[],
    help="workspaces that only should be on the screenshot"
)

# @TODO
parser.add_argument("-e", "--with-empty",
    dest="empty",
    action="store_true",
    help="make screenshot even from empty workspaces"
)

# @TODO
parser.add_argument("--one-empty",
    dest="one_empty",
    action="store_true",
    help="show at most one empty groups if there is such"
)


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
    args = parser.parse_args()

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
