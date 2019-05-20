# -*- coding: utf-8 -*-

import random
import os
import addRandomUI


# 获取文件中 @end 的总数量
def GetMFileEndCount(file_path,old_str):
    file_data = ""
    #print('filePath------'+file_path)
    Ropen=open(file_path,'r')#读取文件
    flagCount = 0
    for line in Ropen:
        if old_str in line:#如果.h文件中的某一行里包含old_str,则往这一行添加一下语句
            flagCount += 1
    return flagCount   


# 对添加的垃圾代码进行调用
def CallRubbishMethods(methods,Ropen,dir_path):
    flagCount = 0       #记录当前行数
    writeLineNumber = 0 #记录应该在哪一行调用
    file_data = ""
    isfound = False
    header = ""
    while True:
        line = Ropen.readline()
        if not line:
            break
        flagCount = flagCount + 1
        if "- (void" in line and isfound == False:     #目前还有个问题，就是代码无法准确地添加在正确地位置
            writeLineNumber = flagCount
            file_data += line
        elif writeLineNumber > 0 and isfound == False: #找到了‘{’的位置
            if "{" in line:
                for method in methods:
                    line += addRandomUI.switcher(method['name'], method['params'])
                isfound = True
                classBody = addRandomUI.generateClass(dir_path)
                caller = classBody['caller']
                className = classBody['name']
                header += "#import \"" + className + ".h\"\n"
                line += caller
            file_data += line
        else:
            file_data += line
    file_data = header + file_data
    return file_data



#.h文件添加废代码
def HFileAddCode(file_path,old_str,endTotalCount):
    # .h文件里属性的类型从这个数组里随机选
    classArray = ['NSString', 'UILabel', 'NSDictionary', 'NSData', 'UIScrollView', 'UIView', 'UITextView',
                  'UITableView', 'UIImageView']
    file_data = ""
    Ropen=open(file_path,'r')
    flagCount = 0
    for line in Ropen:
        nameStr = addRandomUI.getRandomStr(6, 10)
        className = random.choice(classArray)

        if old_str in line:
            flagCount += 1
            if flagCount==endTotalCount:
                file_data += '\n@property(nonatomic,strong) '+className +' *'+nameStr+';\n'
            file_data += line
        else:
            file_data += line
    Ropen.close()
    #Wopen=open(file_path,'w')
    #Wopen.write(file_data)
    #Wopen.close()

   
    
#.m文件添加垃圾代码
def MFileAddCode(file_path,old_str,endTotalCount):

    file_data = ""
    print('filePath------'+file_path)
    Ropen=open(file_path,'r')#读取文件
    callMethods = []
    flagCount = 0
    for line in Ropen:
        if old_str in line:
            flagCount += 1
            # 在最后一个 '@end' 前面加上垃圾代码
            if flagCount==endTotalCount:
                methodBody = addRandomUI.addRandomClass()
                file_data += methodBody['str'] + '\n\n'
                callMethods.append(methodBody)
            file_data += line
        else:
            file_data += line
    Wopen=open(file_path,'w')
    Wopen.write(file_data)
    Wopen.close()
    
    Ropen.seek(0)
    dir_path = file_path[0:file_path.rfind("/")+1]
    result = CallRubbishMethods(callMethods, Ropen, dir_path)
    Wopen=open(file_path,'w')
    Wopen.write(result)
    Ropen.close()
    


def addCode(file_path):
    global codeCount
    if '.h' in file_path:  # file_dir+'/'+file含义是file_dir文件夹下的file文件
        # 获取文件中 @end 的总数量，在最后一个 @end 前面添加垃圾代码
        hCount = GetMFileEndCount(file_path,"@end")
        for num in range(codeCount):
            HFileAddCode(file_path, "@end", hCount)
  
    if '.m' in file_path:
        mCount = GetMFileEndCount(file_path,"@end")
        for num in range(codeCount):
            MFileAddCode(file_path, "@end", mCount)
        

# 循环递归遍历文件夹
def traverse(file_dir):
    fs = os.listdir(file_dir)
    for dir in fs:
        tmp_path = os.path.join(file_dir, dir)
        if not os.path.isdir(tmp_path):
            addCode(tmp_path)
        else:
            # 是文件夹,则递归调用
            traverse(tmp_path)


def addRubbish():
    global codeCount
    # 每个文件中添加的代码数量
    codeCount = 2
    # 主工程目录
    file_prefix = '../HDLCProject/'
    # 要添加垃圾代码文件所在的文件夹路径
    file_dirs = ['HDLC/RunView']
    for dir in file_dirs:
            file_dir = file_prefix + dir
            traverse(file_dir)
        

def main():
    addRubbish()
    print('添加垃圾代码完成，请在提交代码前尝试运行检查代码并相应调整')


if __name__ == '__main__':
    main()
