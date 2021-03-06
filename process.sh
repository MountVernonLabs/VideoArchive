#!/bin/bash
#
# Generates thumbnail contact sheets of all video files in current working directory.
#
# Script defaults to writing PNG contact sheets to the same folder, using the original
# video filename as the basename for the contact sheet
#
# More details: https://trac.ffmpeg.org/wiki/Create%20a%20thumbnail%20image%20every%20X%20seconds%20of%20the%20video
#
# NOTE: 'montage' requires that Ghostscript be installed, in order to be able to generate titles
# on the contact sheet: run 'brew install ghostscript' to install


function cleanup () {

	rm -rf .snapshots/*
}

SNAPSHOT_INTERVAL="15" # time interval (in seconds) to grab each frame


if [ ! -d ".snapshots" ] # check for existence of screengrab temp folder in CWD
  then mkdir .snapshots
fi

shopt -s nocaseglob 	# forces case insensitive extension globbing in the following for loop

for FILE in *.{wmv,avi,rm,ram,mpg,mpeg,mov,mp4,flv,asf,mkv,m4v};

	do [ -e "$FILE" ] || continue;

		trap cleanup SIGHUP SIGINT SIGTERM
		# extract thumbnail frames every $SNAPSHOT_INTERVAL seconds. By telling FFmpeg to set the output files FPS option to
		# a very low value, we made FFmpeg drop a lot of frames at the output, in order to achieve such a low frame
		# rate, effectively having our thumbnails generated every X seconds
		#
		# thumbnails are written to a hidden .snapshots temp folder in the same folder the script was run in.

		echo "------------------------------------------------"
		echo "\nExtracting thumbnails for \"${FILE}\""
		ffmpeg -loglevel warning -i "${FILE}" -f image2 -vf fps=fps=1/$SNAPSHOT_INTERVAL .snapshots/._"${FILE}"_%03d.png 2> /dev/null

		# assemble the contact sheet, using ImageMagick's "montage" util

		echo "Compiling contact sheet for \"${FILE}\""
		montage .snapshots/"._${FILE}"_*.png -tile 4 -geometry 240x153 -title "${FILE}" "${FILE}_sheet.jpg" 2> /dev/null

		echo "Creating master thumbnail for \"${FILE}\""
		ffmpeg -i "${FILE}" -ss 00:00:10.000 -s 240x153 "${FILE}"_thumb.jpg 2> /dev/null

		echo "Creating animated GIF thumbnail for \"${FILE}\""
		ffmpeg -ss 00:00:00.000 -i "${FILE}" -pix_fmt rgb24 -r 1 -s 240x153 -t 00:00:30.000 "${FILE}"_thumb.gif 2> /dev/null

		# Create the transcript
		echo "Transcribing \"${FILE}\""
		ffmpeg -i "${FILE}" -ar 16000 -ac 1 file.wav 2> /dev/null
		pocketsphinx_continuous -infile file.wav -logfn /dev/null > "${FILE}".txt
		rm *.wav

		# purge the temporary .snapshots folder

		echo "Cleaning up tempfiles...\n"
		rm -f .snapshots/._"${FILE}"_*.png

		# trigger the upload to the database
		python videoMeta.py "${FILE}"

		# clean up the generated files and original source video
		rm *.jpg
		rm *.gif
		rm *.txt
		rm "${FILE}"

	done
