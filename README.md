<p align="center">
<img src="https://github.com/WZKSDN/OIer/raw/master/on_server/logo-white.png" />
</p>

<h1 align="center">OIerDb</h1>

<p align="center">OIerDb is a database for Chinese OI participants.</p>
<p align="center">OIerDb 是中国信息学竞赛选手的一个数据库.</p>

### The following data are the unlicensed data gathered and formatted by fjzzq2002 from noi.cn. These data are modified and completed.
- CTSC 2010-2017
- APIO 2010-2017
- NOI 2010-2017
- NOI D类 2014-2017
- WC 2015-2017
- NOIP 2013-2017

### The rest of the data are directly from noi.cn, including:

- NOI 2009
- NOI type D 2010-2013
- NOIP 2010-2012 ( not complete)



### 这些数据是在开源项目中，由fjzzq2002整理的，并进行了部分完善
- CTSC 2010-2017
- APIO 2010-2017
- NOI 2010-2017
- NOI D类 2014-2017
- WC 2015-2017
- NOIP 2013-2017

### 其余数据来源于NOI官网，包括

- NOI 2009
- NOI D类 2010-2013
- NOIP 2010-2012 提高组一等奖

将来会及时更新新数据，也可能会添加缺失数据。

## 搭建指南

这个项目是"OIerDb",但其实可以方便地改装成为任何一个学科竞赛获奖的数据库。项目由如下几部分组成：

### 合并及数据预处理

#### 原始数据文件

##### data.txt

data.txt中是所有的获奖记录，实则为csv格式，每一行格式如下：

`比赛名称,奖项,姓名,年级,学校,分数,省份,性别,`

下面是一个例子

`NOI2018,金牌,杨骏昭,高一,南京外国语学校,522,江苏,男,`

需要注意的是，如果其中有一项缺省，逗号的数目不能减少，且每行最后还有一个逗号。

##### school_oped.txt

school_oped.txt中是表示学校合并信息的文件，同时记录有学校所属的省份。每一行格式如下：

`省份,地市,学校名称1,学校名称2,(更多学校名称，结尾无逗号)`

下面是一个例子

`江苏,苏州市,江苏省苏州中学,江苏省苏州中学校,苏州中学`

需要注意，每一个在`data.txt`中出现的学校名称都应当在这个文件中出现。
在`getter.py`中提供了一个基于百度地图api的从学校名称找定位的函数，通过这个函数可以初步地获得学校所在省份和地市，并合并一下定位相同的学校。这个效果并不充分，合并更多学校很大程度上基于人工判断，如果有人希望部署这个系统至其他位置，可参考本项目中`school_oped.txt`中做出的合并。

#### 合并及数据处理脚本

两个脚本均是`python3`脚本，并需要`pypinyin`才能够正常运行。

##### new_merger.py

new_merger.py 是最重要的数据合并器。

new_merger.py 从 `data.txt` 和 `school_oped.txt` 读入数据，并输出csv格式到`result.txt`中。

##### school_analyzer.py

school_analyzer.py 是学校获奖记录统计及排名器。

new_merger.py 从 `data.txt` 和 `school_oped.txt` 读入数据，并输出csv格式到`OI_school.txt`中。

这个脚本将每个学校的获奖记录统计，并计算分数。分数由一个函数f(排名，比赛类型，比赛年份)得出

f(排名，比赛类型，比赛年份) = 0.8 ^ (2018-比赛年份) * g(排名*400/总参赛人数) * 比赛权重

g(x)在x = 0-60时为 100-40上的线性函数，x在60-250上为 36 - 7.5 上的线性函数，x在250-400上为7.5-0上的线性函数。

`权重 = {"NOI":1,"NOID类":0.75,"CTSC":0.6,"WC":0.5,"APIO":0.4,"NOIP提高":0.1,"NOIP普及":0.04}`

如果您有兴趣修改这个评分函数（或参数），请对比说明您的函数（或参数）的优越性。毕竟现在应用的也是一念之间的产物。

### 在线部署

[作者的部署](http://bytew.net/OIer)

作者的部署使用了`MySQL`，但实际上您使用什么数据库都可以（尽管这里只提供了php格式的查询MySQL数据库并返回的代码）。在更新/新添加数据时，先运行数据预处理的脚本，而后将生成的csv格式数据导入到数据库中，就结束了。

#### search.php 和 school.php

根据查询查表，而后返回 json 格式的数据。您需要更改php中的数据库信息以适应自己的设置。具体实现可能不是很漂亮。

欢迎您来作出贡献，提出意见和建议，或者自己搭一个玩玩。
