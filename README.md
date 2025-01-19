<<<<<<< HEAD
The file aims to scrape problem details, including the problem statement and editorial content, 
from Codeforces problem pages or contests. It saves the extracted data into text and JSON files for later use.

First we create all the required directories where we are going to store problem statements,editorial,metadata then when contest link is provided 
we will first extract links to all the problems in the context and then extract individual details of each problem in the next step
when problem link is provided The function find_question_details is called and we extract info starting from
title of the question in the link then the problem statement and Also storing all other data like time,memory limits,problem id like 'A' or 'B' ..etc also contest id
input and output specifications and testcases , problem tags ,difficulty.When doing this some content got repeated(
because it was present twice in the html once as math then other inside some elements like 'div' )
which i overcame by using code -for span in soup.find_all("span", {"class": "math"}): span.decompose() which removed the terms which
caused the duplication.

Then coming to the editorial content , to navigate to the editorial page we should first find the link to editorial
in the page then we open it.But on the contest page or the problem there may be many links to tutorials,editorial,video tutorials etc
depending on the contest and each may be in a different language so first after finding all those ,I iterated
to find the editorial I need from all of them, which is English and provided it is not a video tutorial , also sometimes it is just mentioned as
tutorial on some pages so in above case if I don't get any result then I will use this one.

Now we are on editorial page which contains solutions to all the problems of the contest here I want the 
editorial of problems, which I know as previously we processed all details of the problem so We know
the title of the problem I stored them all in a list(giving it as an argument to the function). so First we again locate the place where the title of the current element matches
with our current problem's name(starting from first one in the list of problems) then we extract all the hints ,solution,codes or implementations provided below it till
we encounter the next problem or reach the end of the editorial then we write this editorial content into a file because we found the next 
problem and the present problem's editorial is done and even here we will use for span in soup.find_all("span", {"class": "math"}): span.decompose() 
so that there is no duplication in terms . Sometimes there were names of authors and 
solution writer's mentioned in either a 'p' or 'h' but definitely not a 'div' so I skipped all those after I
found the problem name.
=======
# chatbot_gdg
>>>>>>> b023213ae47d42ab47fbfdca84cf3c7ff663d908
