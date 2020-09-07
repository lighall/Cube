import requests
from lxml import etree
import re
import urllib.parse

url_list = ['http://cubesolv.es/?query=+Kian+Mansour', 'http://cubesolv.es/?query=Alexander+Lau',
            'http://cubesolv.es/?query=Alexander%20Lau&page=2', 'http://cubesolv.es/?query=Sean+Patrick+Villanueva']
url_list = ['http://cubesolv.es/?query=Sean+Patrick+Villanueva']
name = 'Sean Patrick Villanueva'

with open('%sExample.html' % name.replace(' ', ''), mode='w', encoding='utf-8') as f:
    h = """
        <title>%s Example</title>
        <link rel="shortcut icon" type="image/jpg" href="img/favicon.ico">
        <a href="/Cube">HOME</a>
        <br><br>
    """ % name
    f.write(h)
no = 1
for u in url_list:
    html = requests.get(u).text
    tree = etree.HTML(html)
    for ud in tree.xpath('/html/body/div/div[2]/div[2]/table//tr/td[5]/a/@href'):
        ud = 'http://cubesolv.es'+ud
        html = requests.get(ud).text
        tree = etree.HTML(html)
        title = ''.join(tree.xpath(
            '/html/body/div/div[2]/h2//text()')).replace('\n', '').replace('  ', ' ')
        title = re.sub('^\s+|\s+$', '', title)
        scramble = ''.join(tree.xpath(
            '/html/body/div/div[2]/div[1]/div[1]/div[1]//text()')).replace('\n', '').replace('  ', ' ')
        scramble = re.sub('^\s+|\s+$', '', scramble)
        solution = ''
        for i in tree.xpath(
                '/html/body/div/div[2]/div[1]/div[1]/div[2]//text()'):
            i = re.sub('^\s+|\s+$', '', i)
            if i.startswith('//'):
                i = i+'\n'
                i = re.sub('//\s+', ' //', i)
            solution += i
        url = 'alg/index.html?setup=%s&alg=%s&title=%s'
        title_u = urllib.parse.quote(title)
        scramble_u = scramble.replace(' ', '_').replace("'", '-')
        scramble_u = urllib.parse.quote(scramble_u)
        solution_u = solution.replace(' ', '_').replace("'", '-')
        solution_u = urllib.parse.quote(solution_u)
        solution_u = solution_u.replace('//', '%2F%2F')
        url = url % (scramble_u, solution_u, title_u)
        print(ud)
        with open('%sExample.html' % name.replace(' ', ''), mode='a', encoding='utf-8') as f:
            h = """
                <h2 id='%d'>%d | %s</h2>
                <h3><a href = '%s' target="_blank">Scramble</a> %s</h3>
                <h3><a href = '%s' target="_blank">Solution</a></h3>
                <div>%s</div>
                <br/>
                <br/>
            """ % (no, no, title, ud, scramble, url, solution.replace('\n', '<br />'))
            no += 1
            f.write(h)
