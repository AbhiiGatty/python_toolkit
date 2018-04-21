import requests

#File_Addrs = 'user_data/links/data.project-gxs.com.final/crawled.txt'   # The address of file containing urls
File_Addrs = 'links'      # For testing Purpose

# Initialization
List_Of_URLs = []
List_Of_Invalid_URLs = []
Total_Size = 0
Processed_URLs = 0
Retry_Num = 0
Max_Retries = 3
Progress = 0

# Preprocessing
with open(File_Addrs,'r') as f: # Loading URLs into list for faster access
    List_Of_URLs = list(set(f.read().splitlines()))    # Removing duplicates
    Total_URLs = len(List_Of_URLs)  # Total number of links

Rate = 100/Total_URLs

# Return the given bytes as a human friendly KB, MB, GB, or TB string
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

# Main fuction to gather info about url
def grab_info(list_Of_URLs):
    global Total_Size, Processed_URLs, Total_URLs, Progress, Rate  # Accessing global variables
    global List_Of_Invalid_URLs
    List_Of_Invalid_URLs = []
    for url in list_Of_URLs:
        if url not in [' ','']:      # Ignoring any whitespaces within the list
            try:
                File_Size = int(requests.get(url, stream=True).headers['Content-length'])
                Progress += Rate
                Processed_URLs = Processed_URLs + 1
                Total_Size += File_Size
                print('URLs Done:{0}/{1} File Size:{2} Total Size:{3} Progress:{4:.2f}%'.format(Processed_URLs, Total_URLs, HumanReadableSize(File_Size), HumanReadableSize(Total_Size), Progress))
                
            except requests.exceptions.ConnectionError as err:
                print(err)
            except requests.exceptions.HTTPError as err:
                print(err)
            except KeyboardInterrupt:
                print("Killing Program...")
                exit(0)
            except:
                List_Of_Invalid_URLs.append(url)
                print('invalid')

grab_info(List_Of_URLs)

while len(List_Of_Invalid_URLs) > 0:
    print("\nTotal unprocessed/invalid URLs: {}\n".format(len(List_Of_Invalid_URLs)))
    if Retry_Num < Max_Retries:
        Retry_Num += 1
        print("*******Retrying unprocessed URLs {}/3*******\n".format(Retry_Num))
        grab_info(List_Of_Invalid_URLs)
    else:
        break

# Final Report 
print("******Final Diagnostic Report******")
print("Total no. of URLs: {0} Processed URL rate: {1:.2f}%".format(Total_URLs, Progress))
print("Total no. of Invalid URLs: {}".format(len(List_Of_Invalid_URLs)))
print("Total size of {}/{} links is: {}".format(Processed_URLs,Total_URLs,HumanReadableSize(Total_Size))) 
