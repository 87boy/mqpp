# coding:utf8
import urllib2
import urllib

data_string = '[{"name": "log_lines","columns": ["time", "sequence_number", "line"],"points": [[1400425947378, 3, "this line is first"],[1400425947378, 4, "and this is second"]]}]'

response = urllib2.urlopen('http://localhost:8086/db/testdata/series?u=root&p=root', data_string)

'''data_string就是要上传的内容
   name：series的名字，等同于mysql的表名，你可以取成"313sensor"
   columns：每条数据包括哪几项
       time，当前时间戳
       sequence_number，等同于id
       接下来就是要传的值，比如"temperature"，"co2"，"humidity"
   points：数据，传对应的数据值即可

   PS：记得注意data_string的规范（引号，大括号，中括号，之类）

   urlopen中需要改的：
   localhost改成富帅的ip
   testdata改成你的数据库名
   两个root改成账号和密码

   数据上传完成后，可以在浏览器中打开"<富帅ip>:8086"，在图形化界面中访问influxdb
   '''