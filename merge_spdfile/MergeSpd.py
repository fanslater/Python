# -*- coding:gbk -*-
from __future__ import print_function
import os
import sys
import CommentedTreeBuilder as ctb
import shutil
import datetime as dt

try:
    import xml.etree.cElementTree as et
except ImportError:
    import xml.etree.ElementTree as et

def formatXml(element, indent, newline, level=0):
    temp = list(element)
    for subelement in temp:
        if temp.index(subelement) < (len(temp) - 1):
            subelement.tail = newline + indent * (level + 1)
        else:
            subelement.tail = newline + indent * level
        formatXml(subelement, indent, newline, level=level + 1)

full_spd_default = "./bin/KCBPSPD.xml"
while 1:
    full_spd = raw_input("请输入全量kcbpspd.xml路径（可将文件拖拽到当前窗口）（不输默认【%s】）\n" % full_spd_default)
    if len(full_spd) == 0 or full_spd.isspace():
        full_spd = full_spd_default
    else:
        full_spd_default = full_spd

    add_spd = raw_input("请输入增量kcbpspd.xml路径（可将文件拖拽到当前窗口）（不输默认【./add_KCBPSPD.xml】）\n")
    if len(add_spd) == 0 or add_spd.isspace():
        add_spd = "./add_KCBPSPD.xml"

    out_spd = full_spd

    # 备份原来的全量SPD文件
    try:
        shutil.copy(full_spd, os.path.splitext(full_spd)[0] + "." + dt.datetime.now().strftime("%Y%m%d%H%M%S") + ".backup.xml")
    except Exception as ex:
        print("backup old full_spd error!", ex)
        os.system("pause")
        sys.exit(-1)

    # 读取全量SPD
    try:
        treeFullSpd = et.parse(full_spd, parser=ctb.CommentedTreeBuilder())
        ndFullSpdRoot = treeFullSpd.getroot()
    except Exception as ex:
        print("parse xml [%s] error!" % full_spd, ex)
        os.system("pause")
        sys.exit(-1)
    else:
        print("load xml[%s] success!" % full_spd)

    # 读取增量SPD
    try:
        treeAddSpd = et.parse(add_spd, parser=ctb.CommentedTreeBuilder())
        ndAddSpdRoot = treeAddSpd.getroot()
    except Exception as ex:
        print("parse xml [%s] error!" % add_spd, ex)
        os.system("pause")
        sys.exit(-1)
    else:
        print("load xml[%s] success!" % add_spd)

    # 将增量spd的内容追加到全量spd
    for child in ndAddSpdRoot:
        ndFullSpdRoot.append(child)

    # 去重
    lstProgram = ndFullSpdRoot.findall("program")
    for i in range(len(lstProgram) - 1, 0, -1):
        for j in range(i - 1, -1, -1):
            if i != j and lstProgram[i].attrib["name"] == lstProgram[j].attrib["name"]:
                try:
                    ndFullSpdRoot.remove(lstProgram[j])  # 这里操作list是没用的，list只是缓存了节点对象地址。要去root节点对接里面删除节点。
                except:
                    pass

    # 重新美化xml
    formatXml(ndFullSpdRoot, "  ", "\n")
    treeFullSpd.write(out_spd, "UTF-8")
    print("处理成功，输出文件=[%s]\n\n" % out_spd)
    os.system("pause")
