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
print cfg.s3bucket

# Upload to S3
print "Uploading to S3"

f = open(sys.argv[1]+'_sheet.png','rb')
cfg.s3conn.upload(sys.argv[1]+'_sheet.png',f,cfg.s3bucket)

f = open(sys.argv[1]+'_thumb.png','rb')
cfg.s3conn.upload(sys.argv[1]+'_thumb.png',f,cfg.s3bucket)
