// ReactPanel.vue

<template>
  <div id="ReactPanel">
      <div>
          <button @click="updateQuery(1)">count(*)</button>
      </div>
    <div class="row">
        <div class="column">
            <!-- Search Function -->
            <div>
            <input v-model="searched"
            placeholder="type keyword and enter"
            @change="searchSubmit"/>
            </div>

            <!-- Select Function -->
            <div>
            <select v-model="selected" @change="selectSubmit">
                <option disabled value="">Please select one</option>
                <option v-for="option in options"
                v-bind:value="option">{{option}}</option>
            </select>
            <p>Selected: {{ selected }}</p>
            </div>

            <!-- Range Function -->
            <div>
            <select v-model="ranged.left" @change="rangeSubmit">
                <option disabled value="">Select left</option>
                <option v-for="year in years"
                v-bind:value="year">{{year}}</option>
            </select>
            <select v-model="ranged.right" @change="rangeSubmit">
                <option disabled value="">Select right</option>
                <option v-for="year in years"
                v-bind:value="year">{{year}}</option>
            </select>
            <p>Range from: {{ ranged.left }} to {{ranged.right}}</p>
            </div>

            <!-- Hier Function -->
            <HierQueryItem :model="metaData" @sendBackCheck="hierSubmit">
            </HierQueryItem>
            <!-- <QueryTree
            @onClicked="updateQuery"
            /> -->

        </div>
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
import HierQueryItem from './HierQueryItem.vue'
import metaJson from '../../../publist.json'

class TreeNode{
    constructor(name="All Areas",keyword="blabla"){
        this.id=0;
        this.name=name;
        this.keyword=keyword;
        this.level=1;
        this.checked=true;
        this.isFolder=false;
        this.opened=false;
        this.urlnames=[];
        this.urls=[];
        this.children=[];
    }
    turnOn(){
        //if (this.checked != true)
        //{
            var child;
            this.checked=true;
            for (child of this.children)
            {
                child.turnOn();
            }
        //}
    }
    turnOff(){
        //if (this.checked != false)
        //{
            var child;
            this.checked=false;
            for (child of this.children)
            {
                child.turnOff();
            }
        //}
    }
    append(child){
        if (child!=this)
        {
            this.isFolder=true;
            this.children.push(child);
            child.level=this.level+1;
            child.id=this.children.length;
        }
    }
}


export default{

    components:{
        QueryTree,
        ResultTree,
        HierQueryItem
    },
    data(){
        return{
            queryRecord:-1,
            results:"Oh...",
            searched:"",
            options:["World","the USA","Canada","China","Asia"],
            selected:"",
            ranged:{left:1970,right:2018},
            years:Array.from({length: 49}, (x,i) => i+1970),
            metaData:""
        }
    },
    methods:{
        updateQuery (queryId){
            this.queryRecord=queryId
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
        },
        searchSubmit(){
            this.results=this.searched
        },
        selectSubmit(){
            this.results=this.selected
        },
        rangeSubmit(){
            console.log(this.ranged.left)
            this.results=[this.ranged.left,this.ranged.right]
        },
        hierSubmit(node){
            //console.log("Finally, I solve it as Dad~")
            //console.log("Change come from "+node.name)
            //@app.route('/api/confcount/')
            console.log(node.name+" "+node.level)
            if (node.level===4)
            {
                this.getConfCountFromBackend(node.name)
            }
        },
        getConfCountFromBackend(conf){
            const path = `http://localhost:5000/api/confcount`
            axios.get(path, {params:{
                data:conf
            }})
            .then(response => {
                console.log("receive query result!")
                this.results = response.data.subSet
            })
            .catch(error => {
                console.log(error)
            })
        }

    },
    created:function(){
        this.metaData=new TreeNode();
        //
        // var child1=new TreeNode("Computer Vision","CVPR");
        // var child2=new TreeNode("Language Processing","NIPS");
        // var grandson=new TreeNode("Robotics","IROS");
        // child1.append(grandson);
        // this.metaData.append(child1);
        // this.metaData.append(child2);
        // // console.log(metaJson.areas)
        // console.log( metaJson.areas[0].name)

        this.metaData.opened=true

        for (var area_i in metaJson.areas)
        {
            var child=new TreeNode(metaJson.areas[area_i].name)
            this.metaData.append(child)
            child.opened=true
            // console.log("area: "+metaJson.areas[area_i].name)
            // console.log(metaJson.areas[area_i])
            var subarea_i;
            for (subarea_i in metaJson.areas[area_i].subareas){
                var grandson=new TreeNode(metaJson.areas[area_i].subareas[subarea_i].name)
                child.append(grandson)


                // console.log("subArea: "+metaJson.areas[area_i].subareas[subarea_i].name)
                var url_i;
                var conf_i;
                for (url_i in metaJson.areas[area_i].subareas[subarea_i].urls){
                    grandson.urlnames.push(metaJson.areas[area_i].subareas[subarea_i].urls[url_i].name)
                    grandson.urls.push(metaJson.areas[area_i].subareas[subarea_i].urls[url_i].url)

                    // console.log("url: "++" "+)
                }
                for (conf_i in metaJson.areas[area_i].subareas[subarea_i].confs){
                    var grandgrandson=new TreeNode(metaJson.areas[area_i].subareas[subarea_i].confs[conf_i].name,metaJson.areas[area_i].subareas[subarea_i].confs[conf_i].keywords[0])
                    grandson.append(grandgrandson)
                    // console.log("conf: "+metaJson.areas[area_i].subareas[subarea_i].confs[conf_i].name)
                }
            }
        }




    }
}
</script>
