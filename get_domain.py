import httpx
import re
import random
import json


#global stuff
user_agents = ['Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36',
               'Mozilla/5.0 (X11; Linux i686; rv:109.0) Gecko/20100101 Firefox/116.0']

main_url = "https://yugen.to"
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


data = {
    "main_domain" : main_domain,
    "api_domain" : api_domain
    "status_code" : str(r.status_code)
}

with open("domains.json", "w") as json_file:
    json.dump(data, json_file)
json_file.close()
