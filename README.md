# iOS-addRubbishCode
帮助OC语言添加混淆代码的脚本，至于用来干嘛的就不多说了。
主要有两个功能：一个是在原来的类里添加新的方法，并进行调用，另一个则是生成新的类，并自动调用。

## addRandomUI.py 
主要包含了生成方法名生成类并调用的实现方法

## addRubbishCode.py 
遍历项目文件，调用addRandomUI.py中的方法来添加相关方法

## changePrefix.py
批量修改文件名前缀

# 使用方法
1. 在addRubbishCode.py中的addRubbish()方法里修改项目路径及内部要添加代码的目录
2. 在addRandomUI.py中的generateNameWithWords()方法里添加自定义的词汇
3. 执行脚本 python addRubbishCode.py
4. 可能存在调用脚本后位置错误引起的报错情况，找到错误修改后即可

萌新脚本，欢迎大家使用提出建议，目前脚本功能残缺，楼楼正在努力维护
想一起加入进来维护的可以加QQ：1007909850 备注:iOS-addRubbishCode即可
