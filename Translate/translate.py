import sublime, sublime_plugin
import json
import http.client
import hashlib
import urllib
import random
import urllib.request
appid = '20161014000030208'
secretKey = '0SHUHXhYhEUDsQu8wxgl'
httpClient = None

#q = 'apple'
fromLang = 'auto'
toLang = 'auto'
salt = random.randint(32768, 65536)

def GetTranslate(q):
	result=""
	myurl = '/api/trans/vip/translate'
	sign = appid+q+str(salt)+secretKey
	m1 = hashlib.md5()
	m1.update(sign.encode("utf8"))
	sign = m1.hexdigest()
	myurl = myurl+'?appid='+appid+'&q='+urllib.request.quote(q)+'&from='+fromLang+'&to='+toLang+'&salt='+str(salt)+'&sign='+sign
	 
	try:
		httpClient = http.client.HTTPConnection('api.fanyi.baidu.com')
		httpClient.request('GET', myurl)
	 
		#response是HTTPResponse对象
		response = httpClient.getresponse()
		
		re=response.read().decode("utf8")
		json_obj=json.loads(re)
		print (re)
		print(json_obj["trans_result"][0]["dst"])
		result =json_obj["trans_result"][0]["dst"]

	except Exception as e:
		print (e)
	finally:
		if httpClient:
			httpClient.close()
	return result


def ShowTranslate(view,word):
	result=GetTranslate(word)
	def cb():
		print("haha")  
	#view.show_popup_menu("aa", cb) 
	str1='''<body id="my-plugin-feature">
		<style>
			div.error {
				background-color: black;
				border-radius:3;
				padding: 10px;
			}
		</style>
		<div class="error">%s</div>
	</body>'''%(result)
	view.show_popup(str1, sublime.COOPERATE_WITH_AUTO_COMPLETE | sublime.HIDE_ON_MOUSE_MOVE_AWAY , -1, 300, 100, cb, cb) 
class TranslateCommand(sublime_plugin.TextCommand):
	def run(self, edit):
		#self.view.insert(edit, 0, "Hello, World!")
		view=self.view
		sel = view.sel()[0]
		last_line,last_col = view.rowcol(sel.begin())
		#print(str(last_line)+"  "+str(last_col) )
		p=view.text_point(last_line, last_col)
		rect=view.word(p)
		word=view.substr(rect)
		
		ShowTranslate(view,word)

class Translate(sublime_plugin.EventListener):
	def on_pre_save(self, view):
		#print("hello3")
		a=10

	def on_hover(self,view, point, hover_zone):
		rect=view.word(point)
		word=view.substr(rect)
		#ShowTranslate(view,word)
		#print(view.substr(rect))

	def on_modified(self,view):
		sel = view.sel()[0]
		last_line,last_col = view.rowcol(sel.begin())
		#print(str(last_line)+"  "+str(last_col) )
		def cb(a):
			print("haha")  
		#view.show_popup_menu("aa", cb) 
		str1='''<body id="my-plugin-feature">
			<style>
				div.error {
					background-color: red;
					padding: 115px;
				}
			</style>
			<div class="error"></div>
		</body>'''
		#view.show_popup(str1, sublime.COOPERATE_WITH_AUTO_COMPLETE | sublime.HIDE_ON_MOUSE_MOVE_AWAY , -1, 500, 500, cb, cb) 
	def on_query_completions(self,view, prefix, locations):
		print(prefix)
		return [
			["fn", "def ${1:name}($2) { $0 }"],
			["for", "for ($1; $2; $3) { $0 }"],
			["for", "for ($1; $2; $3) { $0 }"]
		]

class ViewSelCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        self.show_selections()
        print(self.get_single_selection())
        print(self.get_multiple_selections())
        print(self.get_cursor_position())
        pass

    # 打印所有选区.
    def show_selections(self):
        print(x for x in self.view.sel())

    # 获取唯一的选区( sel()返回的List一定不为空, 失去焦点时, 选区为文件头, 即(0, 0) ).
    def get_single_selection(self):
        return self.view.sel()[0]

    # 获取所有选区.
    def get_multiple_selections(self):
        return self.view.sel()

    # 获取当前光标的位置.
    def get_cursor_position(self):
        region = self.view.sel()[0]
        return region.end()
