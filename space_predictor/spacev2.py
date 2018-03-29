import requests
import threading

#File_Addrs = 'user_data/links/data.project-gxs.com.final/crawled.txt'   # The address of file containing urls
File_Addrs = 'links'      # For testing Purpose

# Initialization
List_Of_URLs = []
List_Of_Invalid_URLs = []
Total_Size = 0
Processed_URLs = 0
Times_Looped = 0
Max_retries = 3
Progress = 0

# Preprocessing
with open(File_Addrs,'r') as f: # Loading uls into list for faster access
    List_Of_URLs = list(set(f.read().splitlines()))    # Removing duplicates
    Total_URLs = len(List_Of_URLs)  # Total number of links
    print("Total Number of URLs to process : {}".format(Total_URLs))

Rate = 100/Total_URLs

# Return the given bytes as a human friendly KB, MB, GB, or TB string'
def HumanReadableSize(B):
   B = float(B)
   KB = float(1024)
   MB = float(KB ** 2) # 1,048,576
   GB = float(KB ** 3) # 1,073,741,824
   TB = float(KB ** 4) # 1,099,511,627,776

   if B < KB:
      return '{0} {1}'.format(B,'Bytes' if 0 == B > 1 else 'Byte')
   elif KB <= B < MB:
      return '{0:.2f} KB'.format(B/KB)
   elif MB <= B < GB:
      return '{0:.2f} MB'.format(B/MB)
   elif GB <= B < TB:
      return '{0:.2f} GB'.format(B/GB)
   elif TB <= B:
      return '{0:.2f} TB'.format(B/TB)
