// ResultTree.vue

<template>
  <div id="ResultTree">

    <!-- <h3>Parent gave</h3>
    <div v-if="results.length>=1 && results[0].length>1">
    <table >
        <tr v-for="rec in results">
            <th v-for="item in rec">
                {{item}}
            </th>
        </tr>
    </table> -->

</div>
<!-- <div v-else>
    {{results}}
</div> -->
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
import ResultItem from './ResultItem.vue'

export default{
    name: "ResultTree",
    components:{ResultItem},
    props:["treeResults"],
    data(){
        return {
        }
    }
}
</script>
