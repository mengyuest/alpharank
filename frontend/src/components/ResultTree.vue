// ResultTree.vue

<template>
  <div id="ResultTree">
    <h2>Result</h2>
    <h3>Static Result</h3>
    <ol>
        <li>Get Coffee </li>
        <li>Get Tea </li>
        <li>Get Milk </li>
    </ol>
    <h3>Dynamic Result</h3>
    <p> {{message}} </p>
    <h3>Parent gave</h3>
    <table>
        <tr v-for="rec in results">
            <th v-for="item in rec">
                {{item}}
            </th>
        </tr>
    </table>
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
