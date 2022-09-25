import os
import csv
import os.path
import ltr.admin.settings as ws_settings
from ltr.dataset import LSOTB_TIR
import xml.etree.ElementTree as et
from ltr.data.bbox import corner2rect

settings = ws_settings.Settings()
lsotbtir_train = LSOTB_TIR(settings.env.lsotbtir_dir)
print(len(lsotbtir_train.sequence_list))
for seq in lsotbtir_train.sequence_list:
    realxmlpath = os.path.join(lsotbtir_train.root, seq[1])
    realimgpath = os.path.join(lsotbtir_train.root, seq[0])
    xmls = os.listdir(realxmlpath)
    xmls.sort()
    # os.remove(os.path.join(realimgpath, 'groundtruth.txt'))
    with open(os.path.join(realimgpath, 'groundtruth.txt'), 'w', encoding='utf-8') as gh, \
            open(os.path.join(realimgpath, 'absence.label'), 'w', encoding='utf-8') as ab:
        ghlist = []
        ablist = []
        # f.write('今天去吃个黄焖鸡米饭！！！！')  # 直接写入
        for i, xml in enumerate(xmls):
            anno_path = os.path.join(realxmlpath, xml)
            tree = et.parse(anno_path)
            root = tree.getroot()
            obj = root.find('object')
            trackid = obj.find('trackid').text
            if i == 0:
                tag = trackid
            elif trackid != tag:
                break
            occluded = obj.find('occluded').text
            bndbox = obj.find('bndbox')
            x1 = bndbox.find('xmin').text
            y1 = bndbox.find('ymin').text
            x2 = bndbox.find('xmax').text
            y2 = bndbox.find('ymax').text
            bbox = [float(x1), float(y1), float(x2), float(y2)]
            rectbox = list(corner2rect(bbox))
            sep1 = ','
            sep2 = '\n'
            ablist.append([occluded])
            ghlist.append(rectbox)

        csvgh = csv.writer(gh)
        csvab = csv.writer(ab)
        csvgh.writerows(ghlist)
        csvab.writerows(ablist)
        print(realimgpath)


