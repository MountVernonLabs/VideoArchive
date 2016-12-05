import tinys3
s3conn = tinys3.Connection('S3_ACCESS_KEY','S3_SECRET_KEY',tls=True)
s3bucket = "YOUR BUCKET"

import pymysql.cursors
import pymysql

# My SQL database connection
connection = pymysql.connect(host='YOUR_MYSQL_HOST',
                             user='YOUR_USER',
                             password='YOUR_PASSWORD',
                             db='YOUR_DATABASE',
                             charset='utf8mb4',
                             cursorclass=pymysql.cursors.DictCursor)
