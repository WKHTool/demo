#导入一些需要库
import os	#os库，这里用到了路径和目录相关的功能
from lxml import etree #使用到了lxml中etree对象，用于解析网页
import requests as reqs #用于完成网络请求的处理
import re 	#正则表达式
import urllib #用到了urllib中关于url的一些功能
import uuid #用于生存uuid（全局唯一）标识符，在没有文件名的时候，用作文件名。

#类型与后缀名的对应关系
typeMapping = {
	"jpeg":".jpg"
	,"gif":".gif"
	,"x-icon":".icon"
	,"fax":".fax"
	,"tiff":".tif"
	,"pnetvue":".net"
	,"png":".png"
	,"vnd.rn-realpix":".rp"
	,"vnd.wap.wbmp":".wbmp"
	,"x-bmp":".bmp"
	,"x-png":".png"
}

strUrl = r"http://www.cswu.cn"
domainParseRes = urllib.parse.urlparse(strUrl)

page = reqs.get(strUrl)
headers = page.request.headers
#headers["Host"] = domainParseRes.netloc
#headers["Referer"] = strUrl
headers["User-Agent"] = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36"
headers["Accept"] = "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8"
if page.status_code != 200:
	print("status code is not 200")
	exit()

html = etree.HTML(page.content.decode("utf-8"))
imageList = [i for i in html.xpath(r"//img/@src")]
imageList += [i for i in html.xpath(r"//image/@src")]
imageList = list(set(imageList))

folderName = html.xpath(r"/html/head/title/text()")
print(folderName)
folderName = folderName[0] if len(folderName) != 0 else "imageFolder"
filterChars = ["\n","\r","?","<",">","?",":","\\","/","|","*",'"']
for i in filterChars:
	folderName = folderName.replace(i,"")
print(folderName)
print("图片链接数:",len(imageList))

strPath = os.path.abspath(r".")
strPath = os.path.join(strPath,folderName)
if not os.path.exists(strPath):
	os.mkdir(strPath)

rex = re.compile(r"[^/]+$")

for i in imageList:
	parseRes = urllib.parse.urlparse(i)
	if parseRes.netloc == "":
		i = domainParseRes.scheme + "://" + domainParseRes.netloc + i
	elif parseRes.scheme == "":
		i = domainParseRes.scheme + ":" + i

	try:
		imgHeaders = headers.copy()
		imgHeaders["authority"] = domainParseRes.netloc
		imgHeaders["path"] = parseRes.path
		imgHeaders["scheme"] = parseRes.scheme
		img = reqs.get(i,cookies = page.cookies,headers = headers)
	except Exception as e:
		print("a exception had occured when download image {url}".format(url = i))
		continue

	if img.status_code != 200:
		print("status_code = {code} : {url} download image had failed".format(code = img.status_code,url=i))
		continue

	filename = rex.findall(i)[0]
	if re.match(r"[^.]+\.\w{3,4}$",filename) == None:
		filename = ""

	if filename == "":
		filename = str(uuid.uuid1()).replace("-","")
		fileTypes = img.headers.get("content-type","").lower().split("/")
		if len(fileTypes) == 0:
			continue
		if fileTypes[0] != "image" and fileTypes[0]  != "application":
			continue
		fileExt = typeMapping.get(fileTypes[1],"")
		if fileExt == "":
			continue
		filename += fileExt

	filename = urllib.parse.unquote(filename)
	print(filename)
	filepath = os.path.join(strPath,filename)
	with open(filepath,"wb") as f:
		f.write(img.content)
