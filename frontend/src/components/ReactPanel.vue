// ReactPanel.vue

<template>
  <div id="ReactPanel">
      <!-- <div>
          <button @click="updateQuery(1)">count(*)</button>
      </div> -->
    <div class="row">
        <div class="column">
            <!-- Search Function -->
            <div>
            <input v-model="searched"
            placeholder="enter title keyword (case insensitive)"
            @change="getNaiveMetricsFromBackend"/>
            </div>

            <!-- Select Function -->
            <div>
            <select v-model="selected" @change="getNaiveMetricsFromBackend">
                <!-- <option disabled value="">Please select one</option> -->
                <option v-for="option in options"
                v-bind:value="option">{{option}}</option>
            </select>
            <span>Selected: {{ selected }}</span>
            </div>

            <!-- Range Function -->
            <div>
            <select v-model="ranged.left" @change="getNaiveMetricsFromBackend">
                <option disabled value="">Select left</option>
                <option v-for="year in years"
                v-bind:value="year">{{year}}</option>
            </select>
            <select v-model="ranged.right" @change="getNaiveMetricsFromBackend">
                <option disabled value="">Select right</option>
                <option v-for="year in years"
                v-bind:value="year">{{year}}</option>
            </select>
            <span>Range from: {{ ranged.left }} to {{ranged.right}}</span>
            </div>

            <!-- Hier Function -->
            <HierQueryItem :model="metaData" @sendBackCheck="hierSubmit">
            </HierQueryItem>
            <!-- <QueryTree
            @onClicked="updateQuery"
            /> -->

        </div>
        <div class="column">
            <h2>Rank Result</h2>
            <div v-if="treeResults.length>1">
            <ol class="pic-container">
                <h3>Rank/Institution/FacultyNum/Factor</h3>
                <li v-for="item in treeResults">
                    <ResultItem v-bind:itemResult="item">
                    </ResultItem>
                </li>
            </ol>
            </div>
            <div v-else>
                Please pick up valid conditions in the left panel~
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

.pic-container{
    height: 800px;
    overflow-x:scroll;
}
</style>

<script>
import axios from 'axios'
import ResultTree from './ResultTree.vue'
import ResultItem from './ResultItem.vue'
import QueryTree from './QueryTree.vue'
import HierQueryItem from './HierQueryItem.vue'
import metaJson from '../../../publist.json'

class TreeNode{
    constructor(name="All Areas",keyword="blabla"){
        this.id=0;
        this.name=name;
        this.keyword=keyword;
        this.level=1;
        this.checked=false;
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
        //ResultTree,
        ResultItem,
        HierQueryItem
    },
    data(){
        return{
            queryRecord:-1,
            results:"Oh...",
            searched:"",
            options:["World","Asia","Australasia","Canada","Europe","South America","the USA"],
            selected:"World",
            ranged:{left:1970,right:2018},
            years:Array.from({length: 49}, (x,i) => i+1970),
            metaData:"",
            treeResults:""
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
            console.log(node.name+" "+node.level)
            this.getNaiveMetricsFromBackend()
        },//This function should be extract to be abstract
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
        },
        getAreaConfList(){
            var sub_area_list=[];
            for (var area_i in this.metaData.children)
            {
                var area=this.metaData.children[area_i];
                for (var sub_area_i in area.children)
                {
                    var sub_area=area.children[sub_area_i];
                    //console.log("after naive "+sub_area.name)
                    var conf_list=[];
                    for (var conf_i in sub_area.children)
                    {
                        var conf=sub_area.children[conf_i];
                        if (conf.checked===true)
                        {
                            conf_list.push(conf.keyword);
                        }
                    }
                    if (conf_list.length>0)
                    {
                        sub_area_list.push(conf_list);
                    }
                }

            }
            return sub_area_list
        },
        getNaiveMetricsFromBackend(){
            console.log("Run to naive")
            var sub_area_list=this.getAreaConfList()
            console.log(sub_area_list)
            const path = `http://localhost:5000/api/naivemetrics`
            axios.get(path, {params:{
                data:JSON.stringify(sub_area_list),//{array: sub_area_list}
                range:JSON.stringify([this.ranged.left,this.ranged.right]),
                region:this.selected,
                searched:this.searched
            }})
            .then(response => {
                console.log("receive query result!")
                this.treeResults = response.data.subSet
                console.log(this.treeResults[0]["name"])
            })
            .catch(error => {
                console.log(error)
            })
        }
    },
    created:function(){
        this.metaData=new TreeNode();
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
