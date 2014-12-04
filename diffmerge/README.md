
##功能

将两个数据库中的基因数据进行对比，并在数据库中存储对比结果。

##应用依赖

- python 2.7
- json_tools

##数据库配置说明

mongodb数据库

Database Name: genetest

collection: genechange

##使用说明

1. 运行`python diff.py`，得到两个库的差别部分，并将其存储到一个名为`genechange`的collection中。
2. 运行`python merge.py`，将`genechange`中的内容，提交到旧的库中，即将旧库更新。

##开发环境

ubuntu 14.04, mongodb, python2.7.8

##开发者

- email: qiwsir@gmail.com
- website: www.itdiffer.com
- github: qiwsir

##感谢

林老师，Chunlei Wu

##感悟

这是一个非常有意思的小东西，业务逻辑虽然简单，但是在处理大量数据的时候，必须要考虑到计算设备、以及运算过程、存储方式等方面。最先开始以为保存到文件中，但是后来发现效果不好，会出现超出内存现象，导致什么存下了空白或者null的东西。后来修改为用数据库解决存储问题。

如果要再深入，可以在对比的内容上更细致一些，并且在结果显示上，可以用网页显示，类似github中提交代码那样的显示方式。
