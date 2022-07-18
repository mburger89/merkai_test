# Meraki take home test

## Install
    This project uses pipenv to manage depences.
    get it by doing `brew install pipenv` (if on a mac) or `pip install pipenv`.
    Then you can just run pipenv install at the root of the project.

    if you prefer to do it a different way you can refer to the  Pipfile for dependencies

## Running the test
```
    python test.py -key < api key >
```
results will be found in a results folder `/results`

## Thinking behind the test
Thinking was to test the websites functionality by having:
- the script attempt to login
- check number of devices  
- click on each of the links 
- check that the dynamic data like "clients" and "usage" where being displayed

I decided to test these points as in my experience these are some things that commonly break.imparticularly the dynamic data can fail to render or load so it is import to ensure its there as expected. I didn't check for the usage as it is part of the same request obeject so it would just be duplicative. I will say that typically I would meet with the team or individual who built the web app or service before I start writing anything and go over what are some parts that they are concerned about and think may need testing. Then I would tell them what I think could use testing and really try to make it more of collaberative effort on the test plan for that service. 

I chose to write these tests in a way to enabled me to ouput a json object of the results that could be parsed by a web frontend or other client.
This is how I typically do testing as I typically need to create a frontend to display results for less techinical people than myself. 
I have also writen testing using various testing frameworks like pytest, but I have not done it like that in a while cause most in most situation I have been in there is a need for a UI that can easily display the results to a non-technical user. So how its done is not as crucail as being able to injest those results and display them in a friendly UI. I decided to use python selenium for this testing as it is an industry standard and I am most familar with it.

