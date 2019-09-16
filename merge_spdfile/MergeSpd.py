# -*- coding:gbk -*-
from __future__ import print_function
import os
import sys
import CommentedTreeBuilder as ctb
import shutil

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

full_spd = raw_input("����ȫ��SPD·��������Ĭ�ϡ�./KCBPSPD.xml����\n")
if len(full_spd) == 0 or full_spd.isspace():
    full_spd = "./KCBPSPD.xml"

add_spd = raw_input("��������SPD·��������Ĭ�ϡ�./add_KCBPSPD.xml����\n")
if len(add_spd) == 0 or add_spd.isspace():
    add_spd = "./add_KCBPSPD.xml"

out_spd = full_spd

# ����ԭ����ȫ��SPD�ļ�
try:
    shutil.copy(full_spd, os.path.splitext(full_spd)[0] + "_bak.xml")
except Exception as ex:
    print("backup old full_spd error!", ex)
    os.system("pause")
    sys.exit(-1)

# ��ȡȫ��SPD
try:
    treeFullSpd = et.parse(full_spd, parser=ctb.CommentedTreeBuilder())
    ndFullSpdRoot = treeFullSpd.getroot()
except Exception as ex:
    print("parse xml [%s] error!" % full_spd, ex)
    os.system("pause")
    sys.exit(-1)
else:
    print("load xml[%s] success!" % full_spd)

# ��ȡ����SPD
try:
    treeAddSpd = et.parse(add_spd, parser=ctb.CommentedTreeBuilder())
    ndAddSpdRoot = treeAddSpd.getroot()
except Exception as ex:
    print("parse xml [%s] error!" % add_spd, ex)
    os.system("pause")
    sys.exit(-1)
else:
    print("load xml[%s] success!" % add_spd)

# ������spd������׷�ӵ�ȫ��spd
for child in ndAddSpdRoot:
    ndFullSpdRoot.append(child)

# ȥ��
lstProgram = ndFullSpdRoot.findall("program")
for i in range(len(lstProgram) - 1, 0, -1):
    for j in range(i - 1, -1, -1):
        if i != j and lstProgram[i].attrib["name"] == lstProgram[j].attrib["name"]:
            try:
                ndFullSpdRoot.remove(lstProgram[j])  # �������list��û�õģ�listֻ�ǻ����˽ڵ�����ַ��Ҫȥroot�ڵ�Խ�����ɾ���ڵ㡣
            except:
                pass

# ��������xml
formatXml(ndFullSpdRoot, "  ", "\n")
treeFullSpd.write(out_spd, "UTF-8")
print("����ɹ�������ļ�=[%s]" % out_spd)
os.system("pause")
