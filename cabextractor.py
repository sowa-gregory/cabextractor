import xml.etree.ElementTree as ET
import os
import shutil
cab_name = "traka.cab"
tmp_dir = "tmp"
expand_cmd = "expand"

def extract():
    if os.path.isdir(tmp_dir):
        shutil.rmtree(tmp_dir)
    os.mkdir(tmp_dir)
    os.system(expand_cmd+" "+cab_name+" -F:* "+tmp_dir)

def characteristicInstall(child:ET):
    for param in child.findall("parm"):
        name = param.attrib["name"]
        value = param.attrib["value"]
        if name=="AppName": print("AppName:"+value)
        if name=="InstallDir": print("InstallDir:"+value)

def characteristicExtract( dir_name:str, child:ET):
    for c in child:
        print("  "+c.attrib["type"])
        
def characteristicMakeDir(child:ET):
        oper_name = child[0].attrib["type"]
        if oper_name!="MakeDir" : raise ("unknown xml structure")
        dir_name = child.attrib["type"]
        print("dir:"+dir_name)
        characteristicExtract(dir_name, child[1:])
        
def characteristicFileOperation(child:ET):
    for ch in child: characteristicMakeDir(ch)

#extract()
tree = ET.parse(tmp_dir+os.path.sep+"_setup.xml")
root = tree.getroot()
for child in root:
    if child.tag == "characteristic":
        ctype = child.attrib["type"]
        if ctype == "Install": characteristicInstall(child)
        elif ctype == "FileOperation": characteristicFileOperation(child)

