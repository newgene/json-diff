##功能

将两个数据库中的基因数据进行对比，并在数据库中存储对比结果。

##应用依赖

- python 2.7
- BinaryTree模块，源码：https://bitbucket.org/mozman/bintrees/src

##数据库配置说明

mongodb数据库

Database Name:genetest

其中所包含的collection有：

###genedoc_mygene_20141026_g6svo5ct

即将比较的数据，与下面的数据相比

###genedoc_mygene_20141019_efqag2hg

参与比较的数据 

###genedoc_add

新数据相对旧数据，新增加的基因id以及内容。

存储格式：{"gene_id":"该基因在新数据中的id","content":"该基因的完整内容"}

###genedoc_del

新数据相对旧数据，已经删除基因id以及内容。

存储格式：{"gene_id":"该基因在旧数据中的id","content":"该基因的完整内容"}

###genedoc_upd

新数据相对就数据，基因id没有变化，但是具体的基因内容有变化（删除、新增、修改）的部分

存储格式：{"gene_id":"该基因在新（旧）数据中的id","status":"内容变化属性:delete,add,update","content":"发生变化的那部分内容"}

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
