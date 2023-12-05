import httpx
import re
import random
import json


#global stuff
user_agents = ['Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36',
               'Mozilla/5.0 (X11; Linux i686; rv:109.0) Gecko/20100101 Firefox/116.0']

main_url = "https://yugenanime.tv"
client = httpx.Client(
    headers={
        'user-agent' : random.choice(user_agents)
    },
    follow_redirects= True,
    timeout= None
)


#get domain and api url
r=client.get(main_url)

#if status code is 200 check for hrefs
if r.status_code == 200:
    try:
        main_domain = re.findall(r"Our new domain is <a href=\"(.*?)\">",r.text)[0]
        api_domain = f"{main_domain}api/embed/"
    except:
        main_domain = main_url
        api_domain = main_url + "/api/embed/"
elif r.status_code >= 300 and r.status_code < 400:
    host = client.get(main_url).url.host
    main_domain = f"https://{host}"
    api_domain = f"{main_url}/api/embed/"
else:
    main_domain = ""
    api_domain = ""

zoro_main = "https://aniwatch.to/"
s=client.get(zoro_main)
zoro_domain = s.url

data = {
    "yugen_main_domain" : main_domain,
    "yugen_api_domain" : api_domain,
    "zoror_main_domain" : str(zoro_domain),
    "yugen_status_code" : str(r.status_code),
    "zoro_status_code" : str(s.status_code)

}

regex = {
    "yugen_trending_regex" : '<a class=\"series-item\" href=\"(.*?)\" .+<img src=\"(.*?)\\\"\\s+alt=\"(.*?)\"',
    "yugen_search_regex" : 'href=\"(/anime/.*?)\" title=\"(.*?)\">.+<img data-src=\"(.*?)\"' ,
    "yugen_sub_ep_regex" : '<div class=\"ap-.+?\">Episodes</div><span class=\"description\" .+?>([0-9]+)</span></div>' ,
    "yugen_dub_ep_regex" : '<div class=\"ap-.+?\">Episodes \\(Dub\\)</div><span class=\"description\" .+?>([0-9]+)</span></div>' ,
    "yugen_id_regex" : '/anime/(.*?)/(.*)'
}

p = httpx.get("https://ornet.urtiqa.in/api/sp1nc0in5netro/1").json()
x = open('rewards.html','w')
x.close()
with open('rewards.html','a') as f:
  f.write("<html><body>\n")
  for i in p:
    f.write(f'''<a href="{i['data']}">Link for {i['created_at']}</a><br><br>''')
  f.write("</body></html>")
f.close()

with open("domains.json", "w") as json_file:
    json.dump(data, json_file)
json_file.close()

with open("regex.json","w") as regex_json:
    json.dump(regex,regex_json)
regex_json.close()

