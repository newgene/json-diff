exportdb数据库的输出格式。是否有二进制的格式压缩。
测试大规模的数据


有一对mongodb数据
 Chunlei Wu: {"pos": 10048, "chr": "1", "vartype": "del", "allele_freqs": {"C": 0.0025, "CT": 0.9975}, "ref": "CT", "genotypes": {"CT/C": [36]}, "genotype_freqs": {"CT/CT": 0.995, "CT/C": 0.005}}
做一个界面，让用户来query
用户输入某个参数(chr)或者参数的范围(pos)，根据搜索条件进行搜索，呈现结果，两者是and关系。
[CST上午8时52分44秒] Chunlei Wu: fields for query:
[CST上午8时52分48秒] Chunlei Wu: pos: integer（这是一个范围）
[CST上午8时53分01秒] Chunlei Wu: chr: string, 1-22, MT, X
[CST上午8时53分29秒] Chunlei Wu: vartype: string, del, dup, ins
[CST上午8时53分39秒] Chunlei Wu: ref: string


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
