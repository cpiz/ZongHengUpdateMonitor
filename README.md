# 一个用于通知用户纵横中文网小说更新的脚本


## 配置

在文件notify.cfg中配置要通知的手机号码与书号，格式为

```bash
13500010002:12345,45667
13500020003:54321
```

或者

```bash
13500010002:12345
13500010002:45667
13500020003:54321
```

以#号开头的行将视作整行注释

## 原理

定时自动访问 http://m.zongheng.com/chapter/list?bookid=188493&asc=0&pageNum=1 页面（倒序显示书目），查看最近的一章名称，与缓存文件中的最后一条记录对比
如果章节名称相同，表示指定书目暂无更新
如果文件不存在，或者章节名称不同，则通过“消息速递”服务（http://1290.me）向指定手机发送更新提示，发送成功后将最后一章名称记录在章节文件中

使用python原生库liburl2

## 备注

这是2012写的小脚本，那是一个手机推送还没今天这么泛滥的年代。代码托管在GAE上定时运行，用于通知我正在追的小说是否有更新。因为知乎上有人问起源码，就发到了Github来。但是5年过去，纵横小说网的页面肯定有新变化，当年用到的“消息速递”服务也已经停止运营，Python应该也出了更好的库。
所以脚本肯定是无法工作的，如果出于学习目的看看思路还有一点价值，有心的动手改一改也能再跑起来，就看大家的需要了。我目前已经没时间看小说，也不玩Python和GAE了，所以不再回复咨询，见谅。