#!/usr/bin/python3
import sys
import urllib3
from bs4 import BeautifulSoup

'''
arguments should look like these:
\
source_url = 'https://mycourses.aalto.fi/course/view.php?id=24335&section=5'
module_name = 'MachineLearningBasicPrinciple_CS-E3210_'
destination = 'F://WorkSpaces//ScrapingPDF//Lectures//'
'''

source_url = sys.argv[1]
module_name = sys.argv[2]
destination = sys.argv[3]

print ('download from ' + sys.argv[1] + ', Module: ' +  sys.argv[2])
print ('download to ' + sys.argv[3])

http = urllib3.PoolManager()
response = http.request('GET', source_url)
soup = BeautifulSoup(response.data, 'html.parser') # parsing the website	

# grabs each documents
containers = soup.findAll('ul', {'class':'section img-text'})
lectures_containers = containers[0].findAll('li') 	

# retrieving all lecture Urls
all_lecture_urls = []
for lecture in lectures_containers:
    all_lecture_urls.append(lecture.a.attrs['href'])
    
# download to destination
for i, each_url in enumerate(all_lecture_urls):
    filedata = http.request('GET', each_url, preload_content=False)
    with open((destination + module_name + str(i+1) + '.pdf'), "wb") as file:
        data = filedata.read()
        file.write(data)
        file.close()
    print('Downloaded : %i / %i' % (i+1, len(all_lecture_urls)))
        
print('Done')