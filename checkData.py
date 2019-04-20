#coding=utf-8
import requests
import copy
import time
import xlwt
import os

getOrderUrl = 'http://admin.mergiigle.com/api/manager/pay/userOrder/pageList'
#orderStatus=3 已收款
#orderType=1001 微信，orderType=1002 支付宝
postBody = {
    "agent": "",
    "merchantNo": "",
    "sysOrderNo": "",
    "username": "fgk",
    "orderStatus": "3",
    "orderType": "1001",
    "pageNum": 1,
    "pageSize": 20
}

def readAccountFromFile(fileName):
    """
    read accounts from file
    :return:a list of accounts
    """
    with open(fileName,'r') as f:
        accountsList = f.readlines()
        accountsList = map(lambda x:str(x).strip(),accountsList)

    return accountsList

def getMoneyToday(moneyType,userName,checkDate=None):
    """
    get user money of today
    :param moneyType:WX,ZFB,QQ...
    :param userName:account name
    :param checkDate:the date of check
    :return: a list contains user datas like:
        {
            "data": {
                "total": 1000,
                "AmountDetails": [
                    1000
                ]
            },
            "name": "fanwei"
        }
    """
    userData = {}

    if str(moneyType).upper() not in ["WX","ZFB","QQ"]:
        raise TypeError("moneyType must be WX or ZFB or QQ")

    body = copy.deepcopy(postBody)
    if str(moneyType).upper() == "WX":
        body.update({"orderType":"1001"})
    elif str(moneyType).upper() == "ZFB":
        body.update({"orderType": "1002"})
    else:
        body.update({"orderType": "1003"})

    body.update({"username":userName})

    response = requests.post(getOrderUrl,json=body).json()
    moneyList = []
    payAmountList = []
    dataList = response['data']['list']
    if not checkDate:
        today = time.strftime("%Y-%m-%d")
    else:
        today = checkDate
    for data in dataList:
        createTime = data['createTime']
        orderAmount = data['orderAmount']
        payAmount = data['payAmount']

        # check time
        createTimeStr = time.strftime("%Y-%m-%d",time.localtime(float(int(createTime)/1000)))
        if createTimeStr == today:
            moneyList.append(orderAmount)
            payAmountList.append(payAmount)
            continue

    userData['data'] = {"AmountDetails":moneyList,"total":sum(moneyList),"payAmountDetails":payAmountList}
    userData['name'] = userName

    return userData

def writeExcel(datas):
    """
    write all accounts data to excel
    :param datas:所有用户的今日收款数据,格式如下：
    {
        "WX":[
                {"data": {"total": 300,"AmountDetails": [300]},"name": "fgk"},
                {"data": {"total": 1000,"AmountDetails": [1000]},"name": "fanwei"}
            ],
        "ZFB":[
                {"data": {"total": 300,"AmountDetails": [300]},"name": "fgk"},
                {"data": {"total": 1000,"AmountDetails": [1000]},"name": "fanwei"}
            ]
    }

    :return:
    """
    datas_wx = datas['WX']
    datas_zfb = datas['ZFB']
    total_wx = datas['totals']['WX']
    total_zfb = datas['totals']['ZFB']

    workBook = xlwt.Workbook()
    sheet_WX = workBook.add_sheet(time.strftime("%Y-%m-%d")+"_WX")
    sheet_ZFB = workBook.add_sheet(time.strftime("%Y-%m-%d") + "_ZFB")
    # write title
    sheet_WX.write(0, 0, "Account")
    sheet_WX.write(0, 1, "Amount")
    sheet_WX.write(0, 2, "AmountDetails")
    sheet_WX.write(0, 3, "OrderAmountDetails")

    sheet_ZFB.write(0, 0, "Account")
    sheet_ZFB.write(0, 1, "Amount")
    sheet_ZFB.write(0, 2, "AmountDetails")
    sheet_ZFB.write(0, 3, "OrderAmountDetails")

    row = 1
    for data in datas_wx:
        AmountDetails = map(lambda x:str(x),data['data']['AmountDetails'])
        OrderAmountDetails = map(lambda x:str(x),data['data']['payAmountDetails'])
        sheet_WX.write(row, 0, data['name'])
        sheet_WX.write(row, 1, data['data']['total'])
        sheet_WX.write(row, 2, ",".join(AmountDetails))
        sheet_WX.write(row, 3, ",".join(OrderAmountDetails))
        row += 1
    row += 2
    sheet_WX.write(row,0,r"total")
    sheet_WX.write(row, 1, total_wx)

    row = 1
    for data_zfb in datas_zfb:
        AmountDetails = map(lambda x: str(x), data_zfb['data']['AmountDetails'])
        OrderAmountDetails = map(lambda x: str(x), data_zfb['data']['payAmountDetails'])
        sheet_ZFB.write(row, 0, data_zfb['name'])
        sheet_ZFB.write(row, 1, data_zfb['data']['total'])
        sheet_ZFB.write(row, 2, ",".join(AmountDetails))
        sheet_ZFB.write(row, 3, ",".join(OrderAmountDetails))
        row += 1
    row += 2
    sheet_ZFB.write(row, 0, "total")
    sheet_ZFB.write(row, 1, total_zfb)

    if os.path.exists("checkData.xls"):
        os.remove("checkData.xls")
    workBook.save("checkData.xls")

if __name__ == '__main__':
    print u"开始获取数据"
    accounts = readAccountFromFile("accounts.txt")
    allAcountsDatas = {'WX':None,'ZFB':None,"totals":{'WX':None,'ZFB':None}}
    allAccountsDatas_WX = []
    allAccountsDatas_ZFB = []
    todayTotalMoney_WX = 0
    todayTotalMoney_ZFB = 0
    for acccount in accounts:
        accountData_WX = getMoneyToday('WX',acccount,"2019-04-19")
        allAccountsDatas_WX.append(accountData_WX)
        todayTotalMoney_WX += accountData_WX['data']['total']

        accountData_ZFB = getMoneyToday('ZFB',acccount)
        allAccountsDatas_ZFB.append(accountData_ZFB)
        todayTotalMoney_ZFB += accountData_ZFB['data']['total']

    allAcountsDatas.update({'WX':allAccountsDatas_WX,'ZFB':allAccountsDatas_ZFB,'totals':{'WX':todayTotalMoney_WX,'ZFB':todayTotalMoney_ZFB}})
    print u"总金额：" , allAcountsDatas['totals']
    print u"获取数据结束"
    writeExcel(allAcountsDatas)
