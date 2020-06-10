from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium import webdriver
from os.path import abspath
from os import path
from time import sleep
from seleniumrequests import Chrome
import json
import sys
import time
import traceback
sys.stdout = open('output.txt', 'w',encoding="utf-8")

options = webdriver.ChromeOptions() 
options.add_argument(r"--flag-switches-begin") 
options.add_argument(r"--flag-switches-end") 
options.add_argument(r"--enable-audio-service-sandbox") 
options.add_argument(r"--user-data-dir=C:\\Users\\mostafa-pc\\AppData\\Local\\Google\\Chrome\\User Data") 
chrome_driver_exe_path = abspath("./chromedriver/chromedriver.exe") 
assert path.exists(chrome_driver_exe_path), 'chromedriver.exe not found!'

#username="magnus_carlsen"
#username="cristiano"
username="thisisbillgates"
end_cursor=""
query_hash_id="7c8a1055f69ff97dc201e752cf6f"
burst_number=0
user_id=""
has_next_page=True

web = webdriver.Chrome(executable_path=chrome_driver_exe_path, options=options)
web.get("https://www.instagram.com/"+username+"/?__a=1")

web.set_window_position(0, 0)
web.set_window_size(700, 700)

def show_12_posts(end_cursor=end_cursor,user_id=user_id,has_next_page=has_next_page):
    ps=web.page_source
    ps=ps[ps.index("{"):ps.index("</pre>")]
    y='{}'
    try:
        y=json.loads(ps)
    except Exception:
        raise "can't parse"
    if "message" in y and y["message"]=="rate limited":
        print("::::::::::: rate limited wait(5m)  :::::::::::")
        time.sleep(300)
        return [end_cursor,user_id,True]

    graph_or_data="graphql" if "graphql" in y else "data"
    for post_number in range(len(y[graph_or_data]["user"]["edge_owner_to_timeline_media"]["edges"])):
        print("---------------- burst: "+str(burst_number)+"---------post_number: "+str(post_number)+"-------------")
        if graph_or_data=="graphql":
            user_id=y[graph_or_data]["user"]["id"]
        end_cursor=y[graph_or_data]["user"]["edge_owner_to_timeline_media"]["page_info"]["end_cursor"]
        has_next_page=y[graph_or_data]["user"]["edge_owner_to_timeline_media"]["page_info"]["has_next_page"]
        if(len(y[graph_or_data]["user"]["edge_owner_to_timeline_media"]["edges"][post_number]["node"]["edge_media_to_caption"]["edges"])>0):
            print("text",y[graph_or_data]["user"]["edge_owner_to_timeline_media"]["edges"][post_number]["node"]["edge_media_to_caption"]["edges"][0]["node"]["text"])
        print("likes",y[graph_or_data]["user"]["edge_owner_to_timeline_media"]["edges"][post_number]["node"]["edge_media_preview_like"]["count"])
        print("comments",y[graph_or_data]["user"]["edge_owner_to_timeline_media"]["edges"][post_number]["node"]["edge_media_to_comment"]["count"])
        print("thumbnail",y[graph_or_data]["user"]["edge_owner_to_timeline_media"]["edges"][post_number]["node"]["thumbnail_src"].replace("&amp;","&"))
        if("edge_sidecar_to_children" in  y[graph_or_data]["user"]["edge_owner_to_timeline_media"]["edges"][post_number]["node"]):
            print("media-1",y[graph_or_data]["user"]["edge_owner_to_timeline_media"]["edges"][post_number]["node"]["edge_sidecar_to_children"]["edges"][0]["node"]["display_url"].replace("&amp;","&"))
            print("media-2",y[graph_or_data]["user"]["edge_owner_to_timeline_media"]["edges"][post_number]["node"]["edge_sidecar_to_children"]["edges"][1]["node"]["display_url"].replace("&amp;","&"))
    
    return [end_cursor,user_id,has_next_page]

def query_hash():
    q="https://www.instagram.com/graphql/query/?query_hash="+query_hash_id+"&variables={%22id%22:%22"+user_id+"%22,%22first%22:"+str(1*12)+",%22after%22:%22"+end_cursor+"%22}"
    print(q,end_cursor)
    web.get(q)
    return show_12_posts()

end_cursor,user_id,has_next_page=show_12_posts()
try:
    while True:
        burst_number=burst_number+1
        end_cursor,_,has_next_page =query_hash()
        if has_next_page is False:
            break;
        time.sleep(1)
except Exception as e:
    print(e)
    

