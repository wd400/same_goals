<template>
<div>
    <p class="text-5xl font-bold" >{{ $route.params.user }} </p>
        <a  class="text-blue-400 text-1xl font-bold" :href="`/similar/${$route.params.user}`">
          Find similar
      </a>
    <div v-if="islogged">

<textarea  class=" shadow  appearance-none border rounded py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline" v-model="finaldescription" type="text" id="name" name="name" required
  placeholder="Description (about me, contact,...)"     maxlength="200" size="10"></textarea>



    <button  
        type="button"  @click="newdescription">
    💾
    </button>


    </div>
    <div v-else>

      {{finaldescription?finaldescription:""}}
    </div>


     

 <!--BUG ICI-->
 <div v-if="finaltodos">

  <br/>
  <todo-list  :todos="finaltodos" :edit="islogged"/>

 </div>
 <div v-else>
 Loading ...   
 </div>


  </div>
  
</template>

<script setup>
onMounted( async () => {
islogged.value=$getWithExpiry('user')==route.params.user
});

let islogged=ref(false)
let finaltodos=ref([])

let finaldescription=ref("")

const config = useRuntimeConfig();
const route = useRoute();
const { $getWithExpiry } = useNuxtApp()

const todos = await $fetch(config.API_BASE_URL+`/user/${route.params.user}`,{ server: false})
finaltodos.value=todos.todos

const {description: fetcheddescription} = await $fetch(config.API_BASE_URL+`/description/${route.params.user}`,{ server: false})
finaldescription.value=fetcheddescription

async function newdescription(){

  const result  = await $fetch(config.API_BASE_URL+ '/description' ,{
method: 'post', body: { content: finaldescription.value  },server: false,
credentials: 'include'} )

}

</script>