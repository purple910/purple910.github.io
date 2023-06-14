

# axios+store+loading的配置



## 介绍
在程序中一般会对响应时间比较长的操作进行loading的配置，避免用户的重复操作。

### 配置store
> 添加一个store/index.js文件
```
import Vue from 'vue'
import Vuex from 'vuex'

Vue.use(Vuex)

export default new Vuex.Store({
  state: {
    // 全局的load变量
    isAppending: false
  },
  getters: {
  },
  mutations: {
    // 修改load变量的值
    changeAppending(state, bool) {
      state.isAppending = bool;
    }
  },

})

```

## main.js引入
```
import store from '@/store/index.js'

new Vue({
  store,
  router,
  render: h => h(App)
}).$mount('#app')
```

##  在axios的拦截器中配置
```
import store from '../store/index'

// request拦截器  可对请求进行相应的处理
axios.interceptors.request.use(
  function (config) {
    config.withCredentials = true
    // 默认永不超时
    config.timeout = 0
    let val = window.sessionStorage.getItem('tokenValue')
    let key = window.sessionStorage.getItem('tokenName')
    let token = {}
    Vue.set(token, key, val)
    if (token) {
      config.headers = token
    }

    // 设置全局的load变量值为true，也就是开启load
    store.commit("changeAppending", true);

    return config
  },
  function (error) {
    // 对请求错误做些什么
    return Promise.reject(error)
  }
)
//response拦截器
axios.interceptors.response.use(
  function (response) {
    // 设置全局的load变量值为false，也就是关闭load
    store.commit("changeAppending", false);

    if (response.data.code === 0) {
      return response
    }
    if (response.data.code === -1) {
      router.replace({
        name: 'login'
      });
    }
    Message({
      type: 'error',
      message: response.data.message,
      showClose: true,
    })

    // 将未处理的异常往外抛
    return Promise.reject(response)
  },
  function (error) {
    // 设置全局的load变量值为false，也就是关闭load
    store.commit("changeAppending", false);

    // todo: 做一些其他日志记录处理
    Message({
      type: 'error',
      message: '服务器错误，' + error,
      showClose: true,
    })
  }
)

```

### 组件使用
> 直接绑定在需要load的标签上
```
 <a-button type="primary" @click="submit" style="margin-right: 10px" :loading="$store.state.isAppending">确 定</a-button>
```