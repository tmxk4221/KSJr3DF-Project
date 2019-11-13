# 윈도우 이미지 자동화 도구 Code #


import os
from os import path
import sys
import urllib.request
import requests
from tqdm import tqdm
import subprocess

# URL 저장 경로 지정
W7_url_1 = "http://207.148.109.78/W7.part1.exe"
W7_url_2 = "http://207.148.109.78/W7.part2.rar"
WS12_url_1 = "http://207.148.109.78/WS12.part1.exe"
WS12_url_2 = "http://207.148.109.78/WS12.part2.rar"

# 저장할 파일이름
savename_W7_url_1 = path.expandvars(r'%APPDATA%\5drone\W7.part1.exe')
savename_W7_url_2 = path.expandvars(r'%APPDATA%\5drone\W7.part2.rar')
savename_WS12_url_1 = path.expandvars(r'%APPDATA%\5drone\WS12.part1.exe')
savename_WS12_url_2 = path.expandvars(r'%APPDATA%\5drone\WS12.part2.rar')

# VM Image가 저장될 환경 변수 경로
ovf_source_W7 = path.expandvars(r'%appdata%\5drone\5drone_Win7x64.ovf')
ovf_source_WS12 = path.expandvars(r'%appdata%\5drone\5drone_WinServer2012.ovf')
appdata_W7 = path.expandvars(r'%appdata%\5drone\5drone_Win7x64\5drone_Win7x64.vmx')
appdata_WS12 = path.expandvars(r'%appdata%\5drone\5drone_WinServer2012\5drone_WinServer2012.vmx')

# ovftool
ovftool = path.expandvars(r'%ProgramFiles(x86)%\VMware\VMware Workstation\OVFTool\ovftool.exe') 

# vmrun
vmrun = path.expandvars(r'%ProgramFiles(x86)%\VMware\VMware Workstation\vmrun.exe')

# 인자로 받기
def receive_argu(string):
    if (string == 1):
        print("Detecting Windows Images that already exists ...")
        if(os.path.isfile(appdata_W7) == False):
            print("Download Windows 7 Images from server")
            download_WIN7()
            os.system(savename_W7_url_1)
            subprocess.call([ovftool,ovf_source_W7,appdata_W7])
        print("Windows 7 Images Detected. Starting....")
        subprocess.run([vmrun,'-T','ws','start',appdata_W7])
    elif (string == 2):
        print("Detecting Windows Server Images that already exists ...")
        if(os.path.isfile(appdata_WS12) == False):
            print("Download Windows Server Images from server")
            download_WINSERVER2012()
            os.system(savename_WS12_url_1)
            subprocess.call([ovftool,ovf_source_WS12,appdata_WS12])
        print("Windows Server 2012 Images Detected. Starting....")
        subprocess.run([vmrun,'-T','ws','start',appdata_WS12])
    else:
        print("Invalid Argument !!!")

# 다운로드 함수
def download_file(url):
    if (url == W7_url_1):
        local_filename = savename_W7_url_1
    elif (url == W7_url_2):
        local_filename = savename_W7_url_2
    elif (url == WS12_url_1):
        local_filename = savename_WS12_url_1
    elif (url == WS12_url_2):
        local_filename = savename_WS12_url_2
    else:
        print("Invalid Argument !!!")

    r = requests.get(url, stream=True)
    r.raise_for_status()
    total_size = int(r.headers.get('content-length',0))
    t = tqdm(total=total_size, unit='iB', unit_scale=True)
    with open(local_filename, "wb") as f:
        for data in r.iter_content(chunk_size=8192):
            t.update(len(data))
            f.write(data)
    t.close()
    r.close()
    return

# 인자별 다운로드
def download_WIN7():
    download_file(W7_url_1)
    print("=========== Windows 7 VM Image Download Complete 1/2 ===========")
    download_file(W7_url_2)
    print("=========== Windows 7 VM Image Download Complete 2/2 ===========")

def download_WINSERVER2012():
    download_file(WS12_url_1)
    print("=========== Windows Server 2012 VM Image Download Complete 1/2 ===========")
    download_file(WS12_url_2)
    print("=========== Windows Server 2012 VM Image Download Complete 2/2 ===========")

# main
if __name__ == '__main__':
    print("======== Windows VM Image Auto Download & Converter ========")

    print("Detecting OVFTool ...")
    if(os.path.isfile(ovftool) == False):
        print("OVFTool not Installed. Reinstall VMWare Workstation.")
        exit(0)

    print("Detecting VMRun ...")
    if(os.path.isfile(vmrun) == False):
        print("VMRun not Installed. Reinstall VMWare Workstation.")
        exit(0)
      
    receive_argu(int(sys.argv[1]))
