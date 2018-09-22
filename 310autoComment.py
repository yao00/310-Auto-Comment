''' Author: yao@alumni.ubc.ca
	Requirement: install pyGithub and python3
	Function: comment gitHub commit at a certain time until getting a non-waiting response'''

from github import Github
from datetime import datetime
from threading import Timer
import time

#replace with your own gitHub token
access_token = "replace with your own access_token"
msg = "@autobot #d0"
waitMin = 5
organization = "CPSC310-2018W-T1"
repo_name = "replace with your own repo_name"

# Enterprise with custom hostname
g = Github(base_url="https://github.ugrad.cs.ubc.ca/api/v3", login_or_token = access_token)

def atAutobot():
	# always get the 1st commit of the list
	latest_commit = g.get_organization(organization).get_repo(repo_name).get_commits()[0];
	print(latest_commit.url)
	print(latest_commit.commit.message)
	latest_commit.create_comment(msg)

	# data is processing
	while (latest_commit.get_comments()[0].body == msg):
		print("waiting for response, the time is ",datetime.today())
		time.sleep(60*3)

	# to avoid failure in edge cases in time stamps, send a request every waitMin
	while(latest_commit.get_comments()[latest_commit.get_comments().totalCount-1].body[0:13] == "You must wait"):
		print("at autobot again, the time is ",datetime.today())
		time.sleep(60*waitMin) 
		latest_commit.create_comment(msg)
	print(latest_commit.get_comments()[latest_commit.get_comments().totalCount-1].body)
	#print(latest_commit.get_comments()[latest_commit.get_comments().totalCount-1].body)

x=datetime.today()
y=x.replace(day=x.day+1, hour=19, minute=23, second=00, microsecond=0)
delta_t=y-x
secs=delta_t.seconds+1

t = Timer(secs, atAutobot)
t.start()
