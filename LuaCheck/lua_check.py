import sublime, sublime_plugin
import subprocess
import re,os,sys

def check(path):
	#print(sublime.packages_path())
	if not re.search(r".lua$",path):
		print("not lua")
		return
	p = subprocess.Popen('E:/lua/luac.exe '+path, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
	error=""
	for line in p.stdout.readlines():
		error=error+line.decode("utf8")
	retval = p.wait()
	if retval != 0:
		sublime.message_dialog(error)

class LuacheckCommand(sublime_plugin.TextCommand):
	def run(self, edit):
		check(self.view.file_name())

class LuaCheck(sublime_plugin.EventListener):
	def on_post_save(self, view): #on_post_save_async
		check(view.file_name())
 