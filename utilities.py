import os
import shutil


def empty_folder(directory_name):
    if not os.path.isdir(directory_name):
        os.makedirs(directory_name)
    else:
        folder = directory_name
        for the_file in os.listdir(folder):
            file_path = os.path.join(folder, the_file)
            try:
                if os.path.isfile(file_path):
                    os.unlink(file_path)
                elif os.path.isdir(file_path):
                    shutil.rmtree(file_path)
            except Exception as e:
                print(e)


def list_dir(path):
    return os.listdir(path)


def restore():
    empty_folder('restored_file')
    meta_data = open('raw_data/meta_data.txt', 'r')
    meta_info = []
    for row in meta_data:
        temp = row.split('\n')
        temp = temp[0]
        temp = temp.split('=')
        meta_info.append(temp[1])
    address = 'restored_file/' + meta_info[0]

    list_of_files = sorted(list_dir('files'))

    with open(address, 'wb') as writer:
        for file in list_of_files:
            path = 'files/' + file
            with open(path, 'rb') as reader:
                for line in reader:
                    writer.write(line)
                reader.close()
        writer.close()

    empty_folder('files')


def divide():
    empty_folder('files')
    empty_folder('raw_data')
    FILE = list_dir('uploads')
    FILE = './uploads/'+FILE[0]

    MAX = 2048*32						# 2	MB	-	max chapter size
    BUF = 20*1024*1024*1024  			# 20GB	-	memory buffer size

    chapters = 0
    ugly_buffer = ''
    meta_data = open('raw_data/meta_data.txt', 'w')
    file__name = FILE.split('/')
    file__name = file__name[-1]
    print(file__name)
    meta_data.write("File_Name=%s\n" % file__name)
    with open(FILE, 'rb') as src:
        while True:
            target_file = open('files/SECRET' + '%07d' % chapters, 'wb')
            written = 0
            while written < MAX:
                if len(ugly_buffer) > 0:
                    target_file.write(ugly_buffer)
                target_file.write(src.read(min(BUF, MAX - written)))
                written += min(BUF, MAX - written)
                ugly_buffer = src.read(1)
                if len(ugly_buffer) == 0:
                    break
            target_file.close()
            if len(ugly_buffer) == 0:
                break
            chapters += 1
    meta_data.write("chapters=%d" % (chapters+1))
    meta_data.close()
