# Install WooCommerce and WP Htaccess Editor plugins
# Download all content from web: wget -r -nc http://www.dougschmittantiques.com/
# Scp images to server: scp -rp * root@172.28.195.229:/var/www/wordpress/wp-content/images/
# Register all media:  for i in {0..99}; do sudo wp media import $i/* --allow-root --path=/var/www/html; rm -r $i; done


# Product	Reason for failure
# RANSOM & RANDOLPH OAK DENTAL CABINET W/ SWING OUT DRAWERS, SKU 145907630	Unable to use image "rrdentalcabinetfinished".
# Ransom & Randolph Dental Cabinet, SKU 9224967905	Unable to use image "rrdentalcabinet3finished".
# Rocky Mountain Motorcycle Trip, SKU 8790339882	Unable to use image "bikes-trucks-ect__Tonys-motorcycle-trip__Roll1__0334537-R1-044-20A".
# Ransom & Randolph Co. Oak Dental Cabinet, SKU 2341671537	Unable to use image "dental-doctors-cabinets__rrdentalcabca".
# Ransom & Randolph Co. Mahogany Dental Cabinet - Model #75, SKU 648106962	Unable to use image "dental-doctors-cabinets__rrcabinetno75__rrdentalcabinetcatalog".
# Ransom & Randolph Co. Oak Dental Cabinet - Model #75, SKU 4390955373	Unable to use image "dental-doctors-cabinets__rrcabinetno75__rrdentalcabinetcatalog".
# Oak Ransom & Randolph Co. Dental Cabinet, SKU 7398481827	Unable to use image "dental-doctors-cabinets__oakrrbest__rrcabinet65".
# Oak Ransom & Randolph Dental Cabinet - Cabinet #65 , SKU 72723008	Unable to use image "dental-doctors-cabinets__rrcabinet65wisconsin__rrcabinet65".
# Oak Ransom & Randolph Dental Cabinet - Cabinet #65 , SKU 4490855579	Unable to use image "dental-doctors-cabinets__rrcabinet65wisconsin__rrcabinet65".
# Oak Ransom & Randolph Dental Cabinet - Cabinet #65 , SKU 3761835939	Unable to use image "dental-doctors-cabinets__rrcabinet65wisconsin__rrcabinet65".
# Ransom & Randolph Co. Oak Dental Cabinet - Model #75, SKU 8811064219	Unable to use image "dental-doctors-cabinets__rrcabinetno75__rrdentalcabinetcatalog".
# Ransom & Randolph Co. Oak Dental Cabinet - Model #75, SKU 1991272804	Unable to use image "dental-doctors-cabinets__rrcabinetno75__rrdentalcabinetcatalog".
# Ransom & Randolph Co. Oak Dental Cabinet - Model #75, SKU 8780776254	Unable to use image "dental-doctors-cabinets__rrcabinetno75__rrdentalcabinetcatalog".
# Ransom & Randolph Co. Oak Dental Cabinet - Model #75, SKU 7411517735	Unable to use image "dental-doctors-cabinets__rrcabinetno75__rrdentalcabinetcatalog".
# Mahogany Ransom & Randolph Dental Cabinet - Cabinet #65 , SKU 2700932414	Unable to use image "dental-doctors-cabinets__rrcabinet65wisconsin__rrcabinet65".
# Ransom & Randolph Co. Oak Dental Cabinet - Model #75, SKU 512057278	Unable to use image "dental-doctors-cabinets__rrcabinetno75__rrdentalcabinetcatalog".
# Mommy, SKU 8233297617	Unable to use image "Hunters-pages__1st_year-windex-pic__h-sleep-in-hugster-2".
# Oak Stick & Ball Hanging Hat Rack with Beveled Mirror, SKU 1732694756	Unable to use image "specialty-items__stickballradks2018__DSC00001".
# Oak Stick & Ball Hanging Magazine Rack, SKU 744640053	Unable to use image "specialty-items__stickballradks2018__DSC00004".
# Siegel, SKU 1584917765	Unable to use image "Siegel".
import os
import sys
from pathlib import Path
from html.parser import HTMLParser
import hashlib

excluded_text = ["","\n","\n\n",'www.dougschmittantiques.com','\xa0',' or ', 'For pricing & information email: dougschmittantiques@verizon.net or phone: (570) 698-6694','Check-out our full listing of antiques at our homepage:']
excluded_images = ['signsSOLD_17055.gif','SOLD_17055.gif']


class MyHTMLParser(HTMLParser):
    startTitle = False;
    startBody = False;
    title = "";
    description = "";
    images = "";

    def handle_starttag(self, tag, attrs):
        tag = tag.lower();

        if tag == 'title':
            self.startTitle = True;
        if tag == 'img':
            for attr in attrs:
                if attr[0] == 'src' and attr[1] not in excluded_images:
                    if self.images != "":
                        self.images = f"{self.images},{attr[1]}"
                    else:
                        self.images = f"{attr[1]}"
        if tag == 'body':
            self.startBody = True;



    def handle_endtag(self, tag):
        if tag == 'title':
            self.startTitle = False;
        if tag == 'body':
            self.startBody = False;


    def handle_data(self, data):
        if(self.startTitle):
            self.title = self.title + data.replace('\n', ' ')

        if(self.startBody):
            if data not in excluded_text:
                self.description = self.description + data.replace("\"","\"\"") + "\n"


    def __init__(self):
        HTMLParser.__init__(self)

rootdir = "C://temp//www.dougschmittantiques.com//"
outfileName = "products.csv" # hardcoded path
folderOut = open( outfileName, 'w' )
folderOut.write('sku,title,categories,stock,description,images,"Attribute 1 name","Attribute 1 value(s)","Attribute 1 visible","Attribute 1 global"\n')

redirectOut = open("redirects.csv", "w")

result = list(Path(rootdir).rglob("*.[hH][tT][mM]"))

img_count = 0
file_count = 0

for file in result:
    file_count = file_count + 1

    f = open(file, 'r' ,encoding='UTF-8', errors='ignore')
    toWrite = f.read()
    parser = MyHTMLParser()
    parser.feed(toWrite);

    images = ""

    for img in parser.images.split(","):
        if "SOLD_17055" in img:
            continue;
        if img == '':
            continue;

        img_cleaned = img.replace("http://www.dougschmittantiques.com/","").replace("%20"," ");
        fileLocation = Path(f"{file.parent}/{img_cleaned}").resolve();
        newFilename = f"{os.path.relpath(fileLocation,rootdir)}".replace('/','__').replace('\\','__').replace(" & ","-").replace("'","").replace("(","").replace(")","").replace(" ","-");

        newFileDir = f"image_links2/{img_count % 20}";
        newFileLocation = f"{newFileDir}/{newFilename}".replace(" & ","-").replace("'","").replace("(","").replace(")","").replace(" ","-").replace("%20","-");
        os.makedirs(newFileDir, exist_ok=True)
        wpFileName = os.path.splitext(newFilename)[0]

        if os.path.exists(fileLocation):
            if not os.path.islink(newFileLocation):
                os.symlink(fileLocation, newFileLocation);

            if images == "":
                images = wpFileName
            else:
                images = images + f",{wpFileName}"

            img_count = img_count + 1;
        else:
            print ("no such file");

    category = ""

    if len(file.parts) > 4:
        category = file.parts[3]

    shash = int(hashlib.md5(str(file).encode()).hexdigest(), 16) % (10 ** 10)

    if images != '':
        title = parser.title.replace("\xa0","")

        folderOut.write(f'{shash},{title},{category},0,"{parser.description}","{images}","Old URL","{str(file)}",0,0\n')

        wp_url = title.replace(" & ","-").replace(" - ","-").replace("'","-").replace("(","").replace(")","").replace(" ","-").replace("%20","-").replace(".","").replace("\"","").replace("/","").replace("#","").lower();
        

        redirectOut.write(f'"/{"/".join(file.parts[3:])}",/product/{wp_url}/\n')


folderOut.close()
redirectOut.close()