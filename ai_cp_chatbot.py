#!/usr/bin/env python
# coding: utf-8

# In[1]:


from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options as ChromeOptions
from webdriver_manager.chrome import ChromeDriverManager

from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from bs4 import BeautifulSoup

import os
import json
import time

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import undetected_chromedriver as uc


# In[2]:


# Set up the Chrome options for non-headless execution
# chrome_options = ChromeOptions()
chrome_options = uc.ChromeOptions()
chrome_options.add_argument('--start-maximized')  # Maximize the browser window
chrome_options.add_argument('--disable-infobars')  # Disable info bars
chrome_options.add_argument('--disable-blink-features=AutomationControlled')  # Disable automation controlled flag
chrome_options.add_experimental_option('excludeSwitches', ['enable-automation'])
chrome_options.add_experimental_option('useAutomationExtension', False)


# In[3]:


def create_chrome_options():
    # Define Chrome options
    chrome_options = uc.ChromeOptions()
    chrome_options.add_argument('--start-maximized')  # Maximize the browser window
    chrome_options.add_argument('--disable-infobars')  # Disable info bars
    chrome_options.add_argument('--disable-blink-features=AutomationControlled')  # Disable automation controlled flag
    return chrome_options


# In[4]:


def start():
    # Create new Chrome options for each session
    chrome_options = create_chrome_options()
    
    # Set up the WebDriver with undetected-chromedriver
    driver = uc.Chrome(options=chrome_options)
    return driver


# In[5]:


def indices():
    tbody=driver.find_element(By.XPATH, '//table[contains(@class, "problems")]/tbody')
    problem_indices=[td.text for td in tbody.find_elements(By.XPATH, './tr/td[1]')]
    return problem_indices


# In[6]:


def getText(element):
    nodes=element.get_property('childNodes')
    text=''
    for node in nodes:
        try:
            node_type = node['nodeType']
            node_name = node['nodeName']
            node_value = node['nodeValue']
            # print(f"Type: {node_type}, Name: {node_name}, Value: {node_value}")
            text+=(node_value)
            # print(node_value)
        except TypeError:
            if(node.tag_name=='script'):
                # print(node.get_property('innerText'))
                text+=(node.get_property('innerText'))
            elif(node.tag_name=='span'):
                text+=''
                # text+=node.get_property('innerText')
            else:
                text+=node.text
    return text


# In[22]:


ext_links=driver.find_element(By.XPATH, '//*[contains(@class, "caption titled") and contains(text(), "Contest materials")]')

try:
    tut_link=tut_element=ext_links.find_elements(By.XPATH, '//a[contains(text(), "Tutorial")]')
    print(tut_element.tag_name)
    tut_link=tut_element.get_attribute('href')
except:
    tut_element = ext_links.find_element(By.XPATH, '//a[contains(text(), "Tutorial")]/span[contains(text(), "(en)")]').find_element(By.XPATH,'..')
    print(tut_element.tag_name)
    tut_link=tut_element.get_attribute('href')

print(tut_link)


# In[23]:


def getPS(contest_id, problem_index):
    # <---Going to the link--->
    
    url = f'https://codeforces.com/contest/{contest_id}/problem/{problem_index}'
    
    driver.get(url)
    
    xpath_expression = f'//div[@class="problem-statement"]/div'
    elements=driver.find_elements(By.XPATH, xpath_expression)

    # <---Getting the link to the tutorial of the problem--->

    # ext_links=driver.find_elements(By.CLASS_NAME,'resource-locale')
    ext_links=driver.find_element(By.XPATH, '//*[contains(@class, "caption titled") and contains(text(), "Contest materials")]')

    try:
        tut_link=tut_element=ext_links.find_elements(By.XPATH, '//a[contains(text(), "Tutorial")]')
        print(tut_element.tag_name)
        tut_link=tut_element.get_attribute('href')
    except:
        tut_element = ext_links.find_element(By.XPATH, '//a[contains(text(), "Tutorial")]/span[contains(text(), "(en)")]').find_element(By.XPATH,'..')
        print(tut_element.tag_name)
        tut_link=tut_element.get_attribute('href')

    # <---Extracting Metadata and saving into a .json file--->
    
    tags=[tag.text for tag in driver.find_elements(By.CLASS_NAME,'tag-box')]
    metadata={}
    metadata['tags']=tags
    metadata['contest_id']=contest_id
    metadata['problem_index']=problem_index
    for item in elements[0].find_elements(By.XPATH,'./div'):
    
        full_text=item.get_property('innerText')
        try:
            element = item.find_element(By.XPATH,'./div')
            main_text=(element.get_property('innerText'))
            inner_text=full_text.replace(main_text,'',1)
            metadata[main_text]=inner_text
        except NoSuchElementException:
            problem_name=item.text.replace(problem_index+'. ','')
            # print("Problem Name: "+problem_name)
            metadata['problem_name']=problem_name
    
    folder_name=f"{contest_id}"
    file_name=f"metadata_{problem_index}.json"
    
    # Ensure the directory exists, if not, create it
    if not os.path.exists(folder_name):
        os.makedirs(folder_name)
    
    # Save the data as a JSON file in the specified folder
    file_path = os.path.join(folder_name, file_name)
    
    with open(file_path, "w", encoding="utf-8") as json_file:
        json.dump(metadata, json_file, indent=4)
    
    print("json file saved")
    
    try:
        # <---MAIN PS SECTION--->
        
        body=elements[1].find_elements(By.XPATH,'./*')
        
        text=[(item.text).replace('\n',' ') 
              if item.tag_name not in ['ul','ol']
              else '\n'.join(["- "+(child.text).replace('\n', ' ')
              for child in item.find_elements(By.XPATH, './*')])
              for item in body]
        text='\n'.join(text)
        problem_statement=("Problem Statement"+"\n"+text)
    
        # <---FOOTNOTE SECTION--->
    
        # footnote may not be possible
        try:
            footnote=elements[1].find_element(By.XPATH,'./div')
            footnote=footnote.find_elements(By.XPATH,'./*')
            
            # footnote=[(item.text).replace('\n',' ') for item in footnote]
            footnote=[(item.text).replace('\n',' ') 
              if item.tag_name not in ['ul','ol']
              else '\n'.join(["- "+(child.text).replace('\n', ' ')
              for child in item.find_elements(By.XPATH, './*')])
              for item in footnote]
            footnote='\n'.join(footnote)
            footnote=("Footnote"+"\n"+footnote)
        except NoSuchElementException:
            footnote="No Footnote present"
    
        # <---INPUT SECTION--->
        
        input_title=elements[2].find_element(By.XPATH,'./div').text
        input_content=elements[2].find_elements(By.XPATH,'./*')
        
        # input_content=[(item.text).replace('\n',' ') for item in input_content]
        input_content=[(item.text).replace('\n',' ') 
              if item.tag_name not in ['ul','ol']
              else '\n'.join(["- "+(child.text).replace('\n', ' ')
              for child in item.find_elements(By.XPATH, './*')])
              for item in input_content]
        input_content='\n'.join(input_content)
        
        input_=(input_title+"\n"+input_content)
    
        # <---OUTPUT SECTION--->
        
        output_title=elements[3].find_element(By.XPATH,'./div').text
        output_content=elements[3].find_elements(By.XPATH,'./*')
        
        # output_content=[(item.text).replace('\n',' ') for item in output_content]
        output_content=[(item.text).replace('\n',' ') 
              if item.tag_name not in ['ul','ol']
              else '\n'.join(["- "+(child.text).replace('\n', ' ')
              for child in item.find_elements(By.XPATH, './*')])
              for item in output_content]
        output_content='\n'.join(output_content)
        
        output=(output_title+"\n"+output_content)
    
        # <---EXAMPLE SECTION--->
        
        sample_test=elements[4].find_elements(By.XPATH,'./div/div')
        
        input_cases=sample_test[0].find_element(By.TAG_NAME,'pre').find_elements(By.XPATH,'./div')
        output_cases=sample_test[1].find_element(By.TAG_NAME,'pre')
        
        # n=no_of_test_cases
        n=int(input_cases[0].text)
        
        # n_lines=no_of_lines_in_input
        n_lines=int((len(input_cases)-1)/n)
        
        input_cases=[[line.text for line in input_cases[i:i+n_lines]] for i in range(1, len(input_cases), n_lines)]
        
        output_cases=output_cases.text.split()
        
        test_cases=str([{"input":input, "output":output} for input,output in zip(input_cases,output_cases)])
        example=(elements[4].find_element(By.XPATH,'./div').text+"\n"+test_cases)
    
        # <---NOTE SECTION--->
        
        note_title=elements[5].find_element(By.XPATH,'./div').text
        note_content=elements[5].find_elements(By.XPATH,'./*')
        
        # note_content=[(item.text).replace('\n',' ') for item in note_content]
        note_content=[(item.text).replace('\n',' ') 
              if item.tag_name not in ['ul','ol']
              else '\n'.join(["- "+(child.text).replace('\n', ' ')
              for child in item.find_elements(By.XPATH, './*')])
              for item in note_content]
        note_content='\n'.join(note_content)
        
        note=(note_title+"\n"+note_content)
    
        # <---Compiling different parts of PS into one--->
        
        final_full_problem_statement=problem_statement+"\n\n"+footnote+"\n\n"+input_+"\n\n"+output+"\n\n"+example+"\n\n"+note
    
    
        # <---Saving the .txt file--->
        
        folder_name=f"{contest_id}"
        file_name=f"problem_statement_{problem_index}.txt"
        
        # Ensure the directory exists, if not, create it
        if not os.path.exists(folder_name):
            os.makedirs(folder_name)
        
        # Save the data as a JSON file in the specified folder
        file_path = os.path.join(folder_name, file_name)
        
        with open(file_path, "w", encoding="utf-8") as file:
            file.write(final_full_problem_statement)
        
        print("txt file saved")

    except Exception as e:
        print(f"error occured - {e}")

    return tut_link
    


# In[24]:


# def getSolution1(tut_link):
#     driver.get(tut_link)
    
#     main=driver.find_element(By.XPATH, ".//div[@class='content']/div")
        
#     locate_tag = main.find_element(By.XPATH, f".//*[contains(text(), '{contest_id}{problem_index}')]").find_element(By.XPATH, '..')
    
#     # need to click the given tag so that the
#     # inside text becomes visible else
#     # it will remain hidden and can't
#     # be accessed directly by the .text method
#     # and using .get_attribute method will
#     # give us some repeated texts also which we don't want
    
#     i = 2
#     sections = {}
#     while True:
#         try:
#             # Dynamically passing the value of i in the XPath expression
#             sections[f'section_{i-1}'] = locate_tag.find_element(By.XPATH, f'following-sibling::*[{i}]').find_element(By.XPATH, './b')
            
#             # Incrementing i to move to the next sibling
#             i += 1
#         except:
#             # Break the loop if no more elements are found
#             break
    
#     contents=[]
#     for section in sections:
#         section[1].click()
#         section[1]=section[1].find_element(By.XPATH,'..')
#         try:
#             code = section[1].find_element(By.XPATH, ".//pre").find_element(By.XPATH,'./code').text
#             contents.append(code)
#         except:
#             # print(section[1].text+'\n')

#             # tut_text=(tut_text.find_element(By.XPATH,'..')).find_element(By.XPATH,'./div')
#             # sol_text=(sol_text.find_element(By.XPATH,'..')).find_element(By.XPATH,'./div')
            
#             # tut_title=tut_text.find_element(By.XPATH,'./h3').text
#             # tut_content = tut_text.find_elements(By.XPATH, "./*[not(self::h3)]")
#             # tut_content = [
#             #     (item.text).replace('\n', ' ') if item.tag_name != 'ul'
#             #     else '\n'.join(["- "+child.text.replace('\n', ' ') for child in item.find_elements(By.XPATH, './*')])
#             #     for item in tut_content
            
#             _content=section[1].text+'\n'
#             content=(section[1].find_element(By.XPATH,'following-sibling::*[1]')).find_elements(By.XPATH, "./*[not(self::h3 or self::h4)]")
#             content=[
#                 (item.text).replace('\n', ' ') if item.tag_name not in ['ul','ol']
#                 else '\n'.join(["- "+child.text.replace('\n', ' ') for child in item.find_elements(By.XPATH, './*')])
#                 for item in content
#             ]
#             try:
#                 title=(section[1].find_element(By.XPATH,'following-sibling::*[1]')).find_element(By.XPATH, "./h3 | ./h4").text
#                 _content+=('\n\n'.join([title, ('\n\n'.join(content))]))
#             except:
#                 _content+='\n\n'.join(content)+'\n'
            
#             # print(_content)
#             contents.append(_content)
    
#     _content='\n\n'.join(contents)
#     print(_content)


# In[25]:


def getSolution1(tut_link):
    driver.get(tut_link)
    
    # Find the main content of the page
    main = driver.find_element(By.XPATH, ".//div[@class='content']/div")
    
    # Locate the tag based on contest_id and problem_index
    locate_tag = main.find_element(By.XPATH, f".//*[contains(text(), '{contest_id}{problem_index}')]").find_element(By.XPATH, '..')
    
    # Need to click the given tag so that the inside text becomes visible else
    # it will remain hidden and can't be accessed directly by the .text method
    # and using .get_attribute method will give us some repeated texts also which we don't want
    
    i = 2
    sections = {}
    
    # Loop to find all sections dynamically
    while True:
        try:
            # Dynamically passing the value of i in the XPath expression
            sections[f'section_{i-1}'] = locate_tag.find_element(By.XPATH, f'following-sibling::*[{i}]').find_element(By.XPATH, './b')
            
            # Incrementing i to move to the next sibling
            i += 1
        except:
            # Break the loop if no more elements are found or any exception occurs
            # print(f"Error: {e}")
            break
    
    contents = []
    
    # Iterate over sections and extract content
    for section_key, section_value in sections.items():
        section_value.click()  # Click the section to make it visible
        section_value = section_value.find_element(By.XPATH, '..')  # Move to the parent of the clicked element
        
        try:
            # Extract code from the section if available
            code = section_value.find_element(By.XPATH, ".//pre").find_element(By.XPATH, './code').text
            contents.append(code)
        except:
            # If no code is found, handle the content extraction
            # print(f"Error extracting code for {section_key}: {e}")
            
            # Get the content excluding h3 and h4 tags
            _content = section_value.text + '\n'
            content = (section_value.find_element(By.XPATH, 'following-sibling::*[1]')).find_elements(By.XPATH, "./*[not(self::h3 or self::h4)]")
            content = [
                (item.text).replace('\n', ' ') if item.tag_name not in ['ul', 'ol']
                else '\n'.join(["- " + child.text.replace('\n', ' ') for child in item.find_elements(By.XPATH, './*')])
                for item in content
            ]
            
            try:
                # Try to get title from h3 or h4, whichever exists
                title = (section_value.find_element(By.XPATH, 'following-sibling::*[1]')).find_element(By.XPATH, "./h3 | ./h4").text
                _content += ('\n\n'.join([title, ('\n\n'.join(content))]))
            except:
                # If no title found, just append content
                _content += '\n\n'.join(content) + '\n'
            
            # Append the extracted content to the contents list
            contents.append(_content)
    
    # Join the contents from all sections and print
    final_content = '\n\n'.join(contents)
    print(final_content)


# In[26]:


def getSolution2(i,tut_link):
    driver.get(tut_link)
    
    loctag=driver.find_element(By.CLASS_NAME,'ttypography')
    # lst[-1].get_property('childNodes')
    e=loctag.find_element(By.XPATH,f'./div[contains(@class, "spoiler")][{i}]')
    lst=[]
    lst.append(e)
    while(e.find_element(By.XPATH,'preceding-sibling::*[1]').get_attribute('class')!='spoiler' and e.tag_name not in ['h3','h4']):
        e=e.find_element(By.XPATH,'preceding-sibling::*[1]')
        lst.append(e)
        if(e.tag_name in ['h3','h4']):
            break
    lst
    lst.reverse()
    # print(e.find_element(By.XPATH,'.//pre').find_element(By.XPATH,'./code').get_attribute('innerText'))
    # e.find_elements(By.XPATH,'preceding-sibling::*')
    
    content=[(getText(item)).replace('\n',' ')
            if item.tag_name not in ['ul','ol']
            else '\n'.join(["- "+(getText(child)).replace('\n', ' ')
            for child in item.find_elements(By.XPATH, './*')])
            for item in lst]
    
    text='\n\n'.join(content)
    
    if(lst[-1].find_element(By.XPATH,'.//pre').find_element(By.XPATH,'./code')):
        text+=('\n'+(lst[-1].find_element(By.XPATH,'.//pre').find_element(By.XPATH,'./code')).get_attribute('innerText'))
    
    print(text)


# In[27]:


def getCodes(indices):
    i=1
    loctag=driver.find_element(By.CLASS_NAME,'ttypography')
    while True:
        try:
            print("Problem "+indices[i])
            print((((loctag.find_element(By.XPATH,f'./div[contains(@class, "spoiler")][{i}]')).find_element(By.XPATH,'.//pre')).find_element(By.XPATH,'./code')).get_attribute('innerText'))
            print('\n')
            i+=1
        except:
            print("no more codes")
            break


# In[28]:


contest_id=2048
url = f'https://codeforces.com/contest/{contest_id}'


# In[13]:


driver=start()


# In[30]:


driver.get(url)


# In[31]:


problem_indices=indices()
problem_indices


# In[32]:


for problem_index in problem_indices:
    # problem_index=problem_indices[5]
    tut_link=getPS(contest_id, problem_index)
    # for i in range(len(problem_indices)):
    #     problem_index=problem_indices[i]
    #     tut_link=getPS(contest_id, problem_index)
        # print(tut_link)
        # print('\n\n')
        # getSolution(tut_link)
    tut_link

    try:
        getSolution1(tut_link)
    except Exception as e:
        # print(f"error occurred - {e}")
        try:
            i=problem_indices.index(problem_index)
            getSolution2(i, tut_link)
        except:
            # print(f"error occurred - {e}")
            pass


# In[34]:


# def extract_text_recursively(element, depth=0):
#     text = ''
#     if element.tag_name:  # Check if the element has a tag name
#         text += ' ' * depth + (element.text.strip() + '\n')
#         children = element.find_elements(By.XPATH, './*')
#         for child in children:
#             text += extract_text_recursively(child, depth + 1)
#     return text

# def extract_text_from_html():
#     # driver.get(url)
#     body = driver.find_element(By.CLASS_NAME, 'ttypography')
#     return extract_text_recursively(body)


# In[35]:


# def getSolution(tut_link):

#     driver.get(tut_link)
    
#     main=driver.find_element(By.XPATH, ".//div[@class='content']/div")
    
#     locate_tag=(main.find_element(By.XPATH, f".//*[contains(text(), '{contest_id}{problem_index}')]")).find_element(By.XPATH,'..')
    
#     # need to click the given tag so that the
#     # inside text becomes visible else
#     # it will remain hidden and can't
#     # be accessed directly by the .text method
#     # and using .get_attribute method will
#     # give us some repeated texts also which we don't want
    
#     tut_text=(locate_tag.find_element(By.XPATH,'following-sibling::*[2]')).find_element(By.XPATH,'./b')
#     sol_text=(locate_tag.find_element(By.XPATH,'following-sibling::*[3]')).find_element(By.XPATH,'./b')
    
#     tut_text.click()
#     sol_text.click()
    
#     tut_text=(tut_text.find_element(By.XPATH,'..')).find_element(By.XPATH,'./div')
#     sol_text=(sol_text.find_element(By.XPATH,'..')).find_element(By.XPATH,'./div')
    
#     tut_title=tut_text.find_element(By.XPATH,'./h3').text
#     tut_content = tut_text.find_elements(By.XPATH, "./*[not(self::h3)]")
#     tut_content = [
#         (item.text).replace('\n', ' ') if item.tag_name != 'ul'
#         else '\n'.join(["- "+child.text.replace('\n', ' ') for child in item.find_elements(By.XPATH, './*')])
#         for item in tut_content
#     ]
    
#     tut = '\n\n'.join([tut_title, ('\n'.join(tut_content))])
#     print(tut)
#     print('\n\n')
#     sol_content = sol_text.find_element(By.XPATH, ".//code").text
#     print(sol_content)


# In[ ]:


driver.quit()

