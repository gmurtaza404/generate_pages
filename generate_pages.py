import os
import argparse
from bs4 import BeautifulSoup
from PIL import Image

# Globals
headerHtml ="<html lang=\"en\"><head><meta charset=\"UTF-8\"> <meta name=\"viewport\" content=\"width=device-width, initial-scale=1.0\"><meta http-equiv=\"X-UA-Compatible\" content=\"ie=edge\"><title>Proxy server</title></head>"
rootHtml = "<div id=\"root\"> <p> This page is just an artificial memeory load </p> <p> for sake of comaparison each div will take same amount of space</p></div>"
video_width = "320"
video_height = "240"
video_loop = True

def get_image_size(image_name):
    with Image.open(image_name) as img:
            return img.size
    



def simple_code(size_allocation):
    return "x = Array({})".format(size_allocation)

def make_html(img,vid,code):
    tempHtml = headerHtml + "<body>" + rootHtml
    tempHtml = tempHtml +img+vid+code
    tempHtml = tempHtml + "</body>" + "</html>"
    soup = BeautifulSoup(tempHtml, 'html.parser')
    tempHtml = soup.prettify()
    return tempHtml





def generate_pages():
    print "Generating pages..."
    
    parser = argparse.ArgumentParser()
    parser.add_argument("max_size", type=int ,help="max_size of the objects")
    parser.add_argument("img_format" ,help="image format you want to use, options are .jpeg, .jpg, .pdf, .png")
    parser.add_argument("vid_format" ,help="image format you want to use, options are .3gp, .flv, .mkv, .mp4")
    parser.add_argument("code_type",  help="code complexity, simple_script or complex_script")
    args = parser.parse_args()
    
    
    print "generating pages with max {}_mb sized objects\n{} image format.\n{} video format.\n{} code complexity".format(str(args.max_size),args.img_format,args.vid_format,args.code_type)
    
    root_directory = os.getcwd()
        
    for x in range(0,args.max_size):
        print "making a page with {}_mb sized objects.".format(x+1)
        
        folder_name = "{}_mb".format(x+1)
        
        if not os.path.exists(folder_name):
            os.makedirs(folder_name)
        
        os.chdir(folder_name)

        #video file
        vid_name = filter( (lambda y: args.vid_format in y) ,os.listdir("../videos") )[0]
        concat_vid = ("{}/videos/{} \+ ".format(root_directory,vid_name)) * (x) + "{}/videos/{}".format(root_directory,vid_name)
        video_generate_command = "mkvmerge -o out_video{} {} > {}/logs.txt".format(args.vid_format,concat_vid,root_directory)
        os.system(video_generate_command)

        #image file
        img_name = filter( (lambda y: args.img_format in y) ,os.listdir("../pictures") )[0]
        concat_pic = ("{}/pictures/{} ".format(root_directory,img_name)) * (x) + "{}/pictures/{}".format(root_directory,img_name)
        picture_generate_command = "convert {} +append output_img{}  > {}/logs.txt".format(concat_pic,args.img_format,root_directory)
        os.system(picture_generate_command)

        video_width,video_height = get_image_size("output_img{}".format(args.img_format))

        code_name = filter( (lambda y: args.code_type == y),  map((lambda z: z.split(".")[0] ),os.listdir("../scripts")) )[0] + ".js"
       
        #code file 
        with open("code.js","wb") as f:
            with open("../scripts/{}".format(code_name)) as script_template:
                f.write(script_template.read().replace("{}", str((x+1)*1000000))) 

        # make html
        imageHtml = " <div id =\"images\"> <img src = \"output_img{}\" /></div>".format(args.img_format)
        videoHtml = ""
        if video_loop:
            videoHtml = "<div id = \"video\"> <video width=\"{}\" height=\"{}\" controls loop><source src=\"out_video{}\" type=\"video/mp4\"></video></div>".format(video_width,video_height,args.vid_format)
        else:
            videoHtml = "<div id = \"video\"> <video width=\"{}\" height=\"{}\" controls><source src=\"out_video{}\" type=\"video/mp4\"></video></div>".format(video_width,video_height,args.vid_format)
        
        codeHtml = "<div id = \"code\"><script src = \"code.js\"> </script></div>"
        html = make_html(imageHtml,videoHtml,codeHtml)

        with open("final_html.html","wb") as f:
            f.write(html)

        os.chdir(root_directory)

    print "Done..."
generate_pages()