from BeautifulSoup import BeautifulSoup
import urllib2
import numpy as np
import os
html_template = "http://incubator.ecmwf.int/2e/rasdaman/ows?service=WCS&version=2.0.1&request=GetCoverage&coverageId=discharge_forecast&subset=Lat(49.0,60.0)&subset=Long(-11.0,3.0)&subset=ansi(%222015-12-15T00:00:00+00:00%22)&subset=forecast({day})&subset=ensemble({ensemble_name})"

for x in range(0, 720, 24):
    for y in range(0, 51):
        html = html_template.replace('{day}', str(x)).replace('{ensemble_name}', str(y))
        print html
        content=urllib2.urlopen(html).read()

        soup = BeautifulSoup(content)

        data = soup.tuplelist.string
    
        text_file = r'C:\Floodhack\data\day_{day}.txt'.format(day=x)
        if not os.path.exists(text_file):
            with open(text_file, 'a+') as outfile:
                outfile.write(data + '\n')


