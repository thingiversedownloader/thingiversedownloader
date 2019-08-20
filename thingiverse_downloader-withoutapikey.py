# -*- coding: utf-8 -*-

import requests
import json
import sys
import argparse
import os.path
import re
from collections import OrderedDict

stl_path = "./stls"
if not os.path.exists(stl_path):
    os.makedirs(stl_path)

thingiverse_api_base="https://api.thingiverse.com/"
access_keyword="?access_token="
api_token="insert api key here" #Go to https://www.thingiverse.com/apps/create and select Desktop app

rest_keywords={"newest":"/newest","users":"/users/","likes":"/likes/","things":"/things/","files":"/files","search":"/search/","pages":"&page="}

def newest(n_pages=1):
    for index in range(n_pages):
        print("\n\nPage: {}".format(index+1))
        rest_url=thingiverse_api_base+rest_keywords["newest"]+access_keyword+api_token+rest_keywords["pages"]+str(n_pages)
        download_objects(rest_url,"newest.json");

def user(username,n_pages=1):
    #/users/{$username}/things
    for index in range(n_pages):
        print("\n\nPage: {}".format(index+1))
        rest_url=thingiverse_api_base+rest_keywords["users"]+username+rest_keywords["things"]+access_keyword+api_token+rest_keywords["pages"]+str(index+1)
        print(rest_url)
        if(download_objects(rest_url,str(username+".json"))==True):
            return

def likes(username,n_pages=1):
    #/users/{$username}/things
    for index in range(n_pages):
        print("\n\nPage: {}".format(index+1))
        rest_url=thingiverse_api_base+rest_keywords["users"]+username+rest_keywords["likes"]+access_keyword+api_token+rest_keywords["pages"]+str(index+1)
        print(rest_url)
        download_objects(rest_url,str(username+"_likes.json"));

def search(keywords,n_pages=1):
    #GET /search/{$term}/
    for index in range(n_pages):
        print("\n\nPage: {}".format(index+1))
        rest_url=thingiverse_api_base+rest_keywords["search"]+keywords+access_keyword+api_token+rest_keywords["pages"]+str(index+1)
        download_objects(rest_url,str(keywords+".json"))

'''def parser_info(rest_url, file_name):
    s = requests.Session() #It creates a session to speed up the downloads
    r=s.get(rest_url)
    data=r.json()

    #Save the data
    file=open(file_name,"wb")
    file.write(json.dumps(data, indent=4, sort_keys=True,ensure_ascii=False).encode('utf8'))
    file.close()

    #Reading the json file
    file=open(file_name,"r")
    data_pd=json.loads(file.read())

    #The page has objects?
    if (len(data_pd)==0):
        print("\n\nNo more pages- Finishing the program")
        sys.exit()

    #Is it an error page?
    for n in data_pd:
        if (n=="error"):
            print("\n\nNo more pages- Finishing the program")
            sys.exit()

    print("Parsing data from {} objects from thingiverse".format(len(data_pd)))

    for object in range(len(data_pd)):

        object_id=str(data_pd[object]["id"])
        print("\n{} -> {}".format(data_pd[object]["name"],data_pd[object]["public_url"]))

        #Name and last name
        print("Name: {} {}".format(data_pd[object]["creator"]["first_name"],data_pd[object]["creator"]["last_name"]))
'''

def download_objects(rest_url, file_name):

    # r = requests.get(rest_url)
    s = requests.Session() #It creates a session to speed up the downloads
    r=s.get(rest_url)
    data=r.json()

    #Save the data
    file=open(file_name,"wb")
    file.write(json.dumps(data, indent=4, sort_keys=True,ensure_ascii=False).encode('utf8'))
    file.close()

    #Reading the json file
    file=open(file_name,"r")
    data_pd=json.loads(file.read())

    #The page has objects?
    if (len(data_pd)==0):
        print("\n\nNo more pages, exiting current operation")
        return True

    #Is it an error page?
    for n in data_pd:
        if (n=="error"):
            print("\n\nFound Error page, exiting current operation")
            return True()

    print("Downloading {} objects from thingiverse".format(len(data_pd)))

    for object in range(len(data_pd)):

        object_id=str(data_pd[object]["id"])
        print("\n{} -> {}".format(data_pd[object]["name"],data_pd[object]["public_url"]))
        # print("Object id: {}".format(object_id))

        thing_name = data_pd[object]["name"].replace("/","-").replace(":"," -").replace("\"","").replace("\"#","").replace("*","").replace("<","").replace(">","")
        thing_name = re.sub('[!@#$?.]', '', thing_name)
        thing_name = re.sub("^\s+|\s+$", "", thing_name)
        file_path = "./stls/"+data_pd[object]["creator"]["name"]+"/"+thing_name

        if not os.path.exists(file_path):
            os.makedirs(file_path)
        else:
            print("\nSkipping already downloaded object")
            continue

        #User name
        print("{} {}".format(data_pd[object]["creator"]["first_name"],data_pd[object]["creator"]["last_name"]))

            # GET /things/{$id}/files/{$file_id}

        #Get file from a things
        r=s.get(thingiverse_api_base+rest_keywords["things"]+object_id+rest_keywords["files"]+access_keyword+api_token)
        files_info=r.json()

        for file in range(len(files_info)):
            #if(files_info[file]["name"].find(".stl"))!=-1:
                print("    "+files_info[file]["name"])
                #Download the file
                download_link=files_info[file]["download_url"]+access_keyword+api_token
                r = s.get(download_link)

                with open(file_path+"/"+files_info[file]["name"], "wb") as code:
                    code.write(r.content)

def userlist(userlistfile):
    #Load the data from the file to a list
    if os.path.isfile(userlistfile):
        file=open(userlistfile,"r")
        userList = file.readlines()
        file.close()
        # Removing \n
        userList = [x.strip() for x in userList]
        for n in userList:
            user(n,args.pages)
    else:
        print("Specified userlist file not found")
        return


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
