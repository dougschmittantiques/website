import os
from PIL import Image
Image.LOAD_TRUNCATED_IMAGES = True

img_fold = "image_links2"
fileDir = os.path.dirname(__file__)  # this file directory
imagesFolderBase = os.path.join(fileDir, img_fold)
optimizedFolderBase = os.path.join(fileDir, "optimized")

err_img = []

# if the folder to save optimized images doesn't exist don't create a new folder
if os.path.isdir(optimizedFolderBase) == False:
    os.mkdir(optimizedFolderBase)

unopt_size = 0
opt_size = 0

for fold in range(20):
    print(f"Fold: {fold}")
    imagesFolder = imagesFolderBase + "\\" + str(fold)
    optimizedFolder = optimizedFolderBase + "\\" + str(fold)

    if os.path.isdir(optimizedFolder) == False:
        os.mkdir(optimizedFolder)

    unopt_images = []
    for file in os.listdir(imagesFolder):
        if file.endswith(("jpg", "jpeg", "png", "JPG", "gif")):
            unopt_images.append(file)
            size = os.stat(imagesFolder + f"\{file}").st_size
            print(f"Original Image's Size: {file} - {size}")
            unopt_size = unopt_size + size
        else:
            err_img.append(file)

    print("Compressing images...")
    for image in unopt_images:
        if not os.path.exists(os.path.join(optimizedFolder, image)):
            img = Image.open(os.path.join(fileDir, imagesFolder, image))
            # if you want to resize the image use the code below & set the size
            # img = img.resize((800,500), resample=1)
            try:
                img.save(
                    os.path.join(optimizedFolder, image),
                    optimize=True,
                    quality=60,
                )

                org_size = os.stat(imagesFolder + f"\{file}").st_size
                size = os.stat(optimizedFolder + f"\{image}").st_size
                print(f"New Compressed Image's Size: {image} - {size}  %: {size*100/org_size}")
                opt_size = opt_size + size
            except:
                err_img.append(file)
            

        

print("Errors")
for err_i in err_img:
    print(err_i)

print(f"Old size: {unopt_size}  New size: {opt_size}  %: {opt_size*100/unopt_size}")