
# coding: utf-8

# In[ ]:

#from urllib.request import urlopen
import bs4 
import requests
import pandas as pd
from pandas import DataFrame
import csv


# In[2]:

resume=[] #list to store all the links of resume
for i in range(2):
    #url which we need to parse
    URL = "https://www.indeed.com/resumes?q=java&co=US&cb=jt&start={}".format(i*50)
    page = requests.get(URL) #get the URL
    soup = bs4.BeautifulSoup(page.text, 'html.parser') #parse the url
    #Collecting links of resumes
    for link in soup.find_all('a'):
           if link.attrs['href'][:3] in ['/r/','/me']:
                cutPoint = link.attrs['href'].find('?sp=0')
                resume.append('http://www.indeed.com'+link.attrs['href'][:cutPoint])
print (len(resume)) #checking if 100 resume links are stored in the list


# In[3]:

data = [] # a global list which will have all the details

#Get the name, work and education details
for i in resume:
    #parsing the resume links
    source_candidate = requests.get(i)
    candidate = bs4.BeautifulSoup(source_candidate.text, 'html.parser')

    #store the names
    names = [heading.text for heading in candidate.find_all('h1')]
               
    #work details
    
    work_title = [titles.text for titles in candidate.find_all('p', class_='work_title')]
                  
    work_company = [comp.text for comp in candidate.find_all('div', class_='work_company')]
    
    work_date = [dates.text for dates in candidate.find_all('p', class_='work_dates')]
        
    #education details    
    
    edu_title = [edu.text for edu in candidate.find_all('p', class_='edu_title')]               
        
    edu_school = [schools.text for schools in candidate.find_all('div', class_='edu_school')]
    
    #List to store a single resume detail
    
    line = [] 
    
    line = [i for i in names]
    
    #Appending work fields 
    ch = 0 #counter to count index in line
    if len(work_title)>0 or len(work_company)>0 or len(work_date)>0:
        for i in range(5):
                if i<len(work_title):line.append(work_title[i])
                else:line.append('NIL')
                if i<len(work_company):line.append(work_company[i])
                else:line.append('NIL')
                if i<len(work_date):line.append(work_date[i])
                else:line.append('NIL')
                ch+=3
                
    for i in range(15-ch): line.append('NIL') #Append NIL for remaining fields
        
    #Appending education fields
    ch = 0 #resetting counter to 0 to count index in line  
    if len(edu_title)>0 or len(edu_school)>0: 
        for i in range(2):
            if i<len(edu_title):line.append(edu_title[i])
            else:line.append('NIL')
            if i<len(edu_school): line.append(edu_school[i])
            else:line.append('NIL')
            ch+=2
            
    for i in range(4-ch): line.append('NIL') #Append NIL for remaining fields
            
    data.append(line)#store details of 100 resumes globally


# In[4]:

with open('C:/Users/rimo/Desktop/Indeed_Resumes.csv', 'w', encoding='utf-8') as fp: # Opening the .csv file that is created
    a = csv.writer(fp, delimiter=',')  # opening the stream and specifying that ',' is the delimiter
    a.writerows(data) # Now finally writing all the details present in list(data) to the file


# In[5]:

#store column names
u_cols = ['Name', 
          'Designation1', 'Company1', 'Start-end dates1', 
          'Designation2', 'Company2', 'Start-end dates2', 
          'Designation3', 'Company3', 'Start-end dates3', 
          'Designation4', 'Company4', 'Start-end dates4',
          'Designation5', 'Company5', 'Start-end dates5', 
          'Edu_Degree1', 'Edu_School1',
          'Edu_Degree2', 'Edu_School2']

users = pd.read_csv('C:/Users/rimo/Desktop/Indeed_Resumes.csv', sep=',', names=u_cols) #read the csv file

users # Table is displayed.

