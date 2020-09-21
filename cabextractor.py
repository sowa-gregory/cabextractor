"""
cabextractor v1.0
"""


import sys
import os
import shutil
from pathlib import Path
import xml.etree.ElementTree as ET

cab_name = ""
tmp_dir = "__tmp"
out_dir = "out"
expand_cmd = "expand"


def extract():
    if os.path.isdir(tmp_dir):
        shutil.rmtree(tmp_dir)
    if os.path.isdir(out_dir):
        shutil.rmtree(out_dir)

    os.mkdir(tmp_dir)
    os.system(expand_cmd+" "+cab_name+" -F:* "+tmp_dir)

def moveFile(dir: str, src: str, dst: str):
    dst_file = os.path.join(dir, dst)
    src_file = os.path.join(tmp_dir, src)
    print("  movefile: ", src_file, dst_file)
    shutil.move(src_file, dst_file)


def characteristicExtract(dir: str, child: ET):
    for file in child:
        dst = file.attrib["type"]
        oper_name = file[0].attrib["type"]
        if(oper_name != "Extract"):
            raise("invalid operation:"+oper_name)
        param = file[0][0]
        if param.tag != "parm":
            raise("invalid xml structure")
        name = param.attrib["name"]
        src = param.attrib["value"]
        if name != "Source":
            raise("invalid param name:"+name)

        moveFile(dir, src, dst)


def characteristicMakeDir(child: ET):
    oper_name = child[0].attrib["type"]
    if oper_name != "MakeDir":
        raise ("unknown xml structure")
    dir_name = out_dir+child.attrib["type"]
    print("mkdir:"+dir_name)
    Path(dir_name).mkdir(parents=True, exist_ok=True)

    characteristicExtract(dir_name, child[1:])


def characteristicFileOperation(child: ET):
    for ch in child:
        characteristicMakeDir(ch)


def reconstruct():
    tree = ET.parse(tmp_dir+os.path.sep+"_setup.xml")
    root = tree.getroot()
    for child in root:
        if child.tag == "characteristic":
            ctype = child.attrib["type"]
            if ctype == "Install":
                characteristicInstall(child)
            elif ctype == "FileOperation":
                characteristicFileOperation(child)

def characteristicInstall(child: ET):
    for param in child.findall("parm"):
        name = param.attrib["name"]
        value = param.attrib["value"]
        if name == "AppName":
            print("AppName:"+value)
        if name == "InstallDir":
            print("InstallDir:"+value)

if __name__ == "__main__":
    if len(sys.argv) < 2 or len(sys.argv) > 3:
        print("Usage: cabextractor cab_file [outdir]")
        exit()

    cab_name = sys.argv[1]
    if len(sys.argv) == 3:
        out_dir = sys.argv[2]

    extract()
    reconstruct()
    shutil.rmtree(tmp_dir)
