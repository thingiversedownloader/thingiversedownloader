# thingiversedownloader
Download items from thingiverse using a script.  By various methods.

Run with the following command line instructions:

--newest = It takes the newest objects uploaded.

--user=Downloads the object of a specified user.

--likes=Downloads the likes of a specified user.

--search=Downloads the objects that match the keywords. 12 objects per page Example: --search 'star wars'.

--userlist=Loads users to download from specified file (1 per line).

The following are optional, pages defaults to 1, only use these if you're wanting more.

--pages=Defines the number of pages to be downloaded.

--all=Download all the pages available (MAX 1000).



Examples: 

To download the first page of a users designs: 
    thingiverse_downloader-withoutapikey.py --user <username>

To download the first page from all users in a line seperated list: 
    thingiverse_downloader-withoutapikey.py --userlist <relative path to text file>
  
To download the first page from a search for Star Wars:
    thingiverse_downloader_withoutapikey.py --search 'star wars'
    
By default the first page is downloaded.  To change this, use --pages <number of pages to download> or --all.
