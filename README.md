# checkData
1.  文件介绍
- checkData.py 获取收款明细
- accounts.txt 想要获取的账号
- checkData.xls 最终生成的excel文档(账号的收款明细)


2. 修改checkData.py

由于系统现在增加了权限验证，想要获取数据，首先需要登录，但是由于登录时有验证码，所以直接调用登录接口
这条路走不通，目前的解决方案是：登录之后获取请求接口的cookie，然后把这个cookie放在脚本请求的请求头中
 
- 如果获取登陆后请求的cookie

步骤1：使用后台账号登录系统(jason账号) \
步骤2：按F12键(chrome浏览器)，然后刷新浏览器抓请求，找到第一个请求然后点击，在右边切换到Headers标签栏，
然后找到Request Headers部分。最后找到Cookie这个键值，copy这个键的值，比如我当前的键值对是：
Cookie: JSESSIONID=5F5E3DE2A01BF5DDADAB0C25952F257E,有用的部分是冒号后面部分的字符串，例子中的是JSESSIONID=5F5E3DE2A01BF5DDADAB0C25952F257E \


- 修改checkData.py文件

编辑checkData.py,然后找到类似这一句header = {"Cookie":"JSESSIONID=5F5E3DE2A01BF5DDADAB0C25952F257E"},
然后把后面的值（例如JSESSIONID=5F5E3DE2A01BF5DDADAB0C25952F257E）,替换成上面获取到的请求cookie值。

- 修改需要统计的收款日期

编辑checkData.py，然后找到类似这一句
```python
accountData_WX = getMoneyToday('WX',acccount,"2019-07-07",header = header)
```
然后把里面的日期替换成统计成日期，比如今天是：2019-07-08，替换后的语句是：
```python
accountData_WX = getMoneyToday('WX',acccount,"2019-07-08",header = header)
```

3. 执行checkData.py

执行checkData.py,等输出结果，结果类似如下：
```text
开始获取数据
总金额： {'WX': 28610.0, 'ZFB': 0}
获取数据结束
```
执行结束后，在当前目录下生成的checkData.xls文件就是最终的统计结果。





