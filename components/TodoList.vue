<template>
<div class="">
    <div v-for="todo in todos" v-bind:key="todo">
        <button class="text-red-400 text-1xl"
        type="button" v-if="edit" @click="deletetodo(todo.id)">
    X
    </button>
    <span class=" font-bold px-2">{{todo.todo}}</span>
    


    

      <!-- do something -->
    </div>

</div>
    <div v-if="edit">
        
      <!--  <label for="name">TODO: </label>
      -->

<input  v-on:keyup.enter="addtodo" class="shadow  appearance-none border rounded py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline" v-model="current_todo" type="text" id="name" name="name" required
       minlength="3" maxlength="100" size="10">
    <button   class="text-3xl text-green-400 font-bold"
        type="button"  @click="addtodo">
    ✔
    </button>


    </div>
</template>




<script setup>


const props = defineProps({
  todos: {
    type: Array,
    required: true
  },
  edit: {
    type:Boolean,
    required:true
  }
});

const current_todo = ref('');

const loading = ref(false);

const config = useRuntimeConfig();



async function addtodo(){

if (!loading.value){

loading.value=true
const result  = await $fetch(config.API_BASE_URL+`/add`,{
method: 'post', body: { content: current_todo.value} ,server: false,
 credentials: 'include',
    headers: {
          // remove headers
        }
} )

if (result['status']==true){
   props.todos.push({"id":result['id'],"todo":current_todo.value}); 
   current_todo.value="";
} else {
  alert(result['msg'])
}

loading.value=false
}

};



async function deletetodo(id){

const result  = await $fetch(config.API_BASE_URL+`/delete/${id}`,{ server: false,
 credentials: 'include'})

if (result['status']==true){
for (let i = 0; i < props.todos.length; i++) {
  if (props.todos[i]['id']==id){
   props.todos.splice(i, 1); 
    break;
  }
  
}}};
//const { $setWithExpiry } = useNuxtApp()


</script>
