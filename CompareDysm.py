#! /usr/bin/env python3

import os
import sys

def findFile(path, name) :
    for dic_name in os.listdir(path) :
        sub_path = os.path.join(path, dic_name)
        if os.path.isfile(sub_path) :
            if dic_name == name :
                return sub_path
        if os.path.isdir(sub_path) :
            result = findFile(sub_path, name)
            if result : return result

def checkUUID(dysm, crash) :
    # 取uuid
    for uuidline in os.popen('dwarfdump --uuid ' + dysm).readlines():
        arm = uuidline.find(' (arm64)')
        if arm > 6:
            uuid = uuidline[6:arm]
            break
    uuid = uuid.replace('-','').lower()

    # 读取crash日志查找uuid
    crashfile = open(crash, 'r')
    hasfind = 0
    for line in crashfile:
        if line.find(uuid) > -1:
            hasfind = 1
            break
    return hasfind

def main() :
    #本地查找Symbolicatecrash
    filelist = findFile('/Applications/Xcode.app/Contents/SharedFrameworks', 'symbolicatecrash')
    if not filelist :
        print('Not Found Symbolicatecrash')
        print('Press Enter To Exit')
        sys.stdin.readline()
        exit()

    #设置环境变量
    os.environ["DEVELOPER_DIR"] = "/Applications/Xcode.app/Contents/Developer"

    #插件设定UUID
    #os.system('find ~/Library/Application\ Support/Developer/Shared/Xcode/Plug-ins -name Info.plist -maxdepth 3 | xargs -I{} defaults write {} DVTPlugInCompatibilityUUIDs -array-add `defaults read /Applications/Xcode.app/Contents/Info.plist DVTPlugInCompatibilityUUID`')

    #输入Crash文件
    print('Please Input Crash File')
    inputcrash = sys.stdin.readline()[:-1].strip()
    crash = inputcrash.replace('\\','')
    while (os.path.splitext(crash)[1] != '.crash') :
        print('Please Input Correct Crash File')
        inputcrash = sys.stdin.readline()[:-1].strip()
        crash = inputcrash.replace('\\', '')

    #定义输出文件名
    afterFile = inputcrash[:-6]
    afterFile += '_afterparse.crash'

    #输入Dysm文件
    print('Please Input Dysm File')
    inputdysm = sys.stdin.readline()[:-1].strip()
    dysm = inputdysm.replace('\\','')
    while (checkUUID(dysm, crash) == 0) :
        print('Please Input Correct Dysm File')
        inputdysm = sys.stdin.readline()[:-1].strip()
        dysm = inputdysm.replace('\\', '')

    #执行解析
    os.system(filelist + ' ' + inputcrash + ' ' + inputdysm + ' > ' + afterFile)

    print('Program Complete')

    return

if __name__ == '__main__' : main()