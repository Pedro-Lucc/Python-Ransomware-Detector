import os
import itertools
import struct
import math
import fleep
from timeit import default_timer as timer


def shennon_entropy(frequency_list):
    ent = 0.0
    for freq in frequency_list:
        if freq > 0:
            ent = ent + freq * math.log(freq, 2)
    return -ent


def getFileExt(filePath):
    with open(filePath, "rb") as file:
        info = fleep.get(file.read(128))
    return info.extension


start = timer()
for root, dirs, files in os.walk("/home/matheusheidemann", topdown=False):
    print(root)
    for file_name in files:
        fp = os.path.join(root, file_name)

        file_size = os.path.getsize(fp)

        bytes_list = list(itertools.repeat(0, 256))
        with open(fp, "rb") as f:
            read_byte = f.read(1)
            # print(read_byte)
            counter = 0
            mb_counter = 0
            while read_byte != b"":
                # Do stuff with byte
                value = struct.unpack('B', read_byte)[0]  # Le o valor do byte
                bytes_list[value] += 1  # no valor do byte é incrementado 1
                # print(read_byte)
                # print(bytes_list[value])
                # print(bytes_list)
                counter += 1
                # print(counter)
                if counter == 1048576:
                    counter = 0
                    mb_counter += 1

                read_byte = f.read(1)
        if file_size > 0 and len(bytes_list) > 0:
            frequency_list = [float(elem)/file_size for elem in bytes_list]

        entropy = shennon_entropy(frequency_list)
        if file_name.count('.') >= 2 and entropy > 7.9 and len(getFileExt(fp)) == 0:
            print("Caution file: {} might be a ransomwareFile".format(file_name))

end = timer()
time_taken = end - start
print("A aplicação demorou cerca de {} segundos {} ficheiros".format(time_taken, len(files)))
