<p  align="left">
    <a href="https://github.com/coder-pig/"><img alt="logo" width="36" height="36" src="res/head_icon.png" alt="coderpig">
    </a>
</p>

<p  align="center">
<img src="res/project_icon.jpg">
</p>

<p align="center" style="margin: 30px 0 35px;">🐭 尾汁Markdown转换工具</p>

**`hzwz-markdown`** 是一款基于**Python**实现的，用于 `将Markdown文件转换成带样式的微信公众号文章HTML` 的工具。<br>

如果你像笔者一样，用Markdown语法撰写文稿，然后用耗费大量时间，用**统一样式**对文章进行排版，最后发布到公号上，使用此工具，可以有效提高你的排版效率。<br>

网上提供的Markdown转换工具不少，如：<br>

- **Markdown转换工具**：[http://blog.didispace.com/tools/online-markdown/][1]
- **Md2All**：[http://md.aclickall.com/][2]
- **MPEditor**：[http://js8.in/mpeditor/][3]
- **Markdown**：[https://www.mdnice.com/][4]

先感谢下大佬们提供的工具，笔者在开发时复制了部分样式，如**Mac样式窗口**~真香<br>
而在使用这些工具时，慢慢发现了两个问题：<br>

- ① **样式单一**：烂大街，有些支持定制，但要自己写CSS，不会前端谁顶得住啊；
- ② **夹带私货**：要登录，要关注，要跳转，恶心心，我只是想转下文件，我TM...；

遂有了自己写一个工具的想法，我的愿景：

- ① **样式灵活**：样式我不会写，**偷** 我会啊，看到喜欢的公号样式直接偷，还有谁？
- ② **简单易用**：用户通过尽可能简单的配置，一键完成转换，一劳永逸。
- ③ **纯粹&可定制**：代码开源，没有私货，纯透明，会Python还能自行定制。

## 0x1、使用前的准备工作

- **Step 1**：通过Git把代码clone到本地，或是直接Download代码压缩包；
- **Step 2**：**安装Python**，如何安装请自行百度，安装了的直接跳过；
- **Step 3**：**安装Nodejs**，同样自行百度；
- **Step 4**：通过**pip命令**安装用到的依赖库；

```
pip install -r requirements.txt
```

## 0x2、怎么直接用？

### 1、准备下样式配置文件

![][5]

编译时，只会使用custom里的样式配置文件！！！你可以：

- ① 复制**author**文件夹里笔者提供的配置文件到custom目录下；
- ② 复制**default_config.ini**文件到custom目录下，然后自行定制；

定制的规则也很简单，如：

![][6]

是的，主要修改下None的值，除**codestyle**和**mac_window**外，其他的值都指向对应的模板文件，如：**h2=1 → 指向：template/h2/1.html**

![][7]

**codestyle** → 代码高亮，基于highlight.js，通过黑魔法将css转换为ini，并将样式写入到HTML中。
喜欢什么代码样式，自己去官网挑：[https://highlightjs.org/][8]

![][9]

复制下这个样式名，如此处的：**atom-one-dark** 即可应用。

**mac_window** → Mac窗口风格，样式提取自：[https://www.mdnice.com/][10]，有下述几种可供选择：

![][11]

具体效果如下：

![][12]

**Tips**：样式配置文件配置一次就可以了，后续不用配置~

### 2、生成转换后带样式的HTML

将md文件放到 **article/md** 目录下，如：

![][13]

然后找到**app.py**文件，右键**run**运行：

![][14]

接着，控制台会输出应用的样式及输出的文件路径：

![][15]

来到**article/out**目录下可以看到生成带样式的HTML文件，排版有点乱，没关系：

![][16]

### 3、复制到微信公众号

接着打开微信公众号，新建文章，F12打开开发者工具，定位到空白内容，如下图：

![][17]

右键Edit as HTML，把生成的带样式的HTML代码拷进去，然后点下外部空白区域即可：

![][18]

看着有点乱？错位，没关系，点击下保存或者预览，即可恢复正常

![][19]

还不正常也没关系，预览发送到手机查阅效果：

![][20]

可以，效果很不错，还有自定义头尾样式，看起来步骤很多，其实非常简单，真一步到位。

这就是这个脚本的用法，如果你想订制自己的样式的话，可以继续往下看~


----------

##0x3、自定义自己的样式

### 1、模板的获取

以某公号的样式为例：

![][21]

这个黑框背景图片和二级标题不错，网页文章页，F12定位到对应结点，

![][22]

右键**Copy** → **Copy element**，粘贴到工程的 **wash/before/in.html**，执行下清洗脚本：

![][23]

![][24]

![][25]

将out.html文件放到**template/image**目录下，改名为2.html，接着改下样式文件，image=2

![][26]

运行后把生成的带样式的HTML复制到微信，点击保存后看下效果：

![][27]

黑边到手，剩下的二级标题也是如法炮制：

![][28]

看下效果：

![][29]

基本内容就这些，还有些细节后续补上~


  [1]: http://blog.didispace.com/tools/online-markdown/
  [2]: http://md.aclickall.com/
  [3]: http://js8.in/mpeditor/
  [4]: https://www.mdnice.com/
  [5]: http://static.zybuluo.com/coder-pig/zd6x7q4dm7lhe4rtmil0kjr6/image_1epnvsh8pnnt76s1a591v7r1ild9.png
  [6]: http://static.zybuluo.com/coder-pig/zrjm1csunlb2rbmnrncjt2py/image_1epo081avv2e1pj6j3k1k9q7j21g.png
  [7]: http://static.zybuluo.com/coder-pig/bu22v2ggxw8itg9fc3n5etfm/image_1epo0j032g7k1d2114hq1ok2jk437.png
  [8]: https://highlightjs.org/
  [9]: http://static.zybuluo.com/coder-pig/e3v6eqrcw2c9jhqjltcuc8d5/image_1epo11mj91a231ald1kkvrtksaa3k.png
  [10]: https://www.mdnice.com/
  [11]: http://static.zybuluo.com/coder-pig/6qzqdnrb3dz0shhf94sokpkf/image_1epo15uqt1vdfbodkef1jf31pjp41.png
  [12]: http://static.zybuluo.com/coder-pig/dpq3shzx4uat7ns5j090hrhh/image_1epo19d3t1o3b3eapka1jomogn4e.png
  [13]: http://static.zybuluo.com/coder-pig/gvp1wqeta62fglv2zkgox7ja/image_1epo1gtqt8ab1oj16q413c01l3v4r.png
  [14]: http://static.zybuluo.com/coder-pig/zkkdh9g1ezd68fw94ar6i7bo/image_1epo1p8kkuu61j12959bm713co58.png
  [15]: http://static.zybuluo.com/coder-pig/gc535pabtdh1mv0xgdrx2c0l/image_1epo1qe7a1qok1haoon91cmm1fcn5l.png
  [16]: http://static.zybuluo.com/coder-pig/zh1i59p2ymf1gnadw0f1o1uw/image_1epo1thdocob1t021eak1n9o1lrp62.png
  [17]: http://static.zybuluo.com/coder-pig/bydfuqlctg625uc2v0suufvt/image_1epog5bbsis21ukqeucsbh6p9.png
  [18]: http://static.zybuluo.com/coder-pig/nwqe7s9d0odol3868ddchk2h/image_1epog9bol7vqqb6dkvldv88pm.png
  [19]: http://static.zybuluo.com/coder-pig/w2znizkydrmyyx1ncmvshnzj/image_1epoge0f810ak3hf5e71ib8hoq9.png
  [20]: http://static.zybuluo.com/coder-pig/rozyqsejuiecv7h2l7679ewi/1.gif
  [21]: http://static.zybuluo.com/coder-pig/59i8vdcupg066u2327oy10ou/image_1epohjnmt6h1nc3jf8ra127q1k.png
  [22]: http://static.zybuluo.com/coder-pig/grd7ptuk2qx87sanuzxdptpk/image_1epohmvp9ndus26uuu3271kkl21.png
  [23]: http://static.zybuluo.com/coder-pig/ezoqe9s11sbzvxvnp8mcg017/image_1epohr422s2m1mg217hg16o71u7k2e.png
  [24]: http://static.zybuluo.com/coder-pig/9qpejohxemedm9mq7qh1ef8i/image_1epoi35qt15ik1sub1co32s10672r.png
  [25]: http://static.zybuluo.com/coder-pig/bob6wxtk77vrgodz6ds96a8o/image_1epoi4vk61nrherv120a11oo1gds38.png
  [26]: http://static.zybuluo.com/coder-pig/v267ukouivlceps5xavqoboy/image_1epoi9lef1ie0f0q9ld1v6u1b3l3l.png
  [27]: http://static.zybuluo.com/coder-pig/06ky5hoc5x8i2scnb5l0v6xj/image_1epoibbop14jelkk1kv01a3vmms42.png
  [28]: http://static.zybuluo.com/coder-pig/njgzv3n7nulrs23rdtsrdm8s/image_1epoiobu113io1bealj2o2p6jg4s.png
  [29]: http://static.zybuluo.com/coder-pig/3iist6zhwuyyaj4ijgw2srka/image_1epoiqc341t3sma07631hinkdp59.png