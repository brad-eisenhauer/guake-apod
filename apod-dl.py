#!/usr/bin/env python

# apod-dl.py -- Download current Astronomy Photo of the Day (APOD) from
# apod.nasa.gov

# Created 19 Feb 2017 by Brad Eisenhauer

# Download the current APOD and write downloaded file location to stdout for
# consumption by other scripts. APOD will be downloaded to Pictures/apod
# folder in user's home directory, preserving the original file name.

from __future__ import print_function
from __future__ import division

from HTMLParser import HTMLParser
from PIL import Image

import gtk
import operator
import os
import sys
import urllib


DEBUG=False

class ApodHtmlParser( HTMLParser ):
    # url of full-sized APOD
    full_photo_url = ''

    # search anchor tags for photo url
    def handle_starttag( self, tag, attrs ):
        if self.full_photo_url == '' and tag == 'a':
            self.set_url_if_image( dict( attrs )[ 'href' ])

    # if href is photo url, set full_photo_url
    def set_url_if_image( self, href ):
        if href.startswith( 'image/' ):
            self.full_photo_url = href

def get_image_url():
    baseurl = 'https://apod.nasa.gov/apod/'
    response = urllib.urlopen( baseurl + 'astropix.html')
    parser = ApodHtmlParser()
    parser.feed( response.read() )
    response.close()
    return baseurl + parser.full_photo_url

def get_pictures_dir():
    return os.getenv( 'HOME' ) + '/Pictures'

def get_filename( image_url ):
    return image_url.split( '/' )[ -1 ]

def dprint( *args, **kwargs ):
    if (DEBUG == True):
        print( *args, file=sys.stderr, **kwargs)

def eprint( *args, **kwargs ):
    print( *args, file=sys.stderr, **kwargs )

def get_resize_dims(image):
    """Calculate dimensions of resized image based on original image dimensions
        and current screen resolution. If possible, shrink the image so that the
        entire screen fits within the image, but either the width or height of
        the image matches the corresponding dimension of the screen. Do not
        enlarge the image."""
    target_size = (gtk.gdk.screen_width(), gtk.gdk.screen_height())
    resize_ratio = max(tar / src for tar, src in zip(target_size, image.size))
    if (resize_ratio > 1):
        return image.size
    return tuple(round(resize_ratio * d) for d in image.size)
    
def resize_image(image_file):
    """Create a resized copy of image_file with extension '.resize/jpg'. Return
        the name of the resized image. If dimensions to resize to are the same
        the original dimensions, do not create a copy and return instead the
        original file name."""
    outfile = os.path.splitext(image_file)[0] + '.resize.jpg'
    try:
        im = Image.open(image_file)
        to_size = get_resize_dims(im)
        if (im.size == to_size):
            return image_file
        im.thumbnail(target_size)
        im.save(outfile, "JPEG")
        return outfile
    except IOError:
        eprint('Cannot resize "%s"', image_file)
    return image_file

def main():
    url = get_image_url()
    if get_filename( url ) == '':
        eprint( 'There doesn\'t appear to be an image today.' )
        return 1
    dlfile = get_pictures_dir() + '/apod/' + get_filename( url )
    if not os.path.exists( dlfile ):
        urllib.urlretrieve( url, dlfile )
        dlfile = resize_image(dlfile)
    print( dlfile )
    return 0

if __name__ == '__main__':
    sys.exit( main() )
