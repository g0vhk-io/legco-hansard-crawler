import requests
import sys
from lxml import etree
import re
import os

def crawl(year, output_dir):
    current_year = year - 2000
    year_start = (current_year // 4) * 4
    year_end = year_start + 4
    url = "https://www.legco.gov.hk/general/chinese/counmtg/yr%.2d-%.2d/mtg_%.2d%.2d.htm" % (year_start, year_end, current_year, current_year + 1)
    r = requests.get(url)
    r.encoding = "utf-8"
    root = etree.HTML(r.text)
    cm_dates = [re.match(r'.*date=([^&]+)', link).group(1) for link in root.xpath("//a/@href") if link.find("date=") != -1]
    print(url)
    print(cm_dates)
    for d in cm_dates:
        rundown_request = requests.get('http://www.legco.gov.hk/php/hansard/chinese/rundown.php?date=%s&lang=2' % (d))
        rundown_html = rundown_request.text.split('\n')
        for line in rundown_html:
            if line.find(".pdf") != -1:
                var, url = line.split(" = ")
                url = url.strip()
                pdf_url = "https:" + url.replace("\"", "").replace(";", "").replace("#", "").replace("\\", "")
                file_name = pdf_url.split('/')[-1]
                year , month, day = d.split("-")
                dest = os.path.join(output_dir, pdf_url.split('/')[-1])
                print("Downloading " + pdf_url + "...", end='')
                pdf_request = requests.get(pdf_url)
                f = open(dest , 'wb')
                f.write(pdf_request.content)
                f.close() 
                print("Done")

if __name__ == "__main__":
    crawl(int(sys.argv[1]), sys.argv[2])
