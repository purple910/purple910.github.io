# vue 学习



## 路由跳转

```js
 this.$router.push({
        name: "About",
        params: {
          date: row.date,
          name: row.name,
          desc: row.desc,
        },
      });
```


```js
mounted() {
    // 初始化
    let name = this.$route.params.name
    let date1 = this.$route.params.date
    let desc = this.$route.params.desc
    if(desc != null && name != null && date1 != null){
    console.log(desc,name,date1)
    }
}
```



```bash
**1.$route.path**
      字符串，对应当前路由的路径，总是解析为绝对路径，如 "/foo/bar"。
**2.$route.params**
      一个 key/value 对象，包含了 动态片段 和 全匹配片段，
      如果没有路由参数，就是一个空对象。
**3.$route.query**
      一个 key/value 对象，表示 URL 查询参数。
      例如，对于路径 /foo?user=1，则有 $route.query.user == 1，
      如果没有查询参数，则是个空对象。
**4.$route.hash**
      当前路由的 hash 值 (不带 #) ，如果没有 hash 值，则为空字符串。锚点
**5.$route.fullPath**
      完成解析后的 URL，包含查询参数和 hash 的完整路径。
**6.$route.matched**
      数组，包含当前匹配的路径中所包含的所有片段所对应的配置参数对象。
**7.$route.name    当前路径名字**
**8.$route.meta  路由元信息
```



## cookie

```js
//获取cookie、
export function getCookie(name) {
    var arr, reg = new RegExp("(^| )" + name + "=([^;]*)(;|$)");
    if (arr = document.cookie.match(reg))
        return  unescape(arr[2]);
    else
        return null;
}

//设置cookie,增加到vue实例方便全局调用
export function setCookie(c_name, value, expiredays) {
    var exdate = new Date();
    exdate.setDate(exdate.getDate() + expiredays);
    document.cookie = c_name + "=" + escape(value) + ((expiredays == null) ? "" : ";expires=" + exdate.toGMTString());
};

//删除cookie
export function delCookie(name) {
    var exp = new Date();
    exp.setTime(exp.getTime() - 1);
    var cval = getCookie(name);
    if (cval != null)
        document.cookie = name + "=" + cval + ";expires=" + exp.toGMTString();
};
```



```js
// 设置Session
let expireDays = 1000 * 60 * 60;
this.setCookie("name", this.from.name, expireDays); 
// 获取Session
this.from.name = this.getCookie("name");
```



### zip下载

```js
this.$axios
    .post(
    	"/codeBuilder/downLoad",
    { },
    {
    // url中/api是前端解决跨域问题的
    headers: {
    // 这里需要使用form-data格式数据发送请求
    Accept: "application/json",
    },
    responseType: "blob", // 下载zip文件需要使用的响应格式,这是区别于普通post请求的地方,重点!!!
    }
    )
    .then((response) => {
        // console.log(response);
        var zipName = "src"; // 下载的文件名
        let blob = new Blob([response.data], { type: "application/zip" }); // 下载格式为zip
        if ("download" in document.createElement("a")) {
            // 非IE下载;
            let elink = document.createElement("a"); // 创建一个<a>标签
            elink.style.display = "none"; // 隐藏标签
            elink.href = window.URL.createObjectURL(blob); // 配置href
            elink.download = zipName;
            elink.click();
            URL.revokeObjectURL(elink.href); // 释放URL 对象
            if (document.body.contains(elink)) {
            	document.body.removeChild(elink); // 移除<a>标签
            }
        } else {
        	//IE10+
        	navigator.msSaveBlob(blob, zipName);
        }
    })
    .catch((error) => {
        console.log("download error (batch)");
        console.log(error);
    });
```



## xls下载

```js
import { Message } from "element-ui";

this.$axios({
    method: "post",
    	url: "/zb/export",
    data: {},
    	responseType: "blob",
    })
    .then((res) => {
        // 从响应头中获取文件名称
        // const fileName = res.headers["filename"];
        console.log(res.headers);
        const fileName = "12.xls";
        if ("download" in document.createElement("a")) {
            // 非IE下载;
            let elink = document.createElement("a"); // 创建一个<a>标签
            elink.style.display = "none"; // 隐藏标签
            elink.href = window.URL.createObjectURL(new Blob([res.data])); // 配置href
            document.body.appendChild(elink);
            elink.download = fileName;
            elink.click();
            URL.revokeObjectURL(elink.href); // 释放URL 对象
            if (document.body.contains(elink)) {
            	document.body.removeChild(elink); // 移除<a>标签
            }
        } else {
       		//IE10+
        	navigator.msSaveBlob(new Blob([res.data]), fileName);
        }
    })
    .catch((err) => {
    Message.error(err);
    });
```