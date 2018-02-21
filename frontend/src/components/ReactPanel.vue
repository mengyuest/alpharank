// ReactPanel.vue

<template>
  <div id="ReactPanel">
      <div>
          <button @click="getSubsetFromBackend(1)">count(*)</button>
      </div>
    <div class="row">
        <div class="column"> <QueryTree
            @onClicked="updateQuery"
            /></div>
        <div class="column"> <ResultTree v-bind:results="results"></ResultTree> <hr></hr>
            <div v-if="queryRecord!=-1">
                Got a query from {{queryRecord}} ~
            </div>
            <div v-else>
                Empty currently
            </div>
        </div>
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

.column {
    float: left;
    width: 45%;
    text-align:left;
    margin-left: 1em
}

/* Clear floats after the columns */
.row:after {
    content: "";
    display: table;
    clear: both;
}
</style>

<script>
import axios from 'axios'
import ResultTree from './ResultTree.vue'
import QueryTree from './QueryTree.vue'
export default{
    components:{
        QueryTree,
        ResultTree
    },
    data(){
        return{
            queryRecord:-1,
            results:"Oh..."
        }
    },
    methods:{
        updateQuery (queryId){
            this.getSubsetFromBackend(queryId)
        },
        getSubsetFromBackend(queryId){
            const path = `http://localhost:5000/api/subset`
            axios.get(path, {params:{
                setlen:queryId
            }})
            .then(response => {
                this.results = response.data.subSet
            })
            .catch(error => {
                console.log(error)
            })
        }
    }
}
</script>
