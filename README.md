## 简介(初版,最近忙完再来优化一下,写完还没测试,备份一下)
#下个版本:新增后台管理系统,域名获取前缀组合字典.再加几个忘记的内容哈哈哈哈

常见的备份扫描检测工具都是windows上面的老工具  
缺点 : 在于无法自定义规则,请求延迟,及时下载,着能自定义后缀

BackupScanMonitor: 
解决:文件名无法自定义,请求延迟,及时下载,多域名拼装字典,选择多字典

## 安装使用


1. python依赖
    >pip install -r requirements.txt
    
使用说明

1. dict.txt文件  
    >test  
    >testtest  
    
2. postfix.txt后缀格式 
    >zip  
    >rar 
    
3. ruleDict.txt (文件规则)    
    >{dictTxt}{urlFormat}.{postfix}  
    >{dictTxt}-{urlFormat}.{postfix}  
    >{dictTxt}_{urlFormat}.{postfix}  
    说明:
      dictTxt = 字典 ,urlFormat = DomainName ,postfix = 后缀  
    
4. 扫描启动
   >执行python scanBak.py -h  
   >  
   >usage:  Example:  
   >scanBak: python scanBak.py -u https://www.163.com -dp /dict1.txt -px /postfix.txt -t 10 -rl /ruleDict.txt -sp 0.2  
   >scanBak: python scanBak.py -u /url.txt -dp /dict1.txt -px /postfix.txt -t 10 -rl /ruleDict.txt -sp 0.2  
   >  
   >OPTIONS:  
   >   -h, --help            show this help message and exit  
   >   -u URL, --url URL     target url: -u /home/me7dog7/url.txt  
   >   -dp DICTPATH, --dictPath DICTPATH  dictPath: -dp  /home/me7dog7/dict1.txt,/home/me7dog7/dict2.txt  
   >   -px POSTFIX, --postfix POSTFIX postfix: -px /home/me7dog7/postfix.txt  
   >   -rl RULEDICT, --ruleDict RULEDICT ruleDict: -rl /home/me7dog7/ruleDict.txt  
   >   -t THREADSUM, --threadSum THREADSUM threadSum: -t 10  
   >   -sp SLEEP, --sleep SLEEP sleep: -sp 0 help:D elay per request  
   > 说明 -h 显示说明 -u 可以字典也可以为http://www.163.com -dp 字典文件路劲,多个字典可以用逗号分隔来区分   
   > -px 后缀字典文件路劲 -rl 规则字典路劲 -sp 请求间隔  
  
