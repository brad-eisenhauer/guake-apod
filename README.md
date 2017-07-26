# guake-apod
Script to download current [Astronomy Photo of the Day](https://apod.nasa.gov/apod/astropix.html)
and set it as [Guake](http://guake-project.org/) terminal background.

## apod-dl.py
This script downloads the current Astronomy Photo of the Day from apod.nasa.gov
if it is an image (not video) and if the image to be downloaded does not already
exist. Images are downloaded to `~/Pictures/apod`, which must aleady exist. The
script writes the full path of the downloaded image to standard output for
consumption by `guake-apod.sh`.

## guake-apod.sh
This script runs `apod-dl.py`, reading the output. If the download is successful,
it appends the file name to the log (`apod.log`) in the same folder as the
downloaded image. It then proceeds to set the image as the Guake terminal
background via `gconftool-2`.

## Requirements
* Python
* gconftool
* `~/Pictures/apod` directory must exist.

## License
Take it. Do whatever. Knock yourself out.
