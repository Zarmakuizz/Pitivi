# PiTiVi , Non-linear video editor
#
#       pitivi/elements/thumbnailsink.py
#
# Copyright (c) 2005, Edward Hervey <bilboed@bilboed.com>
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU Lesser General Public
# License as published by the Free Software Foundation; either
# version 2.1 of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public
# License along with this program; if not, write to the
# Free Software Foundation, Inc., 59 Temple Place - Suite 330,
# Boston, MA 02111-1307, USA.
"""
GdkPixbuf thumbnail sink
"""

import gobject
import gst
import gtk

class PixbufThumbnailSink(gst.BaseSink):

    __gsignals__ = {
        "thumbnail" : (gobject.SIGNAL_RUN_LAST,
                       gobject.TYPE_NONE,
                       ( gobject.TYPE_PYOBJECT, gobject.TYPE_UINT64 ))
        }

    __gsttemplates__ = (
        gst.PadTemplate ("sink",
                         gst.PAD_SINK,
                         gst.PAD_ALWAYS,
                         gst.Caps("video/x-raw-rgb,"
                                  "bpp = (int) 24, depth = (int) 24,"
                                  "endianness = (int) BIG_ENDIAN,"
                                  "red_mask = (int) 0x00FF0000, "
                                  "green_mask = (int) 0x0000FF00, "
                                  "blue_mask = (int) 0x000000FF, "
                                  "width = (int) [ 1, max ], "
                                  "height = (int) [ 1, max ], "
                                  "framerate = (fraction) [ 0, max ]"))
        )

    def __init__(self):
        gst.BaseSink.__init__(self)
        self._width = 1
        self._height = 1
        self.set_sync(False)

    def do_set_caps(self, caps):
        self.width = caps[0]["width"]
        self.height = caps[0]["height"]
        return True

    def do_render(self, buffer):
        pixb = gtk.gdk.pixbuf_new_from_data(buffer.data,
                                            gtk.gdk.COLORSPACE_RGB,
                                            False,
                                            8,
                                            self.width,
                                            self.height,
                                            self.width * 3)

        self.emit('thumbnail', pixb, buffer.timestamp)
        return gst.FLOW_OK