import os


index = 1
dir = "/home/matheusheidemann/Documents/Github/Python-Ransomware-Detector/ransomware-samples/encrypt-test"
with open("/home/matheusheidemann/Documents/Github/Python-Ransomware-Detector/ransomware-samples/1mb_template_file.txt", 'r') as file_bytes:
    file_data = file_bytes.read()


while index <= 3:
    cdir = f"{str(dir)}/folder{str(index)}"
    os.makedirs(cdir + "/files")
    index += 1

dirlist = []
for root, dir, file in os.walk(dir):
    if "encrypt-test" in root and "files" in root:
        dirlist.append(root)
print(dirlist)
index = 1

for dir in dirlist:
    print(dir)
    while index <= 100:
        with open(dir + '/' + 'file' + str(index) + ".txt", 'w') as file:
            file.write(file_data)
            print(dir)
        index += 1
    index = 1
