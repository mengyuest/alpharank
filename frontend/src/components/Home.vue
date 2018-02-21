// Home.vue
<!--
<template>
  <div>
    <p>Home page</p>
    <p>Random number from backend:{{ randomNumber}}</p>
    <button @click="getRandom"> New random number </button>
  </div>
</template>
-->

<template>
    <div id="app">
        <Header></Header>
        <Introduction></Introduction>
        <hr></hr>
        <ReactPanel></ReactPanel>
        <Footer></Footer>
    </div>

</template>

<style>
/* .vl {

    height: 500px;
} */

#header {
    background-color:black;
    color:white;
    text-align:center;
    padding:5px;
}
#nav {
    line-height:30px;
    background-color:#eeeeee;
    height:300px;
    width:100px;
    float:left;
    padding:5px;
}
#section {
    width:350px;
    float:left;
    padding:10px;
}
#footer {
    background-color:black;
    color:white;
    clear:both;
    text-align:center;
    padding:5px;
}
</style>


<script>
import axios from 'axios'
import Header from './Header.vue'
import Introduction from './Introduction.vue'
import ReactPanel from './ReactPanel.vue'
import Footer from './Footer.vue'
export default{
    name: 'app',
    components:{
        Header,
        Introduction,
        ReactPanel,
        Footer
    },
    data(){
        return {
            randomNumber: 0,
            subSet: "void"
        }
    },
    methods:{
        // getRandom(){
        //     this.randomNumber = this.getRandomFromBackend()
        // },
        // getRandomFromBackend(){
        //     const path = `http://localhost:5000/api/random`
        //     axios.get(path)
        //     .then(response => {
        //         this.randomNumber = response.data.randomNumber
        //     })
        //     .catch(error => {
        //         console.log(error)
        //     })
        // }
    }
    // created () {
    //     this.getRandom()
    // }
}
</script>
