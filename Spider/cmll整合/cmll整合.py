from lxml import etree
import re
import requests
import urllib.parse


# config
getimg = False
# show，showfull，print
htmltype = 'show'

with open('cmll原始.htm', 'r') as f:
    str_html = f.read()
tree = etree.HTML(str_html)
c = 0
tr = ''
td = ''
e = tree.xpath('//div[@class="singlealg"]')
for j in range(42):
    imgc = (int(j % 7))*6 + int(j/7)
    cm = 7
    # 全公式版本采用横排其他版本竖排
    if htmltype == 'showfull':
        imgc = j
        cm = 6
    i = e[imgc]
    img = i.xpath('.//img/@src')[0]
    title = i.xpath('.//h3//text()')[0]
    alg = []
    emalg = i.xpath('.//li//text()')[:1]
    if htmltype == 'showfull':
        if title.startswith('L'):
            emalg = i.xpath('.//li//text()')
        else:
            while True:
                try:
                    urld = i.xpath('.//li//a/@href')[-1]
                    urld = 'http://www.speedcubedb.com/' + urld
                    r = requests.get(urld, timeout=5)
                    dtree = etree.HTML(r.text)
                    emalg = dtree.xpath('//tr/td[1]/text()')
                    break
                except:
                    pass
        print('%s detail' % j)
    for a in emalg:
        a = re.sub('^\s+|\s+$', '', a)
        if a != '' and a != 'More Algorithms':
            alg.append(a)
    if htmltype == 'print':
        alg = '<br>'.join(alg)
    else:
        stralg = []
        for a in alg:
            urla = 'alg/index.html?alg=%s&title=%s&stage=CMLL&type=alg'

            title_u = urllib.parse.quote(title)
            alg_u = a.replace(' ', '_').replace("'", '-')
            setup = []
            stralg.append('<a href ="%s" target="_blank">%s</a>' % (
                urla % (alg_u, title_u), a))
        alg = '<br>'.join(stralg)
    # 打印版本做是当缩减保证a4可以打印下
    if htmltype == 'print':
        title = title.replace(' Commutator', '').replace(
            'Sune', 'S').replace('Anti S', 'AS')
        alg = alg.replace("F R U' R' U' R U R' F' R U R' U' R' F R F'",
                          "F RU'R'U' RUR'F' RUR'U' R'FRF'")
    # 大多情况不需要重新获取图片
    if getimg:
        r = requests.get(img)
        with open('img/%s.png' % imgc, 'wb') as f:
            f.write(r.content)
        print('%s image' % j)
    td += """
    <td valign = 'top'>
        <img src = 'img/%s.png' >
        <br>
        <b>%s</b>
        <br>
        %s
    </td>
    """ % (imgc, title, alg)
    c += 1

    if(c == cm):
        c = 0
        tr += """
        <tr>
        %s
        </tr>
        """ % td
        td = ''
html = """
<title>CMLL</title>
<link rel="shortcut icon" type="image/png" href="img/favicon.png">
<style type="text/css">
    td {
        padding: 3px;
        width: 250px;
        font-size: 12;
    }
    img {
        height: 70px;
        width: 70px;
    }
</style>
<table>
%s
</table>
""" % tr
if htmltype == 'print':
    html = """
    <style type="text/css">
        td {
            padding: 1px;
            width: 200px;
            font-size: 8;
        }
        img {
            height: 35px;
            width: 35px;
        }
    </style>
    <table>
    %s
    </table>
    <br>
    <table>
    %s
    </table>
    """ % (tr, tr)

if htmltype == 'print':
    fn = 'CMLLPrint.html'
if htmltype == 'show':
    fn = 'CMLL.html'
if htmltype == 'showfull':
    fn = 'CMLLFull.html'
with open(fn, 'w') as f:
    f.write(html)
