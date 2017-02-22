#!/usr/bin/env sh

# guake-spod.sh -- Download Astronomy Photo of the Day from apod.nasa.gov and
# set as guake terminal background.

# Created 19 Feb 2017 by Brad Eisenhauer

dl_response=$(apod-dl.py)

if [ $? = "0" ]; then
	gconftool-2 -s -t string /apps/guake/style/background/image $dl_response
	echo "Successfully downloaded APOD to $dl_response and set as guake background."
else
	echo "Error occurred downloading file."
fi
