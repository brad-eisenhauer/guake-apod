#!/bin/sh

# guake-spod.sh -- Download Astronomy Photo of the Day from apod.nasa.gov and
# set as guake terminal background.

# Created 19 Feb 2017 by Brad Eisenhauer

# Script output level definitions
verb_silent=-2
verb_error=-1
verb_normal=0
verb_verbose=1
verb_debug=2

# Output level
# TODO: make verbosity configurable from command line
verbosity=$verb_normal

# Selectively write output messages based on current output level (verbosity)
echo_lvl() {
	verb_lvl=$1
	msg=$2
	if [ $verbosity -ge $verb_lvl ]; then
		echo $msg
	fi
}

# Write message to stderr.
echo_err() {
	msg=$1
	if [ $verbosity -ge $verb_error ]; then
		>&2 echo $msg
	fi
}

# Download script output; if download is successful this will contain the
# path of the downloaded file.
dl_response=''

# Call download script
download_apod() {
	echo_lvl $verb_verbose "Downloading APOD..."

	dl_response=$(apod-dl.py)
	rc=$?

	if [ $rc -eq 0 ]; then
		echo_lvl $verb_verbose "APOD successfully downloaded to $dl_response."
	else
		echo_err "Error downloading APOD."
	fi

	return $rc
}

# Set Guake background
set_guake_bg() {
	echo_lvl $verb_verbose "Setting Guake background image..."
	echo_lvl $verb_debug "\$dl_response='$dl_response'"

	gconftool-2 -s -t string /apps/guake/style/background/image "$1"
	rc=$?

	if [ $rc -eq 0 ]; then
		echo_lvl $verb_verbose "Guake background successfullly set."
		echo_lvl $verb_normal "Visit: https://apod.nasa.gov/apod/astropix.html"
	else
		echo_err "Failed to set background."
	fi

	return $rc
}

# Add file name to APOD log
log_apod() {
	apod_path=$1
	apod_folder=$(dirname $apod_path)
	apod_file=$(basename $apod_path)
	apod_log=${apod_folder}/apod.log
	echo $apod_file >> $apod_log
}

download_apod
rc=$?
if [ $rc -eq 0 ]; then
	log_apod "$dl_response"
	set_guake_bg "$dl_response"
	rc=$?
fi
exit $rc
