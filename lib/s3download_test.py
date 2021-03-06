import sys
import time

sys.path.append('s3downloader')

import s3downloader  
 
    
#main

ncep3_files = ["s3://hdfdata/ncep3/GSSTF_NCEP.3.1987.07.01.he5",
"s3://hdfdata/ncep3/GSSTF_NCEP.3.1987.07.02.he5",
"s3://hdfdata/ncep3/GSSTF_NCEP.3.1987.07.03.he5",
"s3://hdfdata/ncep3/GSSTF_NCEP.3.1987.07.04.he5"]

s3downloader.init()


nspace = s3downloader.freespace()
print("free space:", nspace)
usedspace = s3downloader.usedspace()
print("used space:", usedspace)

print("preloaded files:")
downloads = s3downloader.getFiles(s3uri_prefix="s3://hdfdata/")
for download in downloads:
    print(download)

print("clearing..")
s3downloader.clear()

usedspace = s3downloader.usedspace()
#print("used space", usedspace)

#s3download.addFiles(ncep3_files)
#s3download.addFiles("s3://hdfdata/ncep3/")

s3downloader.addFiles("s3://hdfdata/ncep3/")
output = s3downloader.dump()

downloads = s3downloader.getFiles(state="PENDING")
print("pending files:")
print(downloads)

downloads = s3downloader.getFiles(s3uri_prefix="s3://hdfdata/")
print("all files:")
print(downloads)

#output = s3download.s3cmdls("s3://hdfdata/ncep3/")
print(output)
 
count = s3downloader.start()
while count > 0:
    count = s3downloader.update()
    print("count:", count)
    time.sleep(1)
    
    
# get list of downloaded addFiles
print("downloads:")
downloads = s3downloader.getFiles()
for filepath in downloads:
    print(filepath)
print("done!")




    
     
     
  
