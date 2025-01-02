from bs4 import BeautifulSoup
import requests
import cloudscraper
import sys
import os
from config import BASE_DIR
import re 


sys.stdout.reconfigure(encoding='utf-8')
def scrap_ps(url):
   request=cloudscraper.create_scraper()
   html_text=request.get(url).text
   soup=BeautifulSoup(html_text,'lxml')
   name=soup.find("div",class_="title").text
   problem=soup.find("div",class_="problem-statement")
   problem=problem.find_all("p")
   tags=soup.find_all("span",class_="tag-box")
   time_limit=soup.find("div",class_="time-limit").text
   memory_limit=soup.find("div",class_="memory-limit").text
   input=soup.find("div",class_="input-specification").p.text
   input = re.sub(r'\$\$\$(.*?)\$\$\$', r'\1', input)
   input = re.sub(r'\\le', '\u2264', input)  
   input = re.sub(r'\\ge', '\u2265', input)  
   input = re.sub(r'&lt;', '<', input)  
   input = re.sub(r'&gt;', '>', input)  
   output=soup.find("div",class_="output-specification").p.text
   problem_number=url.split("/")[-2]
   dir_name=f"{problem_number}{name}"
   dir=os.path.join(BASE_DIR,"data",dir_name)
   os.makedirs(dir,exist_ok=True)
   problem_dir=os.path.join(dir,"problems.txt")
   with open(problem_dir,'w',encoding="utf-8") as f:
      for p in problem:
         text=p.text
         text = re.sub(r'\$\$\$(.*?)\$\$\$', r'\1', text)
         text = re.sub(r'\\le', '\u2264', text)  
         text = re.sub(r'\\ge', '\u2265', text)  
         text = re.sub(r'&lt;', '<', text)  
         text = re.sub(r'&gt;', '>', text) 
         text = re.sub(r"\\[a-zA-Z]+", "", text)  
         f.write(text)
   metadata_dir=os.path.join(dir,"metadata.json")
   time_limit=time_limit.replace("time limit per test",'')
   memory_limit=memory_limit.replace("memory limit per test",'')

   with open (metadata_dir,'w',encoding='utf-8') as f:
      f.write("{\n")
      f.write(f"\"name\": \"{name}\",\n")
      f.write(f"\"time limit\": \"{time_limit}\",\n")
      f.write(f"\"memory\": \"{memory_limit}\",\n")
      f.write(f"\"input\": \"{input}\",\n")
      f.write(f"\"output\": \"{output}\",\n")
      f.write(f"\"tags\": [")
      f.write(", ".join([f"\"{tag.text.strip()}\"" for tag in tags]))
      f.write("]\n }")
   
if __name__ == '__main__' :
   scrap_ps("https://codeforces.com/contest/1946/problem/A")