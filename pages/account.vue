<template>
<div class="w-full max-w-xs">
    <h1 class="text-4xl font-bold">{{tologin? 'Login':'Create account'}}</h1>
Switch to <input class="text-blue-400 text-1xl cursor-pointer font-bold"  type="button" v-on:click="tologin=!tologin" :value="tologin? 'Create account':'Login'"> 
<div>
    <label for="username">Username:</label>
    <input class="shadow appearance-none border rounded py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline" v-model="username" type="text" id="username" name="username">
</div>

<div>
    <label for="pass">Password:</label>
    <input class="shadow appearance-none border border-red-500 rounded py-2 px-3 text-gray-700 mb-3 leading-tight focus:outline-none focus:shadow-outline" v-model="password" type="password" id="pass" name="password"
         placeholder="***********"  minlength="8" required>
</div>

<input type="button" class="text-blue-400 text-1xl cursor-pointer font-bold" v-on:click="login()" :value="tologin? 'Sign in':'Sign up'">
</div>
</template>

<script setup>
const router = useRouter();
const tologin=ref(true);



const username = ref('');
const password = ref('');
const config = useRuntimeConfig();

const { $setWithExpiry } = useNuxtApp()

async function login(){



const result  = await $fetch(config.API_BASE_URL+ (tologin.value?'/login':'/signup') ,{
method: 'post', body: { username: username.value,password:password.value  },server: false,
credentials: 'include'} )

console.log(result)



if (result['status']==true){
   if (tologin){
       $setWithExpiry('user',username.value,1000*60*60*12)
     return navigateTo({
    path: '/user/'+username.value,
  })
   }
} else {
    alert(result['msg'])
}


};


</script>
