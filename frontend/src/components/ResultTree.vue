// ResultTree.vue

<template>
  <div id="ResultTree">
    <h2>Result</h2>

    <h3>Dynamic Result</h3>
    <p> {{message}} </p>
    <h3>Parent gave</h3>
    <div v-if="results.length>=1 && results[0].length>1">
    <table >
        <tr v-for="rec in results">
            <th v-for="item in rec">
                {{item}}
            </th>
        </tr>
    </table>
</div>
<div v-else>
    {{results}}
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
export default{
    name: "ResultTree",
    props:["results"],
    data(){
        return {
            message:"sth old"
        }
    }
}
</script>
