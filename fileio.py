file=open("file.txt","w+")

file.write("Hello World")


file.seek(0)
data=file.read()
print(data)
file.close()