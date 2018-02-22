// QueryTree.vue

<template>
  <div id="QueryTree">
    <h2>Query</h2>
    <h3>Static Query</h3>
    <ul>
        <li>Find Coffee </li>
        <li>Find Tea </li>
        <li>Find Milk </li>
    </ul>
    <h3>Dynamic Query</h3>
    <ul>
        <li v-for="query in queries">
        {{query.text}}
        <button @click="$emit('onClicked',query.id)">
        <!-- <button @click="onC"> -->
            {{query.id}}
        </button>
        </li>
    </ul>

    <div>
    <h3>Tree View</h3>
    <!-- <ul>
        <item v-for="model in ">
    </ul> -->
  </div>
</div>
</template>

<style>
/* #Header {
    background-color:black;
    color:white;
    text-align:center;
    padding:5px;
} */
</style>

<script>
let nextId=1

export default{
    name: "QueryTree",
    data(){
        return{
            queries:[
                {id: nextId+1,
                text: 'coffee'},
                {id: nextId+2,
                text: 'milkshake'},
                {id: nextId+3,
                text: 'coco cola'}
            ],
        }
    },
    methods:{
        onC(){
            console.log("clicked")
        },

    },

}
</script>
