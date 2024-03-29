# 10.08.2023 -> 11.08.2023 -> 14.09.2023 -> 17.09.2023 -> 10.10.2023

# Class import
from Stream.util.Driver import Driver
from Stream.util.m3u8 import download
from Stream.util.util import console, msg
from Stream.update import main_update

# Import
from bs4 import BeautifulSoup
from seleniumwire.utils import decode


# Class init
main_update()
driver = Driver()
driver.create(True)


# [ function ] main
def get_film(vid_id):

    url = f"https://streamingcommunity.at/watch/{vid_id}"
    driver.get_page(url=url, sleep=3)
    m3u8 = {"url": "", "data": "", "req_header": "", "key": ""}

    console.log("[blue]Find m3u8")
    for req in driver.driver.requests:

        if("enc.key" in req.url): 
            console.log(f"[green]KEY FIND:  [red]{req.url}")

            # Get response data
            response_body = decode(req.response.body, req.response.headers.get('Content-Encoding', 'identity'))
            m3u8['key'] = "".join(["{:02x}".format(c) for c in response_body])

        if("type" in req.url):
            console.log(f"[green]M3U8 FIND:  [red]{req.url}")

            # Get response data
            m3u8_data = decode(req.response.body, req.response.headers.get('Content-Encoding', 'identity'))
            m3u8['data'] = BeautifulSoup(m3u8_data, "lxml").text

            # Add headers and url
            m3u8['req_header'] = dict(req.headers)
            m3u8['url'] = req.url

    if(m3u8['url'] != ""):
        console.log("[blue]Start download ...")
        download(m3u8['url'], m3u8['data'], m3u8['req_header'], m3u8['key'], vid_id+".mp4")
    else:
        console.log("[red]Try reduce quality")

    driver.close()

get_film(msg.ask("[cyan]Insert film key ").replace(" ", ""))

