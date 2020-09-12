# -*- coding: utf-8 -*-
# https://a.mapillary.com/v3/sequences?client_id=<client_id>&per_page=100&usernames=microsoft
  

# https://a.mapillary.com/v3/sequences/dpGEtcThvmdSi61APNEo4w?client_id=<client_id>
# dpGEtcThvmdSi61APNEo4w

# https://images.mapillary.com/6kKei5Vja38THl7YLsv8Ur/thumb-2048.jpg
import glob
import os
import json
import urllib.request
import os
from threading import Thread
import time
import client_id
# client_id = '<client_id>'
# per_page = 1000
class MapillaryDownload(object):
    def __init__(self, client_id):
        # your mapillary client_id
        self.client_id = client_id

    # microsoft has 1.1m 360 degree img in mapillary
    # get_sequences_by_username('microsoft', '/home/data/mapillary_seq/', 40000, 1000)
    # per_page max = 1000
    def get_sequences_by_username(self, usernames, foldpath, img_need=5000, per_page=200):
        url = 'https://a.mapillary.com/v3/sequences?client_id='+client_id+'&per_page='+str(per_page)+'&usernames='+usernames
        image_count = 0
        while url:
            data = urllib.request.urlopen(url)
            data_json = json.loads(data.read().decode('utf-8'))
            for seq in data_json['features']:
                file_name = seq['properties']['key']
                image_num = len(seq['properties']['coordinateProperties']['image_keys'])
                if image_num >= 100:
                    image_count = image_count + image_num
                    if not os.path.isfile(foldpath+file_name+'.txt'):
                        with open(foldpath+file_name+'.txt', 'w') as f:
                            json.dump(seq, f)
                            print(file_name)
                if image_count >= img_need:
                    break
            if image_count >= img_need:
                break
            url = data.getheader('link').split('<')[-1].split('>')[0]
        print(image_count)

    # file from get_sequences_by_username() function
    def download_from_json_file(self, json_filepath, outfoldpath):
        with open(json_filepath) as fp:
            data = json.load(fp)
        fdpt = outfoldpath+data['properties']['key']
        contents = data['properties']['coordinateProperties']['image_keys']
        if not os.path.isdir(fdpt):
            os.mkdir(fdpt)
            def download(code, count):
                if not os.path.isfile('./'+code+'.jpg'):
                    try:
                        urllib.request.urlretrieve('https://images.mapillary.com/'+code+'/thumb-2048.jpg', fdpt+'/'+code+'.jpg' )
                        print(str(count)+" : "+ code+'.jpg downloaded')
                    except Exception as e:
                        print(e)
                else:
                    print("img saved")
            
            all_num = len(contents)
            start = time.time()

            thr_num = 24

            times = int(all_num/thr_num + 1)

            count = 0
            for i in range(times):
                start2 = time.time()
                threads = []
                for code in contents[i*thr_num:(i+1)*thr_num]:
                    t = Thread(target = download, args = [code,count])
                    t.start()
                    threads.append(t)
                    count += 1
                for t in threads:
                    t.join()
                end2 = time.time()
                print('This process cost：',end2 - start2,'s')
            end = time.time()

            print('Finish: ', str(end - start) +' Download: '+ str(count) + 'image')
            print('Rename filename:')
            num = 0
            for code in contents:
                os.rename(fdpt+'/'+code+'.jpg' ,fdpt+'/'+"{0:0=10d}".format(num)+'.jpg')
                num = num + 1
            print(data['properties']['key']+' done ! ')
        else:
            print(fdpt,'exsisted!')

    # file from get_sequences_by_username() function
    def download_from_json_fold(self, json_foldpath, outfoldpath):
        # outfoldpath = '/home/deng/data/mapillary_data/'
        # json_foldpath = '/home/deng/data/mapillary_seq/'
        for filepath in glob.glob(json_foldpath+'*.txt'):
            print(filepath)
            download_from_json_file(filepath, outfoldpath)

    # make a split file for Machine Learning training dataset
    # make_split_file(foldpath,split_output)
    # foldpath = '/home/data/mapillary_data/'
    # split_output = './mapillary_split/'
    def make_split_file(self, foldpath, split_output):
        for fold in glob.glob(foldpath+'/*'):
            path_num = len(glob.glob(fold+'/*'))
            for path in glob.glob(fold+'/*'):
                tp = path.split('mapillary_data/')[-1].split('/')
                fp = tp[0]
                frame_num = str(int(tp[1].split('.')[0]))
                if frame_num != '0' and frame_num != str(path_num-1):
                    with open(split_output+'train_files.txt', 'a') as f:
                        f.write(fp+' '+frame_num + ' r' +'\n')



if __name__ == "__main__":
    md = MapillaryDownload(client_id.client_id)
    md.get_sequences_by_username('microsoft', '/home/data/mapillary_seq/', 40000, 1000)
    md.download_from_json_fold('/home/deng/data/mapillary_seq/', '/home/deng/data/mapillary_data/')
    md.make_split_file('/home/data/mapillary_data/', '../mapillary_split/')