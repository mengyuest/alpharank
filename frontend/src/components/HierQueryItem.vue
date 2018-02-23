//HierQueryItem.vue

<template>
<div id="HierQueryItem"
v-bind:style="{backgroundColor: model.level>0?'white':'lightblue' ,fontSize: 30-model.level*5 + 'px'}"
>
    <div>
         <div> <!-- v-bind:style="{marginLeft:0*model.level-1+'em'}"> -->

            <span v-if="model.isFolder" @click="toggle">[{{model.opened ? '-' : '+'}}]
            </span>
            <span>
            <!-- <h1 v-if="model.level === 1">
              {{model.name}}
          </h1>
            <h2 v-else-if="model.level === 2">
              {{model.name}}
          </h2>
            <h3 v-else-if="model.level === 3">
              {{model.name}}
          </h3>
            <h4 v-else>
              {{model.name}}
          </h4> -->
            {{model.name}}
            </span>
            <input type="checkbox" id="checkbox"
            v-model="model.checked"
            @click="updateCheck"></input>
		</div>
				<!--v-show控制当前元素的display属性，根据v-show里面的值来判断，true显示，false不显示-->
		<div v-show="model.opened" v-if="model.isFolder">
			<!--model用于双向绑定数据-->
			<HierQueryItem v-for="model in model.children" :model="model"
            @sendBackCheck="receiveLowerCheck">
			</HierQueryItem>
		</div>
    </div>
    <!-- <li>
        <div
          :class="{bold: isFolder}"
          @click="toggle"
          @dblclick="changeType">
          {{ model.name }}
          <span v-if="isFolder">[{{ open ? '-' : '+' }}]</span>
        </div>
        <ul v-show="open" v-if="isFolder">
          <item
            class="item"
            v-for="(model, index) in model.children"
            :key="index"
            :model="model">
          </item>
          <li class="add" @click="addChild">+</li>
        </ul>
      </li> -->

</div>
</template>

<script>
export default{
    name: "HierQueryItem",
    props: {
        model: Object
    },
    data(){
        return {
        }
    },
    // computed:{
    //     isFolder: function(){
    //         return this.model.children.length>=1
    //     }
    // },
    methods:{
        toggle: function(){
            if(this.model.isFolder){
                this.model.opened=!this.model.opened
            }
        },
        updateCheck:function(){
            if (this.model.checked != true)
            {
                this.model.turnOn()
            }
            else
            {
                this.model.turnOff()
            }
            this.$emit('sendBackCheck',this.model)
        },
        receiveLowerCheck:function(value_should_passby){
            var isAllChildrenOff=true;
            var isAllChildrenOn=true;
            var child;
            for (child of this.model.children)
            {
                if (child.checked===true)
                {
                    isAllChildrenOff=false;
                }
                else
                {
                    isAllChildrenOn=false;
                }
            }
            if(isAllChildrenOff===true)
            {
                this.model.checked=false;
            }
            else if(isAllChildrenOn===true)
            {
                this.model.checked=true;
            }
            this.$emit('sendBackCheck',value_should_passby)
        }
    },
}


</script>
