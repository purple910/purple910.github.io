# 离线地图

## 前言

离线地图实现物体实时运动轨迹记录。就像滴滴打车，车的运行那样，包含轨迹。其轨迹不是规划好，是实时按照新的坐标位置进行移动，记录移动过的轨迹。

## 1. 简介

百度WebGL版地图支持html5特性，支持3D视角展示地图。其地图数据使用的是矢量地图瓦片。矢量地图瓦片数据量比图片瓦片数据量要小很多，所以下载矢量瓦片会相对容易。

## 2. 下载离线代码测试包

下载地址： <http://www.wmksj.com/script.html> 下载 百度个性地图3D测试(WebGL V1.0).zip 。

因加载瓦片需要使用http请求，所以该测试是基于Tomcat运行的。请自行安装java(jdk1.7或jdk1.8均可)，然后配置JAVA_HOME环境变量。或者使用其它Web 服务（比如：node.js等）。

主目录，WebGL V1.0 tomcat/webapps/map/

目录及文件介绍：

> index.html demo展示的html文件
>
> offlinemap/tiles_v  存放地图所使用的矢量瓦片
>
> offlinemap/tiles_road存放地图所使用的图片路网的地址
>
> offlinemap/tiles_v_road存放地图所使用的矢量路网的地址
>
> offlinemap/tiles_satellite存放地图所使用的卫星图的地址
>
> offlinemap/tiles存放地图所使用的瓦片图的地址

## 3. 下载矢量瓦片数据

### 3.1 复制下载坐标

>下载地址： <http://www.wmksj.com/map.html>
>
>通过区域选择下载的地图或者手动框选需要下载的地图。在框选区域，右键点击“下载矢量地图”。
>
>在弹出的矢量地图下载窗口中，点击“复制下载坐标”。

### 3.2 下载数据

> 下载工具地址：<http://www.wmksj.com/script.html> 下载 百度地图瓦片下载工具1.4.0及以上版本。直接点击该工具目录的wmksj.exe即可打开。
>
> 根据操作提示粘贴下载坐标，下载格式选择“WebGL矢量”，取消勾选“包含名称”。
>
> **注意：默认“包含名称”是勾选的，一定要取消。**
>
> 将下载的矢量数据将前面离线代码测试包的offlinemap/tiles_v的内容进行覆盖替换。

## 4. 修改demo展示的html文件

### 4.1 替换tools中`LuShu_min.js`文件

> 因为有些功能在原来的路书中不支持，故而对路书的源码进行扩展。

### 4.2 index.html的基本配置

```html
<!DOCTYPE html>
<html>
<head>
    <meta http-equiv="Content-Type" content="text/html; charset=UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>www.wmksj.com</title>
    <link rel="stylesheet" type="text/css" href="offlinemap/css/bmap.css" />
    <script type="text/javascript" src="offlinemap/map_load.js"></script>
    <script type="text/javascript" src="offlinemap/tools/LuShu_min.js"></script>
    <script src="offlinemap/tools/axios.min.js"></script>
    <style type="text/css">
        html,
        body,
        #map_container {
            width: 100%;
            height: 100%;
            overflow: hidden;
            margin: 0;
        }

        .BMap_cpyCtrl {
            display: none;
        }

        .anchorBL {
            display: none;
        }

        .BMap_mask {
            z-index: 999;
        }

        ul li {
            list-style: none;
        }

        .drawing-panel {
            z-index: 999;
            position: fixed;
            bottom: 3.5rem;
            margin-left: 3rem;
            padding: 1rem 1rem;
            border-radius: .25rem;
            background-color: #fff;
            box-shadow: 0 2px 6px 0 rgba(27, 142, 236, 0.5);
        }

        .btn {
            width: 90px;
            height: 30px;
            float: left;
            background-color: #fff;
            color: rgba(27, 142, 236, 1);
            font-size: 14px;
            border: 1px solid rgba(27, 142, 236, 1);
            border-radius: 5px;
            margin: 0 5px;
            text-align: center;
            line-height: 30px;
        }

        .btn:hover {
            background-color: rgba(27, 142, 236, 0.8);
            color: #fff;
        }
    </style>
</head>

<body>
    <div id="map_container"></div>
    <div id="result"></div>
    <ul class="drawing-panel" style="z-index: 99;">
        <li class="btn" onclick="run()">开始</li>
        <li class="btn" onclick="stop()">停止</li>
        <li class="btn" onclick="pause()">暂停</li>
        <li class="btn" onclick="add()">add</li>
    </ul>
</body>
<script type="text/javascript">
    // 创建Map实例
    var map = new BMapGL.Map("map_container");
    //初始化地图,设置中心点坐标和地图级别 
    map.centerAndZoom(new BMapGL.Point(103.9516205, 30.768585), 11);
    //开启鼠标滚轮缩放
    map.enableScrollWheelZoom(true);
    // 添加3D控件
    var navi3DCtrl = new BMapGL.NavigationControl3D();
    map.addControl(navi3DCtrl);
    // 添加比例尺控件
    var scaleCtrl = new BMapGL.ScaleControl();
    map.addControl(scaleCtrl);
    // 添加缩放控件
    var zoomCtrl = new BMapGL.ZoomControl();
    map.addControl(zoomCtrl);

    var fly = 'data:image/png;base64,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';

    // 定义路书变量与上次坐标
    var lushu;
    var lastPath = {}

    //绑定事件
    function run() {
        //路书启动,参数为一个函数
        callback()
    }

    function run1() {
        //路书启动,参数为一个函数
        lushu.start(callback);
    }

    // 全局坐标列表
    var rallPath = []
    // 回调函数
    function callback() {
        let tempPath = []
        const paths = rallPath
        rallPath = []

        // 没有新的坐标添加则结束
        if (paths.length == 0) {
            lushu = null
            console.log("没有新的坐标添加则结束");
            return
        } else {
            // 开始需要至少两个坐标
            if (Object.keys(lastPath).length == 0) {
                if (paths.length > 1) {
                    lastPath = paths[0]
                } else {
                    // 没有两个坐标，则将paths放回全局坐标列表中
                    rallPath = [...paths, ...rallPath]
                    console.log("开始需要至少两个坐标");
                    return
                }
            }

            // 将坐标循环放入地图坐标系中
            tempPath.push(new BMapGL.Point(lastPath.lng, lastPath.lat))
            for (let i = 0; i < paths.length; i++) {
                const element = paths[i];
                tempPath.push(new BMapGL.Point(element.lng, element.lat))
            }

            // 存储上次坐标列表的最后值
            lastPath.lat = paths[paths.length - 1].lat
            lastPath.lng = paths[paths.length - 1].lng
        }

        // 路书存在则清除上次运行图标
        if (lushu != null) {
            lushu.clear()
        }
        lushu = null

        // 将坐标转化为线
        let polyline = new BMapGL.Polyline(tempPath);
        // 创建路书实例
        lushu = new BMapGLLib.LuShu(map, polyline.getPath(), {
            geodesic: true,// 弧度
            defaultContent: '', // ""
            icon: new BMapGL.Icon(fly, new BMapGL.Size(48, 48), { anchor: new BMapGL.Size(24, 24) }), // 图标
            speed: 30000, // 速度
            enableRotation: true, // 是否设置marker随着道路的走向进行旋转
        });

        // 开启路书运动
        run1()
    }

    // 路书停职
    function stop() {
        lushu.stop();
    }
    // 路书暂停
    function pause() {
        lushu.pause();
    }

</script>
</html>
```

### 4.3 动态坐标

### 4.3.1 使用websocket，向rallPath追加坐标

> 前端代码

```js
// 在全局坐标列表中添加坐标数据
var websocket = new WebSocket(
    "ws://localhost:8888/wc/start"
);
// 连接错误
websocket.onerror = () => {
    console.log("onerror");
}
// 连接成功
websocket.onopen = () => {
    console.log("onopen");
}
// 收到消息的回调
websocket.onmessage = (res) => {
    console.log(res.data);
    rallPath.push(JSON.parse(res.data))
}
// 连接关闭的回调
websocket.onclose = () => {
    console.log("WebSocket连接关闭");
}
```

> 后端代码
>
> > ServerEndpointExporter注入bean

```java
@Configuration
public class WebSocketConfig {

    @Bean
    public ServerEndpointExporter serverEndpointExporter() {
        return new ServerEndpointExporter();
    }

}
```

>> WebSocketServer配置

```java
import com.alibaba.fastjson.JSONObject;
import org.springframework.stereotype.Component;
import javax.websocket.*;
import javax.websocket.server.PathParam;
import javax.websocket.server.ServerEndpoint;
import java.io.IOException;
import java.util.concurrent.Executors;
import java.util.concurrent.ScheduledExecutorService;
import java.util.concurrent.ScheduledFuture;
import java.util.concurrent.TimeUnit;

@ServerEndpoint("/wc/{temp}")
@Component
public class WebSocketServer {

    /**
     * 与某个客户端的连接会话，需要通过它来给客户端发送数据
     */
    private Session session;

    /**
     * 定时任务
     */
    ScheduledFuture<?> schedule;

    /**
     * 连接建立成功调用的方法
     */
    @OnOpen
    public void onOpen(Session session, @PathParam("temp") String temp) {
        this.session = session;
        System.out.println("连接成功！");
        if ("start".equals(temp)) {
            test_scheduleAtFixedRate();
        }
    }

    /**
     * 连接关闭调用的方法
     */
    @OnClose
    public void onClose() {
        System.out.println("连接关闭");
    }

    /**
     * 收到客户端消息后调用的方法
     *
     * @param message 客户端发送过来的消息
     */
    @OnMessage
    public void onMessage(String message, Session session) {
        //可以群发消息
        //消息保存到数据库、
        System.out.println("收到客户端消息后调用的方法");
    }

    /**
     * @param session
     * @param error
     */
    @OnError
    public void onError(Session session, Throwable error) {
        this.schedule.cancel(true);
        error.printStackTrace();
    }

    /**
     * 实现服务器主动推送
     */
    public void sendMessage(String message) throws IOException {
        this.session.getBasicRemote().sendText(message);
    }

    public void test_scheduleAtFixedRate() {
        // 固定频率地对一个任务循环执行
        ScheduledExecutorService service = Executors.newScheduledThreadPool(5);
        this.schedule = service.scheduleAtFixedRate(() -> {
            try {
                // 利用websocket向前端推送坐标
                JSONObject map = new JSONObject();
                map.put("lng", Math.floor(Math.random() * 1000 + 1) * 0.001 + 103.5);
                map.put("lat", Math.floor(Math.random() * 1000 + 1) * 0.001 + 30.8);
                sendMessage(map.toJSONString());
            } catch (IOException e) {
                e.printStackTrace();
            }
        }, 0, 100L, TimeUnit.MILLISECONDS);
    }

}
```

### 4.3.2 前端使用setInterval定时函数，调用ajax请求，向rallPath追加坐标

> 前端代码

```js
// 在全局坐标列表中添加坐标数据
function add() {
    axios.post('http://127.0.0.1:8888/add')
        .then(function (response) {
            rallPath.push(response.data)
        })
        .catch(function (error) {
            console.log(error);
        });
    console.log(rallPath);
}

// 定时任务调用add方法
var sh;
sh = setInterval(add, 10);

```

> 后端接口

```java
@RestController("/")
public class CertController {
    @PostMapping("/add")
    public Map<String, Double> add() {
        Map<String, Double> map = new Hashtable<>();
        map.put("lng", Math.floor(Math.random() * 1000 + 1) * 0.001 + 103.5);
        map.put("lat", Math.floor(Math.random() * 1000 + 1) * 0.001 + 30.8);
        return map;
    }
}
```

## 5启动和测试

> 启动tomcat：双击WebGL V1.0 tomcat/bin/startup.bat 。
>
> 在弹出的窗口中出现Server startup in xxx ms字样时，表示启动成功。(注意：如果该窗口闪退，表示JAVA_HOME未配置正确)
>
> 然后在浏览器地址栏输入 <http://localhost/map>， 会看到如下成功显示WebGL 1.0版个性化离线地图。