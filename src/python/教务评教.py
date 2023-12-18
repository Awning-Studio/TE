import requests, bs4

USERNAME = ""
PASSWORD = ""

root = "http://jwxt.gdufe.edu.cn"
base = "/jsxsd"
verify_code = "/verifycode.servlet"
login_ = "/xk/LoginToXkLdap"
list_ = "/xspj/xspj_find.do"
evaluate = "/xspj/xspj_save.do"

session = requests.Session()

# 登录
def login():
	session.get(root + base)

	res = session.get(root + base + verify_code)

	with open("code.png", 'wb') as file:
		file.write(res.content)
	
	code_content = input("输入存于当前目录下的验证码: ")

	data = {
		"USERNAME": USERNAME,
		"PASSWORD": PASSWORD,
		"RANDOMCODE": code_content
	}

	res = session.post(root + base + login_, data=data)
	soup = bs4.BeautifulSoup(res.text, "html.parser")
	if soup.find("title").text == "学生个人中心":
		print("登录成功")
		return True
	else:
		print(f"登录失败: {soup.find('font').text}")
		return False


# 获取课程列表
def getList():
	params = {
		"Ves632DSdyV": "NEW_XSD_JXPJ"
	}
	res = session.get(root + base + list_, params=params)
	soup = bs4.BeautifulSoup(res.text, "html.parser")

	table = soup.find("table", class_="Nsb_r_list Nsb_table")
	rows = table.find_all("tr")
	if len(rows) < 2:
		print("当前不在选课时间")
		return []
	else:
		items = rows[1].find_all("td")[6].find_all("a")

		l = []
		for item in items:
			sort = item.text

			url = root + item["href"]
			res = session.get(url)

			soup = bs4.BeautifulSoup(res.text, "html.parser")
			infoList = soup.find("table", id="dataList").find_all("tr")

			for index in range(1, len(infoList)):
				info = infoList[index].find_all("td")
				print(info[7].find("a"))
				try:
					l.append({
						"id": info[1].text,
						"name": info[2].text,
						"teacher": info[3].text,
						"sort": sort,
						"url": info[7].find("a")["onclick"][7:-12]
					})
				except:
					continue
		return l


# 登录
if login():
	# 获取课程列表
	l = getList()
	for item in l:
		print(f"{item['id']} {item['name']} {item['teacher']} {item['sort']}")
		
		# 进入课程进行评教
		res = session.get(root + item["url"])
        # 构建表单
		form = []
		soup = bs4.BeautifulSoup(res.text, "html.parser")
		table = soup.find("form", id="Form1")
		children = table.find_all("input")
		
		b = False
		for i in range(len(children) - 3):
			if i < 10:
				if i == 0:
					form.append(("issubmit", "1"))
					continue
				form.append((children[i]["name"], children[i]["value"]))
			else:
				sub = i - 10

				mod = sub % 11
				if mod == 0:
					b = (sub + 1) % 2 == 0

				if (b and sub % 2 == 0) or (not b and sub % 2 != 0):
					continue
				
				if mod == 2:
					form.append((children[i - 1]["name"], children[i - 1]["value"]))

				form.append((children[i]["name"], children[i]["value"]))

		res = session.post(root + base + evaluate, data=form)
