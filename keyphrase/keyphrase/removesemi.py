ft=open("/home/project/xx/keyphrase/output/algo2_tfidf.txt")
raw=ft.read()
r=":"
raw1="hello:::"
print(raw)
raw1=raw1.replace(":::","::")
print(raw1[-1])
print(r[0])
if raw1[-1]==':':
	print("true")
ft.close()
ft=open("/home/project/xx/keyphrase/output/algo2_tfidf.tx","w")
ft.write(raw)

