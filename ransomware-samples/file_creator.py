index = 0
dir = "/home/matheusheidemann/Documents/Github/Python-Ransomware-Detector/ransomware-samples/encrypt-test/file"
with open("/home/matheusheidemann/Documents/Github/Python-Ransomware-Detector/ransomware-samples/text_file.txt", 'r') as file_bytes:
    file_data = file_bytes.read()
while index < 100:
    with open(dir + '/' + 'file' + str(index) + ".txt", 'w') as file:
        file.write(file_data)
    index += 1
