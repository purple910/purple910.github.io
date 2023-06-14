# onlyoffice（社区版）使用示例

## 1.部署7.1.1.23版本（linux）

> windows有一键部署包，可参考[官方文档](https://api.onlyoffice.com/editors/howitworks) ，建议使用7.2以下版本，避免jwt鉴权等各方面问题。

- 1.安装docker（前置条件）

```shell
apt install -y docker docker.io
```

- 2.部署

```shell
# 镜像获取
	# 在线获取
	docker pull onlyoffice/documentserver:7.1.1.23
	# 【推荐】离线，可免于设置中文字体字号
	## 1.公司导出镜像
	docker save onlyoffice/documentserver:7.1.1.23 -o /home/swx/onlyoffice/onlyoffice.tar
	## 2.现场导入镜像
	docker load < onlyoffice.tar
	
# 创建挂载目录，注意创建的路径与下方启动容器中挂载路径需要相同
mkdir -p /homw/swx/onlyoffice {log, data, lib, db, config}

# 启动容器
docker run -dit --restart=always -p 7123:80 
-v /home/swx/onlyoffice/log:/var/log/onlyoffice  
-v /home/swx/onlyoffice/data:/var/www/onlyoffice/data 
-v /home/swx/onlyoffice/lib:/var/lib/onlyoffice 
-v /home/swx/onlyoffice/db:/var/lib/postgresql 
-v /home/swx/onlyoffice/config:/etc/onlyoffice/documentserver 
onlyoffice/documentserver:7.1.1.23
```



## 2.前端使用示例

- 1.html中引入js文件

```html
<script type="text/javascript" src="http://实际ip:7123/web-apps/apps/api/documents/api.js"></script>
```

- 2.代码示例

```vue
<template>
  <div style="height: 969px; width: 100%">
    <div id="placeholder" style="height: 100%"></div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      docEditor: null,
    };
  },
  mounted() {
    this.initDoc();
  },
  methods: {
    initDoc() {
      // 更多配置可参考 https://blog.csdn.net/cyulotus/article/details/128404264
      let editorConfig = {
        actionLink: null,
        mode: "edit",
        lang: "zh",
        callbackUrl:
          "http://192.168.7.150:7777/file/uploadFroOnlyOffice?fileId=123",
        // 新建的页面，前端路径
        createUrl:
          "http://192.168.7.150:7777/file/uploadFroOnlyOffice?fileId=123",
        customization: {
          about: false,
          comments: true,
          feedback: false,
          // 手动保存
          forcesave: true,
          // 自动保存
          atuosave: false,
          // 报错返回地址
          goback: {
            url: "http://127.0.0.1:8080/#/onlyoffice",
          },
          submitForm: false,
        },
        plugins: { pluginsData: [] },
      };
      this.docEditor = new DocsAPI.DocEditor("placeholder", {
        document: {
          fileType: "docx",
          title: "文件名.docx",
          // 下载地址
          url: "http://192.168.5.107:7777/file/download?fileId=dcbac6d7a7ea4f659226a65bc3266a91",
        },
        documentType: "word",
        editorConfig: editorConfig,
        height: "100%",
        width: "100%",
      });
    },
  },
};
</script>
```

## 3.后端保存注意事项

- 1.callbackUrl为回调接口，由后端实现，注意事项如下:
  - 需要在返回结果json最外层添加`error:0`，没有则认为该接口调用失败，无法继续使用onlyoffice
  - 后端在body中接收参数，其中`status`有以下几种情况，需要重点关注status=2，6的情况，需要下载参数中的url（GET），该url为修改后的文件，在存储到对应的系统的存储中，完成修改。
    - 1 - 文档正在被编辑，一般用户打开文档时的状态。
    - 2 - 文档正要被document server保存，用户完成编辑关闭编辑器的状态。
    - 3 - 文档保存失败。
    - 4 - 文档内容未改变。
    - 6 - 用户手动点击保存。
    - 7 - 用户手动保存失败



## 4.onlyoffice中文字体、字号安装

### 4.1中文字体

- 拷贝windows字体到其他路径，windows字体文件夹`C:\Windows\Fonts`，上传至服务器`fonts`文件夹（fonts文件夹里面存储字体文件，不要有多余的文件夹）
- 服务器上字体文件夹拷贝进入容器

```shell
docker cp fonts/ 689:/usr/share/fonts/truetype/custom
```

- 清除缓存

```
docker exec -it 6896a42d0740 /bin/bash -c "/usr/bin/documentserver-generate-allfonts.sh"
```

- 清除浏览器cookie和历史信息

### 4.2中文字号

> 修改/var/www/onlyoffice/documentserver/web-apps/apps/documenteditor/main/app.js和/var/www/onlyoffice/spreadsheeteditor/web-apps/apps/documenteditor/main/app.js两个文件，在其`{value:8,displayValue:"8"}`字段前加上以下内容（每个文件都有3处修改）:

```json
{value:42,displayValue:"初号"},{value:36,displayValue:"小初"},{value:26,displayValue:"一号"},{value:24,displayValue:"小一"},{value:22,displayValue:"二号"},{value:18,displayValue:"小二"},{value:16,displayValue:"三号"},{value:15,displayValue:"小三"},{value:14,displayValue:"四号"},{value:12,displayValue:"小四"},{value:10.5,displayValue:"五号"},{value:9,displayValue:"小五"},{value:7.5,displayValue:"六号"},{value:6.5,displayValue:"小六"},{value:5.5,displayValue:"七号"},{value:5,displayValue:"八号"},
```

- 操作命令,以/var/www/onlyoffice/documentserver/web-apps/apps/documenteditor/main/app.js修改为例，另一个文件操作完全相同。

```shell
# 修改两个app.js
# 1.documenteditor的app.js
docker cp 6896a42d0740:/var/www/onlyoffice/documentserver/web-apps/apps/documenteditor/main/app.js ./app.js.gz
# 2.修改
# 3.覆盖原来的
docker cp ./app.js.gz 6896a42d0740:/var/www/onlyoffice/documentserver/web-apps/apps/documenteditor/main/app.js 
# 4.进入容器
docker exec -it 6896a42d0740 /bin/bash
# 5.进入app.js路径
cd /var/www/onlyoffice/documentserver/web-apps/apps/documenteditor/main/
# 6.删除原有app.js.gz
rm -rf app.js.gz
# 7.生成app.js.gz
gzip -k app.js
# 8.exit退出容器，再按照1-7的顺序再修改并替换/var/www/onlyoffice/spreadsheeteditor/web-apps/apps/documenteditor/main/app.js文件
# 9.进入容器并清除缓存
docker exec -it 6896a42d0740 /bin/bash -c "/usr/bin/documentserver-generate-allfonts.sh"
# 10.清除客户端浏览器cookie、历史信息
```

