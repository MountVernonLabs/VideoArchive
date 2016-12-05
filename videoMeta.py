from moviepy.video.io.VideoFileClip import VideoFileClip
clip = VideoFileClip("Come Back to Where it All Started-HD.mp4")
print( clip.duration )

import os.path, time
print time.strftime('%Y-%m-%d',time.gmtime(os.path.getctime("Come Back to Where it All Started-HD.mp4")))
