#!/usr/bin/env bash
# Created By Vanch at 2018/10/6

#定义全局变量
filePath=
#输入文件路径
inputFile() {
    readSuccess=false
    #首先清空变量值
    filePath=
    while [ $readSuccess = false ]; do 
        echo $1
        #读取到变量中
        read -a filePath
        if [[ ! -e $filePath || ${filePath##*.} != $2 ]]; then
            echo "Input file is not ."$2
        else
            readSuccess=true
        fi
    done
}

checkUUID() {
    uuid=`dwarfdump --uuid $2`
    #echo $uuid
    return 0;
}

# 先查找symbolicatecrash解析工具，内置在Xcode的库文件中
# 不同版本的Xcode，位置不同，所以需要find查找具体位置
toolPath=`find /Applications/Xcode.app/Contents/SharedFrameworks -name symbolicatecrash | head -n 1`
if [ ! -f $toolPath ]; then
    echo "Symbolicatecrash not exist!"
    exit 0
fi

#要求输入crash文件路径
inputFile 'Please Input Crash File' 'crash'
crashPath=$filePath

dsymSuccess=false
while [ $dsymSuccess = false ]; do
    #要求输入dSYM文件路径
    inputFile 'Please Input dSYM File' 'dSYM'
    dsymPath=$filePath
    #检查是否匹配
    checkUUID $crashPath $dsymPath
    match=$?
    echo 'match is '$match
    if [ $match -eq 0 ]; then
        echo 'UUID not match!'
    else
        dsymSuccess=true
    fi
done
echo "done"
exit 0
#先设置环境变量
export DEVELOPER_DIR="/Applications/Xcode.app/Contents/Developer"
#指定解析结果路径
crashName=`basename $crashPath`
afterPath=`dirname $crashPath`/${crashName%%.*}'_after.crash'
echo $afterPath
#开始解析
#$toolPath $crashPath $dsymPath > $afterPath 