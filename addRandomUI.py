# -*- coding: utf-8 -*-

import random


# 产生一个satrtIndex到endIndex位长度的随机字符串
def getRandomStr(satrtIndex,endIndex):
    numbers = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
    # random.choice()从列表中返回一个随机数
    final = (random.choice(numbers))
    # 从(50,100)列表中取出一个随机数
    index = random.randint(satrtIndex, endIndex)
    for i in range(index):
        final += (random.choice(numbers))
    return final

#生成名称
def generateNameWithWords(wordNum, needPreix = False,needSuffix = False):
    preix = ["Check", "Update", "Modify", "Add", "Del", "Set", "Send", "Call", "JJ", "HD", "LC", "CQ"]
    words = ["XiaoMi","wechat","verify","user","trade","text","template","square","share","security","search","scroll","scope",
    "salary","regist","record","recharge","reach","random","profile","product","prod","player","photo","phone","payback",
    "passport","paid","page","objc","normal","network","name","module","mine","metadata","message","member","logout","login",
    "logger","location","level","letter","investment","interface","intent","integral","instance","info","image","home","handle",
    "guide","gift","gesture","generate","form","force","flag","finance","file","figure","fields","feature","event","ecnomic",
    "twice","dialog","device","delay","deep","deal","data","cursor","control","container","console","component","client","click",
    "circle","change","calendar","business","border","bitmap","benefit","base","audio","attribute","assets","application","alipay",
    "alert","address","action","account"]
    suffix = ["Model", "Provider", "Manager", "VC", "ViewController", "View", "Delegate"]

    result= ""
    if needPreix:
        result = random.sample(preix, 1)[0]
    selectedWords = random.sample(words, wordNum)
    index = 0
    for word in selectedWords:
        if index == 0:
            result = result + word
        else:
            result = result + word.title()
        index = index + 1
    if needSuffix:
        result = result + random.sample(suffix, 1)[0]
    return result


def switcher(methodName,params,instanceName = ""):
    if len(params) == 0:
        if instanceName != "":
            if "show" in methodName:
                return "\t[" + instanceName + " " + methodName + "];\n"
            else:
                return "\tNSLog(@\"%@\", [" + instanceName + " " + methodName + "]);\n"
        else:
            if "show" in methodName:
                return "\t[self " + methodName + "];\n"
            else:
                return "\tNSLog(@\"%@\", [self " + methodName + "]);\n"
    if "show" in methodName:
        if instanceName != "":
            caller = "\t[" + instanceName + " " + methodName
        else:
            caller = "\t[self " + methodName
        endWith = "];\n"
    else:
        if instanceName != "":
            caller = "\tNSLog(@\"%@\",[" + instanceName + " " + methodName
        else:
            caller = "\tNSLog(@\"%@\",[self " + methodName
        endWith = "]);\n"
    index = 0
    for param in params:
        paramType = param['type']
        if paramType == "NSString":
            if index !=0:
                caller += " " + param['name'] + ":@\"" + generateNameWithWords(6) + "\""
            else:
                caller +=  ":@\"" + generateNameWithWords(6) + "\""
        elif paramType == "NSArray":
            num = random.randint(5, 10)
            strArr = ""
            for i in range(0,num):
                n = random.randint(0, 100)
                strArr += "@" + str(n) + ","
            if index !=0:
                caller += " " + param['name'] + ":@[" + strArr[:-1] + "]"
            else:
                caller += ":@[" + strArr[:-1] + "]"
        elif paramType == "BOOL":
            paramValue = "YES" if (random.randint(1,10) <=5) else "NO"
            if index !=0:
                caller += " " + param['name'] + ":" + paramValue
            else:
                caller += ":" + paramValue
        elif paramType == "NSNumber":
            paramValue = random.randint(1,10)
            if index !=0:
                caller += " " + param['name'] + ":@" + str(paramValue)
            else:
                caller += ":@" + str(paramValue)
        elif paramType == "CGFloat":
            paramValues = ["[UIScreen mainScreen].bounds.size.width","[UIScreen mainScreen].bounds.size.height",str(random.uniform(0,100))]
            paramValue = paramValues[random.randint(0,2)]
            if index !=0:
                caller += " " + param['name'] + ":" + paramValue
            else:
                caller += ":" + paramValue
        else:
            if index !=0:
                caller += " " + param['name'] + ":self"
            else:
                caller += ":self"
        index = index + 1
    caller += endWith
    return caller



#生成.h文件
def  generateHeaderFile(className,methods):
    headerString = '#import <UIKit/UIKit.h>\n\n'
    if 'VC' in className or 'ViewController' in className:
        headerString = headerString + '@interface ' + className + ' : UIViewController\n\n'
    elif 'View' in className:
        headerString = headerString + '@interface ' + className + ' : UIView\n\n'
    else:
        headerString = headerString + '@interface ' + className + ' : NSObject\n\n'
    index = random.randint(0,5)
    propType = ['NSString', 'NSArray', 'UIImage', 'NSDictionary']
    for i in range(0,index):
        headerString = headerString + '@property (strong, nonatomic) ' + random.sample(propType, 1)[0] + ' *' + generateNameWithWords(2) + ';\n'
    headerString = headerString + '\n'
    for method in methods:
        headerString = headerString + method['line']
    headerString = headerString + '\n@end'
    return headerString


#生成.m文件
def generateMainFile(className,methods):
    mainString = '#import \"' + className + '.h\"\n\n'
    mainString = mainString + '@interface ' + className + '()\n\n'
    mainString = mainString + '@end\n\n@implementation ' + className + "\n\n"
    if 'VC' in className or 'ViewController' in className:
        mainString = mainString + '- (void)viewDidLoad  {\n'
        for method in methods:
            mainString = mainString + switcher(method['name'],method['params'])
        mainString = mainString + '}\n\n'

    for method in methods:
        mainString = mainString + method['str'] + "\n\n"
    mainString = mainString + '\n\n@end'
    return mainString



#生成一个垃圾类
def generateClass(dirpath,preix = False):
    classBody = dict()
    #垃圾类的名字
    classBody['name'] = generateNameWithWords(2, True, True)
    methods = []
    #随机生成0到5个垃圾类方法
    index = random.randint(0,5)
    for num in range(0,index):
        section = random.randint(1, 10)
        if section == 1:
            method = addNSString()
        elif section == 2:
            method = addNSArray()
        elif section == 3:
            method = addNSData()
        elif section == 4:
            method = addNSDictionary()
        elif section == 5:
            method = addUIImage()
        else:
            method = addVoid()
        methods.append(method)
    classBody['methods'] = methods
    #生成.h文件
    WopenHeader=open(dirpath + classBody['name'] + '.h','w+')#读取文件
    headerFileString = generateHeaderFile(classBody['name'], methods)
    WopenHeader.write(headerFileString)
    WopenHeader.close()
    print "输出文件---" + classBody['name'] + '.h'

    #生成.h文件
    WopenMain = open(dirpath + classBody['name'] + '.m','w+')#读取文件
    mainFileString = generateMainFile(classBody['name'], methods)
    WopenMain.write(mainFileString)
    WopenMain.close()
    print "输出文件---" + classBody['name'] + '.m'

    #垃圾类的调用代码
    classBody['caller'] = generateInstanceAndCallMethod(classBody, methods)
    return classBody


#生成实例并调用垃圾实例
def generateInstanceAndCallMethod(classBody, methods = False):
    instanceName = classBody['name'][0].lower() + classBody['name'][1:]
    createInstanceString = "\t" + classBody['name'] + " *" +  instanceName + " = [[" + classBody['name'] + " alloc] init];\n"
    #遍历垃圾类重的方法
    for method in methods:
        needCaller = random.randint(0,10)
        if needCaller <= 8:
            caller = switcher(method['name'], method['params'],instanceName)
            createInstanceString = createInstanceString + caller + "\n"
    return createInstanceString



# 生成NSString方法
def addNSString():
    methodBody = dict()
    methodBodyName = generateNameWithWords(2)
    methodBody['name'] = "get" + methodBodyName + "String"
    methodBody['params'] = []
    paramNum = random.randint(0,3)
    for index in range(0,paramNum):
        methodBody['params'].append(randomParam())
    methodBody['line'] = '- (NSString *)' + methodBody['name']
    line = methodBody['line']
    index = 0
    for methodParam in methodBody['params']:
        paramString = generateParam(methodParam, index)
        methodBody['line'] += paramString
        line += paramString
    methodBody['line'] += ';\n'
    line += ' {\n'
    
    line += generateMethodCaller(methodBody['params'])
    stringName = "str" + methodBodyName
    string = 'NSString *' + stringName + ' = @"' + generateNameWithWords(6) + '";\n   return '+ stringName + ';\n}'
    methodBody['str'] = line+string + '\n\n'
    methodBody['caller'] = switcher(methodBody['name'], methodBody['params'])
    return methodBody

# 生成NSArray方法
def addNSArray():
    methodBody = dict()
    methodBodyName = generateNameWithWords(2)
    methodBody['name'] = "get" + methodBodyName + "Array"
    methodBody['params'] = []
    paramNum = random.randint(0,3)
    for index in range(0,paramNum):
        methodBody['params'].append(randomParam())
    methodBody['line'] = '- (NSArray *)' + methodBody['name']
    line = methodBody['line']
    index = 0
    for methodParam in methodBody['params']:
        paramString = generateParam(methodParam, index)
        methodBody['line'] += paramString
        line += paramString
        index = index + 1
    methodBody['line'] += ';\n'
    line += ' {\n'
    
    line += generateMethodCaller(methodBody['params'])

    arrayName = "arr" + methodBodyName
    arrayString = 'NSArray *' + arrayName + ' = @[\n'
    for i in range(1,15):
        element = '     @"' + generateNameWithWords(1) + '",\n'
        arrayString += element
    arrayString += '  ];\n    return ' + arrayName + ';\n}'
    methodBody['str'] = line + arrayString
    methodBody['caller'] = switcher(methodBody['name'], methodBody['params'])
    return methodBody


# 生成NSData方法
def addNSData():
    methodBody = dict()
    methodBodyName = generateNameWithWords(2)
    methodBody['name'] = "get" + methodBodyName + "Data"
    methodBody['params'] = []
    paramNum = random.randint(0,3)
    for index in range(0,paramNum):
        methodBody['params'].append(randomParam())
    methodBody['line'] = '- (NSData *)' + methodBody['name']
    line = methodBody['line']
    index = 0
    for methodParam in methodBody['params']:
        paramString = generateParam(methodParam, index)
        methodBody['line'] += paramString
        line += paramString
        index = index + 1
    methodBody['line'] += ';\n'
    line += ' {\n'
    
    line += generateMethodCaller(methodBody['params'])
    dataName = "data" + methodBodyName
    string = '\tNSData *' + dataName + ' = [@"' + generateNameWithWords(5) + '"' + ' dataUsingEncoding:NSUTF8StringEncoding]' + ';\n   return '+ dataName + ';\n}'
    methodBody['str'] = line+string
    methodBody['caller'] = switcher(methodBody['name'], methodBody['params'])
    return methodBody


# 生成NSArray方法
def addNSDictionary():
    methodBody = dict()
    methodBodyName = generateNameWithWords(2)
    methodBody['name'] = "get" + methodBodyName
    methodBody['params'] = []
    paramNum = random.randint(0,3)
    for index in range(0,paramNum):
        methodBody['params'].append(randomParam())
    methodBody['line'] = '- (NSDictionary *)' + methodBody['name']
    line = methodBody['line']
    index = 0
    for methodParam in methodBody['params']:
        paramString = generateParam(methodParam, index)
        methodBody['line'] += paramString
        line += paramString
        index = index + 1
    methodBody['line'] += ';\n'
    line += ' {\n'
    
    line += generateMethodCaller(methodBody['params'])

    dictName = generateNameWithWords(1)
    dictString = '\tNSDictionary *' + dictName + ' = @{\n'
    for i in range(1,random.randint(2,5)):
        element = '\t\t@"' + generateNameWithWords(1) + '" : ' + '@"' + generateNameWithWords(1) + '",\n'
        dictString += element
    for param in methodBody['params']:
        paramName = param['name']
        paramType = param['type']
        if paramType == "BOOL" or paramType == "CGFloat":
            element = '\t\t@"' + paramName + '" : @('  + paramName + '),\n'
        else:
            element = '\t\t@"' + paramName + '" : '  + paramName + ',\n'
        dictString += element
    dictString += '\t};\n\treturn ' + dictName + ';\n}'
    methodBody['str'] = line + dictString
    methodBody['caller'] = switcher(methodBody['name'], methodBody['params'])
    return methodBody


# 生成UIImage方法
def addUIImage():
    methodBody = dict()
    methodBodyName = generateNameWithWords(2)
    methodBody['name'] = "get" + methodBodyName
    methodBody['params'] = []
    paramNum = random.randint(0,3)
    for index in range(0,paramNum):
        methodBody['params'].append(randomParam())
    methodBody['line'] = '- (UIImage *)' + methodBody['name']
    line = methodBody['line']
    index = 0
    for methodParam in methodBody['params']:
        paramString = generateParam(methodParam, index)
        methodBody['line'] += paramString
        line += paramString
        index = index + 1
    methodBody['line'] += ';\n'
    line += ' {\n'
    
    line += generateMethodCaller(methodBody['params'])

    dataName = generateNameWithWords(2)
    imageName = generateNameWithWords(2) + "Image"
    string = '\tNSData *' + dataName + ' = [@"' + generateNameWithWords(5) + '"' + ' dataUsingEncoding:NSUTF8StringEncoding]' + ';\n'
    string += '\tUIImage *' + imageName + ' = [UIImage imageWithData:' + dataName + '];\n'
    string += '\treturn '+ imageName + ';\n}'

    methodBody['str'] =  line+string + '\n\n'
    methodBody['caller'] = switcher(methodBody['name'], methodBody['params'])
    return methodBody


#生成void的方法
def addVoid():
    methodBody = dict()
    methodBodyName = generateNameWithWords(2)
    methodBody['name'] = "show" + methodBodyName
    methodBody['params'] = []
    paramNum = random.randint(0,3)
    for index in range(0,paramNum):
        methodBody['params'].append(randomParam())
    #methodBody['paramType'] = "NSString"
    methodBody['line'] = '- (void)' + methodBody['name']
    line = methodBody['line']
    index = 0
    for methodParam in methodBody['params']:
        paramString = generateParam(methodParam, index)
        methodBody['line'] += paramString
        line += paramString
        index = index + 1
    methodBody['line'] += ';\n'
    line += ' {\n'

    #方法体内部，三个参数要被使用到
    line += generateMethodCaller(methodBody['params'])

    methodBody['str'] = line + '}\n\n'
    methodBody['caller'] = switcher(methodBody['name'], methodBody['params'])
    return methodBody


# 随机调用(addNSString(),addNSArray(),addNSData(),addNSDictionary(),addUIImage())中的某个函数
def addRandomClass():
    index = random.randint(1, 10)
    if index == 1:
        method = addNSString()
    elif index == 2:
        method = addNSArray()
    elif index == 3:
        method = addNSData()
    elif index == 4:
        method = addNSDictionary()
    elif index == 5:
        method = addUIImage()
    else:
        method = addVoid()
    return method

#生成一个随机的参数类型
def randomParam():
    param = dict()
    paramName = generateNameWithWords(2)
    paramIndex = random.randint(0,5)
    if paramIndex == 0:
        param['type'] = "BOOL"
        param['name'] =  paramName
    elif paramIndex == 1:
        param['type'] = "NSString"
        param['name'] = "str" + paramName
    elif paramIndex == 2:
        param['type'] = "NSNumber"
        param['name'] = "len" + paramName
    elif paramIndex == 3:
        param['type'] = "CGFloat"
        param['name'] = paramName + "Size"
    else:
        param['type'] = "id"
        param['name'] = "obj" + paramName
    return param

#生成方法参数列表
def generateParam(param, index):
    paramName = param['name']
    paramType = param['type']
    #参数类型为BOOL,NSString,NSNumber,CGFloat,id
    if paramType == "BOOL":
        if index != 0:
            return paramName + ":(BOOL)" + paramName + " "
        else:
            return ":(BOOL)" + paramName + " "
    elif paramType == "NSString":
        if index != 0:
            return paramName + ":(NSString *)"+paramName + " "
        else:
            return ":(NSString *)" + paramName + " "
    elif paramType == "NSNumber":
        if index != 0:
            return paramName + ":(NSNumber *)"+paramName + " "
        else:
            return ":(NSNumber *)"+paramName + " "
    elif paramType == "CGFloat":
        if index != 0:
            return paramName + ":(CGFloat)"+paramName + " "
        else:
            return ":(CGFloat)"+paramName + " "
    elif paramType == "id":
        if index !=0:
            return paramName + ":(id)"+paramName + " "
        else:
            return ":(id)"+paramName + " "
    else:
        return ""


#参数调用器,对传入的参数进行调用
def generateMethodCaller(methods = dict()):
    strResult = ""
    hasIdParam = False
    idParamName = ""
    #遍历方法
    for param in methods:
        paramName = param['name']
        paramType = param['type']
        if paramType == "BOOL":
            strResult += "\tif(!" + paramName +") {\n\t\tNSLog(@\"Error: miss key param\");\n\t\t}\n"
        elif paramType == "id":
            strResult += "\t[self " + "setValue:" + paramName + " forKey:" + "@\"" + paramName + "\"];\n"
            hasIdParam = True
            idParamName = paramName
        else:
            if hasIdParam:
                paramValue = ""
                if paramType == "CGFloat":
                    paramValue = "[NSNumber numberWithFloat:" + paramName + "]"
                elif paramType == "BOOL":
                    paramValue = "nil"
                else:
                    paramValue = paramName
                strResult += "\t[" +  idParamName + " setValue:" + paramValue  + " forKey:" + "@\"" + paramName + "\"];\n"
            else:
                if paramType == "NSString":
                    strResult += "\tNSLog(@\"Logger: %@\"," + paramName + ");\n"
                elif paramType == "NSNumber":
                    strResult += "\tNSLog(@\"Logger: %@\"," + paramName + ");\n"
                else:
                    strResult += "\tNSLog(@\"Logger: %f\"," + paramName + ");\n"

    #如果没有参数
    if len(methods) == 0:
        strResult += "\tNSLog(@\"Logger: -------" + generateNameWithWords(2) + "\");\n"
    return strResult


def main():
    print addNSString()['str']


if __name__ == '__main__':
    main()




