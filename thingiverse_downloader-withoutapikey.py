# -*- coding: utf-8 -*-

import requests
import json
import sys
import argparse
import os.path
import re
from collections import OrderedDict

#Go to https://www.thingiverse.com/apps/create and select Desktop app then either save it in the variable "api_token" below or save in apikey.txt in same folder

api_token="Insert API token here" 




def loadData(fileName,fileType):
    #Load the data from the file to a list
    if os.path.isfile(fileName):
        file=open(fileName,"r")
        loadedData = file.readlines()
        file.close()
        # Removing \n
        loadedData = [x.strip() for x in loadedData]
        return loadedData
    else:
        print(fileType + " file not Found at " + os.path.abspath(fileName))
        sys.exit()

def download_objects(rest_url, file_name):

    # r = requests.get(rest_url)
    s = requests.Session() #It creates a session to speed up the downloads
    r=s.get(rest_url)
    data=r.json()

    #Save the data
    file=open(json_path+"/"+file_name,"wb")
    file.write(json.dumps(data, indent=4, sort_keys=True,ensure_ascii=False).encode('utf8'))
    file.close()

    #Reading the json file
    file=open(json_path+"/"+file_name,"r")
    data_pd=json.loads(file.read())

    #The page has objects?
    if (len(data_pd)==0):
        print("\n\nNo more pages, exiting current operation")
        return True

    #Is it an error page?
    for n in data_pd:
        if (n=="error"):
            print("\n\nFound Error page, exiting current operation")
            return True

    print("Downloading {} objects from thingiverse".format(len(data_pd)))

    for object in range(len(data_pd)):

        object_id=str(data_pd[object]["id"])
        print("\n{} -> {}".format(data_pd[object]["name"],data_pd[object]["public_url"]))

        thing_name = data_pd[object]["name"].replace("/","-").replace(":"," -").replace("\"","").replace("\"#","").replace("*","").replace("<","").replace(">","")
        thing_name = re.sub('[!@#$?.]', '', thing_name)
        thing_name = re.sub("^\s+|\s+$", "", thing_name)
        file_path = stl_path+"/"+data_pd[object]["creator"]["name"]+"/"+thing_name

        if not os.path.exists(file_path):
            os.makedirs(file_path)
        else:
            print("\nSkipping already downloaded object")
            continue

        #User name
        print("{} {}".format(data_pd[object]["creator"]["first_name"],data_pd[object]["creator"]["last_name"]))

        #Get file from a things
        r=s.get(thingiverse_api_base+rest_keywords["things"]+object_id+rest_keywords["files"]+access_keyword+api_token)
        files_info=r.json()

        for file in range(len(files_info)):
            print("    "+files_info[file]["name"])
            #Download the file
            download_link=files_info[file]["download_url"]+access_keyword+api_token
            try:
                r = s.get(download_link)
            except:
                print("Problem with download")
                errorList.append(str(download_link))

            with open(file_path+"/"+files_info[file]["name"], "wb") as code:
                code.write(r.content)

def newest(n_pages=1):
    for index in range(n_pages):
        print("\n\nPage: {}".format(index+1))
        rest_url=thingiverse_api_base+rest_keywords["newest"]+access_keyword+api_token+rest_keywords["pages"]+str(n_pages)
        if(download_objects(rest_url,"newest.json")==True):
            return

def user(username,n_pages=1):
    #/users/{$username}/things
    for index in range(n_pages):
        print("\n\nPage: {}".format(index+1))
        rest_url=thingiverse_api_base+rest_keywords["users"]+username+rest_keywords["things"]+access_keyword+api_token+rest_keywords["pages"]+str(index+1)
        print(thingiverse_api_base+rest_keywords["users"]+username+rest_keywords["things"]+access_keyword+"Hiding API token"+rest_keywords["pages"]+str(index+1))
        if(download_objects(rest_url,str(username+".json"))==True):
            return

def likes(username,n_pages=1):
    #/users/{$username}/things
    for index in range(n_pages):
        print("\n\nPage: {}".format(index+1))
        rest_url=thingiverse_api_base+rest_keywords["users"]+username+rest_keywords["likes"]+access_keyword+api_token+rest_keywords["pages"]+str(index+1)
        print(rest_url)
        if(download_objects(rest_url,str(username+"_likes.json"))==True):
            return

def search(keywords,n_pages=1):
    #GET /search/{$term}/
    for index in range(n_pages):
        print("\n\nPage: {}".format(index+1))
        rest_url=thingiverse_api_base+rest_keywords["search"]+keywords+access_keyword+api_token+rest_keywords["pages"]+str(index+1)
        if(download_objects(rest_url,str(keywords+".json"))==True):
            return

def userlist(userlistfile):
    #Read the user data to a list
    userList=loadData(userlistfile,"User list")
    #Iterate the list and call the single user download 
    #function for each user in the list
    for n in userList:
        user(n,args.pages)

#Set the path for the STL's to go to. If it doesn't exist, create it.
stl_path = "./stls"
json_path = "./jsons"
if not os.path.exists(stl_path):
    os.makedirs(stl_path)
if not os.path.exists(json_path):
    os.makedirs(json_path)

#Boring stuff to make the code a bit more readable
rest_keywords={"newest":"/newest","users":"/users/","likes":"/likes/","things":"/things/","files":"/files","search":"/search/","pages":"&page="}
thingiverse_api_base="https://api.thingiverse.com/"
access_keyword="?access_token="

#If the api_token hasn't been manually entered above, look for it in apikey.txt
if api_token == "Insert API token here":
    print("API key not entered into script, looking for it in apikey.txt")
    api_token=loadData("apikey.txt","Api key")[0]

#Initialise the error list with the header
errorList=["Errors occured when downloading the following:"]

if __name__ == "__main__":

    print("\nTHINGIVERSE DOWNLOADER")

    parser = argparse.ArgumentParser()

    parser.add_argument("--newest", type=bool, dest="newest_true",
                        help="It takes the newest objects uploaded")

    parser.add_argument("--user", type=str, dest="username",
                        help="Downloads the object of a specified user")

    parser.add_argument("--pages", type=int, default=1,
                        help="Defines the number of pages to be downloaded.")

    parser.add_argument("--all", type=bool, default=False,
                        help="Download all the pages available (MAX 1000).")

    parser.add_argument("--likes", type=str, dest="likes",
                        help="Downloads the likes of a specified user")

    parser.add_argument("--search", type=str, dest="keywords",
                        help="Downloads the objects that match the keywords. 12 objects per page\n Example: --search 'star wars'")

    parser.add_argument("--userlist", type=str, dest="userlist",
                        help="Loads users to download from specified file (1 per line)")

    args = parser.parse_args()

    if args.all:
        args.pages=1000

    if args.newest_true:
        newest(args.newest_true)
    elif args.username:
        user(args.username,args.pages)
    elif args.userlist:
        userlist(args.userlist)
    elif args.likes:
        likes(args.likes,args.pages)
    elif args.keywords:
        search(args.keywords,args.pages)
    else:
        newest(1)

    #If the errorlist has more than just the heading in it,
    #iterate through and print it all out
    if len(errorList) > 1:
        for n in errorList:
            print(n)