#coding=utf-8

import requests

getAccountUrl = "http://admin.nmgiigle.com/api/manager/system/user/pageList"
postBody = {"username":"","agent":"luna","phoneNumber":"","status":"","pageNum":1,"pageSize":100,"level":None}

def getAccounts(agent="luna",fileName='accounts.txt'):
    '''

    :param agent: agent name
    :return:
    '''
    response = requests.post(getAccountUrl,json=postBody).json()
    accountList = response['data']['list']
    fp = open(fileName,'r')
    myAccounts = map(lambda x:str(x).strip(),fp.readlines())
    fp.close()
    with open("accounts2.txt",'w') as f:
        for accouont in accountList:
            if accouont['username'] not in myAccounts:
                f.writelines(accouont['username']+"\n")

if __name__ == '__main__':
    getAccounts('accounts3.txt')