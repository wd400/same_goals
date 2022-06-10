<template>
<div>
    <p  class=" text-5xl font-bold">{{ $route.params.user }} </p>
    <br/>
  <div v-if="pending">
    Loading ...
  </div>
  <div v-else>
     <div v-for="user in finalusers" v-bind:key="user">

    <NuxtLink :to="`/user/${user.user}`">
 
 

          <div><span class="text-blue-400 text-1xl font-bold">{{user.user}}</span> - {{user.score.toFixed(2)}}</div>
         </NuxtLink>
     </div>
  </div>
  </div>
  
</template>

<script setup>
const config = useRuntimeConfig();

const route = useRoute();

const finalusers=ref([])


const {pending, data: result } = useFetch(config.API_BASE_URL+`/similar/${route.params.user}`, {server: false})
//watch(users, (newTodos) => {})

watch(result, async (newUsers)=>{
   finalusers.value=newUsers.result
}, {
    deep: true
})

</script>