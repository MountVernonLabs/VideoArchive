import os.path, time, sys, tinys3
import config as cfg

# Get the clip durration using moviepy
from moviepy.video.io.VideoFileClip import VideoFileClip
clip = VideoFileClip(sys.argv[1])
durration = clip.duration

# Get date created (format in MySQL date format)
created = time.strftime('%Y-%m-%d',time.gmtime(os.path.getctime(sys.argv[1])))

# File name (passed in as first argument)
filename = sys.argv[1]

# Get the file prefix to use as an ID
prefix = os.path.splitext(sys.argv[1])[0]

# Upload to S3
print "Uploading to S3"

f = open(sys.argv[1]+'_sheet.jpg','rb')
cfg.s3conn.upload(sys.argv[1]+'_sheet.jpg',f,cfg.s3bucket)

f = open(sys.argv[1]+'_thumb.jpg','rb')
cfg.s3conn.upload(sys.argv[1]+'_thumb.jpg',f,cfg.s3bucket)

f = open(sys.argv[1]+'_thumb.gif','rb')
cfg.s3conn.upload(sys.argv[1]+'_thumb.gif',f,cfg.s3bucket)

thumbnail = '//s3.amazonaws.com/mtv-videoarchive/'+sys.argv[1]+'_thumb.jpg'
sheet = '//s3.amazonaws.com/mtv-videoarchive/'+sys.argv[1]+'_sheet.jpg'
gif = '//s3.amazonaws.com/mtv-videoarchive/'+sys.argv[1]+'_thumb.gif'

with open(sys.argv[1]+'.txt', 'r') as myfile:
    transcript=myfile.read()

# Insert record in database
print "Writing to database"

try:
    with cfg.connection.cursor() as cursor:
        # Create a new record
        sql = "INSERT INTO `mv_videoarchive` (`object`, `produced`, `thumbnail`, `length`, `sheet`, `gif`, `transcript`) VALUES (%s, %s, %s, %s, %s, %s, %s)"
        cursor.execute(sql, (prefix, created, thumbnail, durration, sheet, gif, transcript))

    # connection is not autocommit by default. So you must commit to save
    # your changes.
    cfg.connection.commit()

finally:
    cfg.connection.close()
