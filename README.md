##功能

将两个数据库中的基因数据进行对比，并在数据库中存储对比结果。

##应用依赖

- python 2.7
- BinaryTree模块，源码：https://bitbucket.org/mozman/bintrees/src

##数据库配置说明

mongodb数据库

Database Name: genetest

collection: genechange

其中所包含的collection有：


存储格式举例：{"gene_id":"12079","lastdb":"20141019", "newdb":"20141026", "changes" : [{"stat":"u_replace","value":{...}}]}

说明：
- "gene_id"：该基因在新库中的id
- "lastdb"：就数据日期
- "newdb"：新数据日期
- "changes"：变化了的值
- changes的值为list，其中的元素为dictionary，每个dict是该基因的一个变化内容。

changes的值的结构说明：

- "stat"：其值表明本元素内容的变化性质。

    "new_gene"表示这是一条新增加的基因;
    "delete"表示这个基因在新库中被删除；
    "u_replace"表示这部分内容被替换(更新update)；
    "u_add"表示这部分内容是本条基因中新增加的；
    "u_remove"表示这部分内容在新库中的该条基因中已被删除；

- "value"：表示相应发生变化的部分内容。对于新增加的基因，是该基因的全部内容；对于删除的基因，没有这个键值对；对于已有基因，是变化那部分的最底层的值，并且从json最高层到最底层的key都列出来。


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
