# coding=utf-8
import os, sys
import glob  # 用来查找特定文件名的文件
from PIL import Image

# Safety Hat图片位置
src_img_dir = "D:/Project/matlab/fasterRcnn/train_image_1"
# Safety Hat图片的groundtruth的文件位置
src_txt_dir = "./input.txt"
src_xml_dir = "./Annotations"

img_Lists = glob.glob(src_img_dir + '/*.jpg')
# 图片名
img_basenames = []
for item in img_Lists:
    img_basenames.append(os.path.basename(item))

print(len(img_basenames))
image_names = []
for item in img_basenames:
    temp1, temp2 = os.path.splitext(item)
    image_names.append(temp1)

# open the crospronding txt file
now_gt = {}

fopen = open(src_txt_dir, 'r')
lines = fopen.readlines()
i = 0
temp3 = ''
# print((" 476   104   215   222".strip().split(" ")))
for num, line in enumerate(lines):
    if len(line.strip()) == 0: continue
    if line.startswith("ans"):
        i += 1
        temp3 = str(i) + '.jpg'
        print(line)
    else:
        # print(num)
        t1, t2, t3, t4 = line.strip().replace('\n', '').replace('    ', ',').replace('   ', ',').replace('  ',
                                                                                                         ',').split(",")
        # print(line)
        if temp3 not in now_gt.keys():
            now_gt[temp3] = [[t1, t2, t3, t4]]
        else:
            now_gt[temp3].append([t1, t2, t3, t4])
print(len(now_gt.keys()))
# print(num, line)
# temp1, temp2 = line.split(',')
# if (len(temp2.replace('\n', '').strip()) != 0):
#     t1, t2, t3, t4 = temp2.replace('\n', '').strip().split(' ')
#     # print("*%s %s %s %s*" % (t1, t2, t3, t4))
#     # print(temp2.replace('\n', '').strip().split(' '))
#     if temp1 not in now_gt.keys():
#         now_gt[temp1] = [[t1, t2, t3, t4]]
#     else:
#         now_gt[temp1].append([t1, t2, t3, t4])
#
# else:
#     now_gt[temp1] = []
# print(num, ' is processing ... ')
# print(len(now_gt.keys()))
# print(i)

total = 0

for img in image_names:
    total += 1
    im = Image.open((src_img_dir + '/' + str(total) + '.jpg'))
    width, height = im.size
    xml_file = open((src_xml_dir + '/' + str(total) + '.xml'), 'w')
    xml_file.write('<annotation>\n')
    xml_file.write('    <folder>VOC2007</folder>\n')
    xml_file.write('    <filename>' + str(total) + '.jpg' + '</filename>\n')
    xml_file.write('    <size>\n')
    xml_file.write('        <width>' + str(width) + '</width>\n')
    xml_file.write('        <height>' + str(height) + '</height>\n')
    xml_file.write('        <depth>3</depth>\n')
    xml_file.write('    </size>\n')
    for img_each_label in now_gt[str(total) + ".jpg"]:
        spt = img_each_label
        cnt = len(img_each_label) // 4
        for i in range(0, cnt):
            xml_file.write('    <object>\n')
            xml_file.write('        <name>' + str("person") + '</name>\n')  # 必须更改为对应分类的名称
            xml_file.write('        <pose>Unspecified</pose>\n')
            xml_file.write('        <truncated>0</truncated>\n')
            xml_file.write('        <difficult>0</difficult>\n')
            xml_file.write('        <bndbox>\n')
            xml_file.write('            <xmin>' + str(spt[i * 4 + 0]) + '</xmin>\n')
            xml_file.write('            <ymin>' + str(spt[i * 4 + 1]) + '</ymin>\n')
            xml_file.write('            <xmax>' + str(int(spt[i * 4 + 2]) + int(spt[i * 4 + 0])) + '</xmax>\n')
            xml_file.write('            <ymax>' + str(int(spt[i * 4 + 3]) + int(spt[i * 4 + 1])) + '</ymax>\n')
            xml_file.write('        </bndbox>\n')
            xml_file.write('    </object>\n')

    xml_file.write('</annotation>')

print(total)
