import os.path, time, sys, tinys3
import config as cfg

# Get the clip durration using moviepy
from moviepy.video.io.VideoFileClip import VideoFileClip
clip = VideoFileClip(sys.argv[1])
print( clip.duration )

# Get date created (format in MySQL date format)
print time.strftime('%Y-%m-%d',time.gmtime(os.path.getctime(sys.argv[1])))

# File name (passed in as first argument)
print sys.argv[1]

# Get the file prefix to use as an ID
print os.path.splitext(sys.argv[1])[0]

# Retrieves value from external config file
print cfg.test
