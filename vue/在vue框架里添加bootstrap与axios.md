# 在vue框架里添加bootstrap与axios



# 创建vue项目(已经安装了nodejs,vue@cli)
```
vue create vuedemo
```

# 在vue项目里添加bootstrap
```
 cnpm install bootstrap bootstrap-vue -S
```

## 在src/main.js添加
```
import 'bootstrap/dist/css/bootstrap.css'
import 'bootstrap-vue/dist/bootstrap-vue.css'
import BootstrapVue from 'bootstrap-vue'
Vue.use(BootstrapVue)
```
注意: 如果报错,则放在main.js的开头

## 实例 (About.vue)
```
<div class="container">
  <div class="row">
    <div class="col-md-6">
      <button class="btn btn-info">测试按钮</button>
    </div>
    <button class="btn btn-primary">tbtn</button>
  </div>
</div>
```
### 结果
![](https://img2020.cnblogs.com/blog/1863149/202008/1863149-20200822131408532-1339241338.png)

# 在vue项目里添加axios
```
cnpm install axios -S
```
## 如果是vue2
![](https://img2020.cnblogs.com/blog/1863149/202008/1863149-20200822121834085-1260750620.png)
### 在main.js添加
```
import axios from 'axios'
Vue.prototype.$axios = axios      # 这是把axios全局注册 以后可以this.$axios来访问
```
## 如果是vue3
则只需要在要使用的地方引用axios库
因为: 
vue2里面是用new Vue()来创建vue实例
vue3里面是用createapp()来创建vue实例

## 实例 (About.vue)
```
<script>
export default {
  name: 'about',
  data(){
    return {
      userlist: []
    }
  },
  methods:{
   query:function(){
      this.$axios.get('https://jsonplaceholder.typicode.com/posts')
      .then(res => {
        console.log(res)
        console.log(res.data)
        this.userlist = res.data
        console.log(this.userlist[1].id)
        console.log(this.userlist[1].userId)
        console.log(this.userlist[1].title)
        console.log(this.userlist[1].body)
      })
      .catch(err => {
        console.error(err); 
      })
    }
  }
}
</script>
```
```
<button class="btn btn-primary" v-on:click='query'>btn</button>
```
### 结果
![](https://img2020.cnblogs.com/blog/1863149/202008/1863149-20200822132618994-202738163.png)

# axios与store的联合
## store/index.js
```
import Vue from 'vue'
import Vuex from 'vuex'
import axios from 'axios'

Vue.use(Vuex)

export default new Vuex.Store({
  state: {
    // 初始化数据，只要有可能的用到的最好都初始化
    text: {name: 'xxx'},
    data: {},
  },
  //getters可以认为是store的计算属性
	getters: {
		data(state) {
			return state.data
		}
  },
  //存放同步函数方法
  mutations: {
    // store中的数据只能通过commit mutation来改变
    changeData (state, obj) {
      state.data = obj
    }
  },
  //存放异步函数方法
  actions: {
    // 封装一个ajax方法
    saveForm (context) {
      axios.get('https://jsonplaceholder.typicode.com/posts').then(res => {  // 调用接口
        // console.log(res.data)
        // console.log('---------')
        context.commit('changeData', res.data)  // 通过接口获取的后台数据保存到store中，等待组件取用
      })
    },

    //async异步
    async getTodos({commit}) {
      const result = await axios.get('http://jsonplaceholder.typicode.com/todos?_limit=10');
      // console.log(result)
      // console.log('-------------')
      commit('changeData', result.data);
     }
  },
  modules: {
  }
})

```
# About.vue
```
<button class="btn btn-primary" v-on:click='getDataVuex'>异步方法获取数据1</button>
<input type="button" class="btn btn-danger" value="异步方法获取数据2" v-on:click="getDataVuex1">
<h3>{{data}}</h3>

import {mapState,mapGetters} from 'vuex'
computed:mapGetters(['data']),
methods:{
    getDataVuex () {
      // this.$store.dispatch('saveForm');   // 触发actions里的saveForm函数，调动接口
      this.$store.dispatch('saveForm').then(res => {   // 回调函数是箭头函数
            console.log(this.a);  // --> 123
            // console.log(res)
            // console.log(this.$store.state.data)
            console.log(this.$store.getters)
        })
    },
    getDataVuex1 (){
      this.$store.dispatch('getTodos')
      console.log(this.$store.getters)
    }
}

```
### 结果
![](https://img2020.cnblogs.com/blog/1863149/202008/1863149-20200823194430128-1730600736.png)
![](https://img2020.cnblogs.com/blog/1863149/202008/1863149-20200823194440897-131915982.png)

注: [JSONPlace](http://jsonplaceholder.typicode.com/) 持有人是一个免费的在线 REST API，您可以在需要一些假数据时使用。它非常适合教程、测试新库、共享代码示例...
[httpbin.org](http://www.httpbin.org/) A simple HTTP Request & Response Service.