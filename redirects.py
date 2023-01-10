import os
import sys

redirectIn = open("redirects.csv", "r")
redirectOut = open("redirects1.csv", "w")


lines = redirectIn.readlines()

urls = {}


for line in lines:
    line_split = line.strip().split(",")
    url = line_split[1][:-1]

    while url[-1] == "-":
        url = url[:-1]

    if url not in urls:
        urls[url] = 1
    else:
        if(url == "/product/oak-ribbon-cabinet"):
            print("a")
        urlCnt = urls[url]
        urls[url] = urlCnt + 1
        url = url + "-" + str(urlCnt + 1)

    print(url)
    redirectOut.write(line_split[0] + "," + url + "/\n")



redirectIn.close();
redirectOut.close();