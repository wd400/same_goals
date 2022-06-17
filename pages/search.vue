<template>
<div >
        <h1 class=" text-5xl font-bold"  >Search goals</h1>
      
<span>
  <br/>
<input v-model="query" class="shadow appearance-none border rounded py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline" type="text" id="name" name="name" required
       minlength="3" maxlength="100"  v-on:keyup.enter="search" size="10">

    <button class="px-2"  v-on:click="search" >🔍</button>

</span>
 <br/>
<div class="w-1/2 bg-white rounded-lg shadow" >
 
    <ul class="divide-y-2 divide-gray-100">
      <div class="p-3" v-for="todo in todos" v-bind:key="todo">

    <NuxtLink :to="`/user/${todo.user}`">

     
     <div>
     
     
     
<li >    <strong>{{todo.todo}}</strong>
    <h2>{{todo.user}}</h2>

     </li>
     

     </div>
    </NuxtLink>
     </div>
     </ul>
     </div>
</div>
</template>

<script setup>

const todos = ref([]);

const query = ref('');

const loading = ref(false);


const config = useRuntimeConfig();

async function search(){

  if (!loading.value){
  loading.value=true

const result = await $fetch(config.API_BASE_URL+`/search`,{
method: 'post', body: { content: query.value }, server: false} )

if (result['status']==true){
   todos.value=result['result']
} else {
  alert(result['msg'])
}

loading.value=false
  }

};
//{"id":433528108663439400,"user":"user2","todo":"hello"}

</script>
