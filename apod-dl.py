#!/usr/bin/env python

# apod-dl.py -- Download current Astronomy Photo of the Day (APOD) from
# apod.nasa.gov

# Created 19 Feb 2017 by Brad Eisenhauer

# Download the current APOD and write downloaded file location to stdout for
# consumption by other scripts. APOD will be downloaded to Pictures/apod
# folder in user's home directory, preserving the original file name.

from __future__ import print_function
import urllib
import os
from HTMLParser import HTMLParser
import sys

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

def eprint( *args, **kwargs ):
    print( *args, file=sys.stderr, **kwargs )

def main():
    url = get_image_url()
    if get_filename( url ) == '':
        eprint( 'There doesn\'t appear to be an image today.' )
        return 1
    dlfile = get_pictures_dir() + '/apod/' + get_filename( url )
    if not os.path.exists( dlfile ):
        urllib.urlretrieve( url, dlfile )
    print( dlfile )
    return 0

if __name__ == '__main__':
    sys.exit( main() )
