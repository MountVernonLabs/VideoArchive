# VideoArchive
Creates a web-based tool to organize video files into an archive with tagging and contact sheet functionality.  Imports data into a MySQL database ready for a BigTreeCMS module.

# What it does
- Reads in a list of video files
- Generates a contact sheet every 15 seconds of the video
- Generates a thumbnail (both static and animated GIF)
- Provides an automated transcription using cmu-sphinx
- Writes records to a MySQL database

# Install
- Clone repository
- Edit config.py (use sample file), add your MySQL database connections and your AWS S3 bucket details
- import ./sql/import.sql into your database to create the necessary table
- Run sh process.sh to kick off the task

# Still to do
- BigTreeCMS module integration

# Dependancies
- FFMpeg
- ImageMagick
- MySQL
- ghostscript
- Python (with libraries: MoviePy, tinys3, pymysql)
- cmu-sphinx


# Thanks To
@melmatsuoka for the video contact sheet script
https://gist.github.com/melmatsuoka/b87c4dc9374c52827582
