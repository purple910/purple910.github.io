

# 视屏会议接口文档

## 1.引入视频会议
- 1.1 安装依赖`webrtc-adapter`
```
npm install webrtc-adapter
```
- 1.2 vue中使用janus-gatway
```
# 全局引入janus.js（随文档提供该js文件）
将janus.js引入到项目的index.html中，方便全局使用
<script src="./janus.js"></script>
```
- 1.3 使用封装的视屏会议库
```
# 导入janusLibrary.js文件（随文档提供该js文件），调用其中暴露的方法，具体方法见下文
vue3导入：
import { janusLibrary } from '@/utils/janusLibrary'
# janusCallback为下文对外暴露的接口统一的返回回调函数，在该方法中处理接口返回接口，所以下文接口均为异步。可根据示例使用，示例文件（useRoomEffect.js,随文档提供该js文件）
const { joinRoom, joinRoomWithScreen, leaveRoom, audioMuted, videoMuted, janusRestApi } = janusLibrary(janusCallback)
```

## 2.音视频聊天控制接口
#### 2.1加入房间-音视屏聊天
- 接口说明：加入音、视频都使用该接口，通过参数控制以不同的媒体流（音频流、视频流）进入不同的房间（音频、视频房间）。所有人均为发布者。房间不存在时自动创建支持25个发布者、单人码率上限512kb/s的房间（可调整）。
```
joinRoom(room, name, audio, video)
```
| 参数  | 类型    | 名称         | 备注                                                         |
| ----- | ------- | ------------ | ------------------------------------------------------------ |
| room  | string  | 房间号       | 传入**只包含数字**的字符串                                   |
| name  | string  | 用户名       | 用户的唯一标识，建议为 userName_userId，前端显示时只显示userName |
| audio | boolean | 是否转发音频 |                                                              |
| video | boolean | 是否转发视屏 | audio传true，video传false即为语音通话                        |

#### 2.2加入房间-发布屏幕共享、观看屏幕共享、观看直播
- 接口说明：该接口兼容谷歌浏览器、electron（windows及sw_64）。该接口区分参与屏幕共享人员的`身份`，发布者`publisher`为分享屏幕的人员，订阅者`subscriber`为观看屏幕直播的人员；每个屏幕共享房间仅允许存在1个发布者，当房间已存在发布者时，其他用户无法以发布者身份加入该房间。在electron环境下使用时，需要提前获取并制定分享屏幕的来源`electron.desktopCapturer.getSources`。房间不存在会自动创建支持1个发布者、流量上限为768kb/s的房间。
```
joinRoomWithScreen(room, name, role, source)
```
| 参数   | 类型   | 名称           | 备注                                                         |
| ------ | ------ | -------------- | ------------------------------------------------------------ |
| room   | string | 房间号         | 传入只包含数字的字符串                                       |
| name   | string | 用户名         | 用户的唯一标识，建议为userId                                 |
| role   | string | 加入房间的身份 | 分享者（发布屏幕的人）传入'publisher'，观看者传入'subscriber' |
| source | object | 共享屏幕源     | 浏览器传null。electron使用electron.desktopCapturer.getSources获取并传入选定的源 |

#### 2.3离开房间（我离开房间）
- 接口说明：该接口为离开当前房间，会销毁janus实例。
```
leaveRoom()
```

#### 2.4关闭、打开摄像头
- 接口说明：该接口为关闭/打开`自己的画面`。自己为发布者时，使用该方法关闭/打开自己的画面。关闭画面后房间中的其他人观看到我的视频为黑屏，该接口不会影响音频。
```
videoMuted(muted)
```
| 参数  | 类型    | 名称   | 备注                            |
| ----- | ------- | ------ | ------------------------------- |
| muted | boolean | 控制器 | true为关闭画面，false为打开画面 |
#### 2.5静音、解除静音
- 接口说明：该接口为关闭/打开`自己的音频`（静音/解除静音）。自己为发布者时，使用该方法关闭/打开自己的音频。静音后房间中的其他人无法播放我的音频，该接口不会影响视频。
```
audioMuted(muted)
```
| 参数  | 类型    | 名称   | 备注                          |
| ----- | ------- | ------ | ----------------------------- |
| muted | boolean | 控制器 | true为静音，false为解除静音面 |

## 3.其他API

> API使用权限由业务管理

- 接口说明：调用该方法发送api，以下所有api均调用该方法，通过不同的roomData参数对象区别各个api。
```
janusRestApi(roomData)
```
#### 3.1创建房间

- 参数

| 参数       | 类型    | 名称           | 备注                                              |
| ---------- | ------- | -------------- | ------------------------------------------------- |
| request    | string  | 请求名         | 该请求填入'create'                                |
| room       | int     | 房间号         | 创建房间的房间号                                  |
| is_private | boolean | 是否私有房间   | true则不在获取房间列表接口中返回该房间            |
| permanent  | boolean | 是否永久房间   | false                                             |
| publishers | int     | 最大发布者数量 | 屏幕共享房间为1，视频房间根据网络和服务器条件适配 |
| bitrate    | int     | 最大比特率     | 流量控制，根据网络条件来配置                      |
| allowed    | List    | 白名单         | ["token1", "token2"...]，详情使用请看3.6          |

```json
{
	// 请求名
    request: "create",
    // 房间号
    room: roomId,
    // 是否是私有房间，私有房间则不会出现在房间列表中
    is_private: false,
    // 房间描述、房间名
    description: "Test Room",
    // 是否创建永久房间
    permanent: false,
    // 最大支持人数
    publishers: 1,
    // 比特率
    bitrate: 256000,
};
```

- 返回结果（对应4节中的回调content字段）

| 参数      | 类型    | 名称         | 备注                                                         |
| --------- | ------- | ------------ | ------------------------------------------------------------ |
| videoroom | string  | 响应结果     | 创建成功为'created'                                          |
| room      | int     | 房间号       | 创建的房间号，请求传入房间号则为传入房间号，未传入则为生成的房间号 |
| permanent | boolean | 是否永久房间 | 是否永久房间，是传入的permanent值                            |

```json
{
	// 0请求成功，其他错误
	"code": 0,
	// 该字段中信息为请求返回信息
	"content": {
    	"permanent": false,
    	"room": 12138,
    	"videoroom": "created"
	},
	// API回调标识
	"type": "apiCallback",
    // 请求名
    "request": "create"
}
```



#### 3.2销毁房间

- 参数

| 参数    | 类型   | 名称   | 备注                |
| ------- | ------ | ------ | ------------------- |
| request | string | 请求名 | 该请求填入'destroy' |
| room    | int    | 房间号 | 要销毁的房间号      |

```json
{
      request: "destroy",
      room: 12138
}
```

- 返回结果（对应4节中的回调content字段）

| 参数      | 类型    | 名称         | 备注                              |
| --------- | ------- | ------------ | --------------------------------- |
| videoroom | string  | 响应结果     | 销毁成功为'destroyed'             |
| room      | int     | 房间号       | 销毁的房间号                      |
| permanent | boolean | 是否永久房间 | 是否永久房间，是传入的permanent值 |

```json
{
	// 0请求成功，其他错误
	"code": 0,
	// 该字段中信息为请求返回信息
	"content": {
    	"permanent": false,
    	"room": 12138,
    	"videoroom": "destroyed"
	},
	// API回调标识
	"type": "apiCallback",
    "request": "destroy"
}
```



#### 3.3检查房间是否存在

- 参数

| 参数    | 类型   | 名称   | 备注               |
| ------- | ------ | ------ | ------------------ |
| request | string | 请求名 | 该请求填入'exists' |
| room    | int    | 房间号 | 要检查的房间号     |

```json
{
      request: "exists",
      room: roomId
};
```

- 返回结果（对应4节中的回调content字段）

| 参数      | 类型    | 名称           | 备注                    |
| --------- | ------- | -------------- | ----------------------- |
| videoroom | string  | 响应结果       | 该请求返回值为'success' |
| room      | int     | 房间号         | 检查的房间号            |
| exists    | boolean | 是否存在该房间 | true存在，fasle不存在   |

```json
{
	// 0请求成功，其他错误
	"code": 0,
	// 该字段中信息为请求返回信息
	"content": {
    	"exists": false,
    	"room": 12138,
    	"videoroom": "success
	},
	// API回调标识
	"type": "apiCallback",
    "request": "exists"
}
```



#### 3.4查看房间列表

- 参数

| 参数    | 类型   | 名称   | 备注             |
| ------- | ------ | ------ | ---------------- |
| request | string | 请求名 | 该请求填入'list' |

```json
{
      request: "list"
}
```

- 返回结果（对应4节中的回调content字段）

| 参数      | 类型      | 名称     | 备注                    |
| --------- | --------- | -------- | ----------------------- |
| videoroom | string    | 请求名   | 该请求返回值为'success' |
| list      | arrayList | 房间列表 | 包含房间信息            |

```json
{
	// 0请求成功，其他错误
	"code": 0,
	// 该字段中信息为请求返回信息
	"content": {
        // 房间列表
    	"list": [{
            // 房间号
      		room: 12138,
            // 码率
            bitrate: 256000,
            // 房间描述
            description: "Test Room",
            // 音频编码
            audiocodec: "opus",
            // 视频编码
            videocodec: "vp8",
            // 是否私有房间
            is_private: false,
            // 最大发布者数量
			max_publishers: 1,
			......
        },
            ......],
    	"videoroom": "success"
	},
	// API回调标识
	"type": "apiCallback",
    "request": "list"
}
```



#### 3.5查看房间中的人员

- 参数

| 参数    | 类型   | 名称   | 备注                         |
| ------- | ------ | ------ | ---------------------------- |
| request | string | 请求名 | 该请求填入'listparticipants' |
| room    | int    | 房间号 | 房间号                       |
```json
{
    // 请求名
    request: "listparticipants",
    // 房间号
    room: 12138
};
```

- 返回结果（对应4节中的回调content字段）

| 参数         | 类型      | 名称   | 备注                                 |
| ------------ | --------- | ------ | ------------------------------------ |
| videoroom    | string    | 请求名 | 该请求返回值为'participants'         |
| room         | int       | 房间号 | 房间号                               |
| participants | arrayList | 人员   | 房间人员详情，包括所有发布者和订阅者 |

```json
{
	// 0请求成功，其他错误
	"code": 0,
	// 该字段中信息为请求返回信息
	"content": {
        // 成员列表
    	"participants": [{
            // 用户名
            display: "1676355443692",
			// 用户id（自动生成的）
            id: 5880780873751143,
			// 是否是发布者
            publisher: true,
			// 是否正在讲话（该参数在纯音频房间才生效）
            talking: false
        },
            ......],
    	"videoroom": "participants"
	},
	// API回调标识
	"type": "apiCallback",
    "request": "listparticipants"
}
```

#### 3.6 进入房间权限设置（白名单）

> 创建房间时，可通过传入allowed参数，相当于调用action=add的作用，在创建房间时就开启并添加白名单。

- 参数

| 参数    | 类型   | 名称            | 备注                                                         |
| ------- | ------ | --------------- | ------------------------------------------------------------ |
| request | string | 请求名          | 该请求填入'allowed'                                          |
| room    | int    | 房间号          | 房间号                                                       |
| action  | string | 设置类型        | add\|remove\|enable\|disable 分别对应 添加\|删除\|开启进入认证\|关闭进入认证 |
| allowed | List   | 白名单，为token | ['token1','token2'....]                                      |

```json
# action为add、remove写法
{
    request: "allowed",
    room: 12138,
    action: "add", // 或remove
    // 添加或删除白名单里面的token。注意，这里规定token与加入房间的name字段相同
    allowed: ["user1_toen", "user2_token"...]
}
# action为enable、disable写法。可通过传入enbale来获取房间中已有的白名单
{
      request: "allowed",
      room: 12138,
      action: "add"
}
```

- 返回结果（对应4节中的回调content字段）

| 参数      | 类型   | 名称                | 备注                    |
| --------- | ------ | ------------------- | ----------------------- |
| videoroom | string | 请求名\响应状态     | 该请求返回值为'success' |
| room      | int    | 房间号              | 房间号                  |
| allowed   | List   | 已有白名单token列表 |                         |

```json
# action为enable、add、remove返回结果示例
{
	// 0请求成功，其他错误
	"code": 0,
	// 该字段中信息为请求返回信息
	"content": {
        "allowed": ["token1", "token2"...],
       "room": 12138,
    	"videoroom": "success"
	},
	// API回调标识
	"type": "apiCallback",
    "request": "allowed
}
# action为disable返回结果示例
{
	// 0请求成功，其他错误
	"code": 0,
	// 该字段中信息为请求返回信息
	"content": {
       "room": 12138,
    	"videoroom": "success"
	},
	// API回调标识
	"type": "apiCallback",
    "request": "allowed
}
```

#### 3.7 房间踢人

> 注意，踢出后该用户任可以再次进入房间，防止再次进入需要配合3.6一起使用

- 参数

| 参数    | 类型   | 名称   | 备注                                                   |
| ------- | ------ | ------ | ------------------------------------------------------ |
| request | string | 请求名 | 该请求填入'kick'                                       |
| room    | int    | 房间号 | 房间号                                                 |
| id      | string | 用户id | 是加入房间后返回的rf_id，是janus分配给当前用户会话的id |

```json
{
    request: "kick",
    room: 12138,
    // 用户id
    id: id
}
```

- 返回结果（对应4节中的回调content字段）

| 参数      | 类型   | 名称            | 备注                    |
| --------- | ------ | --------------- | ----------------------- |
| videoroom | string | 请求名\响应状态 | 该请求返回值为'success' |

```json
{
	// 0请求成功，其他错误
	"code": 0,
	// 该字段中信息为请求返回信息
	"content": {
    	"videoroom": "success"
	},
	// API回调标识
	"type": "apiCallback",
    "request": "kick"
}
```

#### 3.8 静默其他用户

- 参数

| 参数    | 类型    | 名称     | 备注                                                   |
| ------- | ------- | -------- | ------------------------------------------------------ |
| request | string  | 请求名   | 该请求填入'moderate'                                   |
| room    | int     | 房间号   | 房间号                                                 |
| id      | string  | 用户id   | 是加入房间后返回的rf_id，是janus分配给当前用户会话的id |
| mid     | int     | 通道id   | 通道id，一同保存在stream的track中                      |
| mute    | boolean | 是否静默 | true为静默，false为解除静默                            |

```json
{
    request: "moderate",
    room: roomId,
    id: id,
    mid: mid,
    mute: mute
}
```

- 返回结果（对应4节中的回调content字段）

| 参数      | 类型   | 名称            | 备注                    |
| --------- | ------ | --------------- | ----------------------- |
| videoroom | string | 请求名\响应状态 | 该请求返回值为'success' |

```json
{
	// 0请求成功，其他错误
	"code": 0,
	// 该字段中信息为请求返回信息
	"content": {
    	"videoroom": "success"
	},
	// API回调标识
	"type": "apiCallback",
    "request": "moderate"
}
```



## 4.jasanusCallback统一回调方法使用

- 方法说明：实现该方法以处理上文中接口/api的返回值。
```
janusCallback(data)
```
- data参数详情：

| 参数    | 类型   | 名称     | 备注                                                         |
| ------- | ------ | -------- | ------------------------------------------------------------ |
| type    | string | 回调类型 | 下文列举所有已有的类型及对应的参数                           |
| code    | int    | 状态码   | 0为正常，其他为异常，且仅type为'error'时code不为0；下文列举所有已有的状态码 |
| content | object | 返回内容 | 下文列举所有已有的type对应的返回类型                         |

- type类型


| type        | 名称                      | 备注                                                         |
| ----------- | ------------------------- | ------------------------------------------------------------ |
| addUser     | 用户加入房间回调          | content为对象，包含userName用户唯一标识、kind媒体轨道类型（audio/video）、track媒体轨道 |
| removeUser  | 用户离开房间回调          | content为userName用户唯一标识                                |
| init        | janus初始化回调           | 无content                                                    |
| error       | 发生错误回调              | content为错误信息字符串                                      |
| initHandle  | videoHandle初始化成功回调 | content为videoRoomHandle对象                                 |
| destoryed   | 结束（我退出房间）回调    | 无content                                                    |
| apiCallback | 3节中的api回调            | content已在上述3节各api中说明，具体是哪个请求则根据其中的"request"区分 |

- code码


| type | 备注                |
| ---- | ------------------- |
| 0    | 正常                |
| 1    | 终端不支持webRTC    |
| 2    | Janus初始化错误     |
| 100  | Janus服务端抛出异常 |
| 304  | 房间权限异常        |

## 5.流的显示
- 在视频会议中的所有媒体均是track，不是直接的MediaStream，需要单独转换才可以展示。且本地流与每个远端用户的媒体流都将音、视频分离，在展示时，最好是将同一用户的track合并到同一MediaStream中。
```
#　将track添加到MediaStream
onst stream = new MediaStream();
# 音、视频可分别addTrack
stream.addTrack(track.clone());
```



## 更多接口请参考

https://blog.csdn.net/u012450998/article/details/122556549



