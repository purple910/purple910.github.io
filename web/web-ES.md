---
title: "ES6.x"
date: 2019-07-18T16:39:34+08:00
draft: true
---


# 类
```
class Animal{
    constructor(name){
        this.name=name
    }
    Spack(){
        console.log(name)
    }
}
class Dog extends Animal{
    constructor(name,age){
        super(name);//子类中如果有constructor,就必须有super
        this.age=age
    }
    Spack(){
        super.Spack()//如果没有,则重写Spack方法,有则在Spack中添加内容
        console.log(age)
    }
}
```

# 模块化
```
//导出
var name = 'Rainbow';
var age = '24';
export {name, age};
导入
import {name,age} from '来源';
```

# 箭头函数
```
()=>1
v=>v+1
(a,b)=>a+b
()=>{
    alert("foo");
}
e=>{
    if (e == 0){
        return 0;
    }
    return 1000/e;
}
```

# 模板字符串
```
let name=Tom
`welcome ${name}`
```

# 解构赋值
```
let [foo, [[bar], baz]] = [1, [[2], 3]];
foo // 1
bar // 2
baz // 3

[x, y = 'b'] = ['a', undefined]; // x='a', y='b'

for (let [key, value] of map) {
  console.log(key + " is " + value);
}
```
# 延展操作符
```
function sum(x, y, z) {
  return x + y + z;
}
const numbers = [1, 2, 3];
console.log(sum(...numbers));

let [a,b,...c] = [1,2,3,4,5,6,7,]
console.log(a,b,c)//1 2 [3,4,5,6,7]

var arr = [1, 2, 3];
var arr2 = [...arr]; // 等同于 arr.slice()

```

# Promise
```
var promise = new Promise(function(resolve, reject) {
  // ... some code

  if (/* 异步操作成功 */){
    resolve(value);
  } else {
    reject(error);
  }
});
promise.then(function(value) {
  // success
}, function(error) {
  // failure
});
promise.then((value) => {
  // success
}, (error) => {
  // failure
});
promise.then((value) => {
  // success
}).catch((err) => {
    //failure
});
```

# Generator函数
```
function * gen(x){
  var y = *yield* x + 2;
  return y;
}

var g = gen(1);
g.next() // { value: 3, done: false }
g.next(2) // { value: 2, done: true }
```

# async/await
```
*async* function process(array) {
  for *await* (let i of array) {
    doSomething(i);
  }
}
async function process(array) {
  for await (let i of array) {
    doSomething(i);
  }
}
```

# 正则
```
/foo.bar/.test('foo\nbar')// false
/foo.bar/s.test('foo\nbar') // true

let str = '2019-07-31'
let reg = /(\d{4})-(\d{2})-(\d{2})/
let reg = /(?<year>\d{4})-(?<month>\d{2})-(?<day>\d{2})/
console.log(str.match(reg).groups)

let reg = /^(?<name>welcome)-\k<name>-\1$/
let str = welcome-welcome-welcome
console.log(reg.test(str))
```

# Proxy 
```
let json = {
  name,
  age
}
let newJson = new Proxy(json,{
  set(target,property,value){
    if(property == 'age'){
      if(!Number.isInteger(value)){
        <!-- throw new TypeError('年龄是整数') -->
        return false
      }
    }
    target[property] = value
    return true
  },
  get(target,property){
    if(property in target){
      console.log(`你访问了${property}属性`)
      return target[property]
    }else{
      console.log(`没有这个属性`)
      return null
    }
  },
  has(target,key){
    return key in target;
  },
  deleteProperty(target,property){
    return true
  }
})

var target = function () { return 'I am the target'; };
var handler = {
  apply: function () {
    return 'I am the proxy';
  }
};
var p = new Proxy(target, handler);
p()

const DOM = new Proxy({},{
  get(target,property){
    return function(attr={},...children){
      console el = document.createElement(property)
      for(let key of Object.keys(attr)){
        el.setAttribute(key,attr[key])
      }
      for(let child of children){
        if(typeof child == 'string'){
          child = document.createTextNode(child)
        }
        el.appendChild(child)
      }
      return el
    }
  }
})
let oDiv = DOM.div(
  {id:'id1',class:'cl1'},'div','1123',
  DOM.ul({},
    DOM.li({},111)
    DOM.li({},222)
    DOM.li({},333)
  )
)
```



