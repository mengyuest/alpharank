// ResultItem.vue

<template>
    <div id="ResultItem">
          <span
        @click="toggle">[{{opened ? '-' : '+'}}]
        </span>
        {{itemResult.name}},{{itemResult.f}},{{itemResult.g}}
        <div v-show="opened">
            <ol>
                <li v-for="faculty in itemResult.faculties">
                    <div>
                        {{faculty.name}},{{faculty.p}},{{faculty.c}}
                        <a :href="faculty.homepage">homepage</a>
                        <!-- <a v-link="`${faculty.homepage}`">Link</a> -->
                        <!-- {{}} -->
                    </div>
                </li>
            </ol>
        </div>

</div>
</template>


<style>

</style>


<script>
export default{
    name: "ResultItem",
    props: {itemResult:Object},
    data(){
        return {
            opened:false
        }
    },
    methods:{
        toggle: function(){
            this.opened=!this.opened
        },
    }

}
</script>
