#!/usr/bin/python


import os
import time
import argparse
from datetime import datetime
from libqtile.command import Client

import gi
gi.require_version('Gdk', '3.0')
from gi.repository import Gdk, GdkPixbuf


parser = argparse.ArgumentParser(
    prog = "qtile-screenshot",
    description="Make screenshot of all your groups"
)

parser.add_argument("--groups", "--desktops", "--workspaces",
    dest="groups",
    nargs="*",
    type=str,
    default=[],
    help="workspaces that only should be on the screenshot"
)

parser.add_argument("-e", "--with-empty",
    dest="empty",
    action="store_true",
    help="make screenshot even from empty workspaces"
)

parser.add_argument("--one-empty",
    dest="one_empty",
    action="store_true",
    help="show at most one empty groups if there is such"
)

parser.add_argument('-o', '--output',
    type=str,
    dest='output',
    help='path to output directory or path to screenshot file'
)

args = parser.parse_args()


def print_screen():
    w = Gdk.get_default_root_window()
    sz = w.get_geometry()[2:4]
    pb = Gdk.pixbuf_get_from_window(w, 0, 0, sz[0], sz[1])
    return pb


def compose(pb1, pb2):
    pb3 = GdkPixbuf.Pixbuf.new(GdkPixbuf.Colorspace.RGB, False, 8, pb1.props.width + pb2.props.width, pb1.props.height)
    pb1.composite(pb3, 0, 0, pb1.props.width, pb1.props.height, 0, 0, 1.0, 1.0, GdkPixbuf.InterpType.HYPER, 255)
    pb2.composite(pb3, pb1.props.width, 0, pb2.props.width, pb1.props.height, pb1.props.width, 0, 1.0, 1.0, GdkPixbuf.InterpType.HYPER, 255)
    return pb3


def groups(qtile):
    # @TODO Sort groups in a way that they are in the bar
    if args.groups:
        return filter(lambda x: x in qtile.groups(), args.groups)
    elif args.empty:
        return qtile.groups()
    elif args.one_empty:
        return ((filter(lambda x: not qtile.groups()[x]["windows"], qtile.groups()) + [None])[:1] +
                filter(lambda x: qtile.groups()[x]["windows"], qtile.groups()))
    return filter(lambda x: qtile.groups()[x]["windows"], qtile.groups())


def main():
    c = Client()
    current_screen = c.screen.info()["index"]
    current_group = c.group.info()["name"]

    shoots = []
    for group in groups(c):
        c.group[group].toscreen(0)
        time.sleep(0.1)
        shoots.append(print_screen())
    c.group[current_group].toscreen(0)

    img = shoots[0]
    for shoot in shoots[1:]:
        img = compose(img, shoot)


    dirname = "/tmp"
    basename = datetime.now().strftime("qtile_%F_%R:%S")
    if args.output:
        dirname = args.output if os.path.isdir(args.output) else os.path.dirname(args.output)
        basename = basename if os.path.isdir(args.output) else os.path.basename(args.output)
    img.savev(os.path.join(dirname, basename), "png", [], [])


if __name__ == "__main__":
    main()
