<template>

<ul class="flex justify-between">
  <li class="mr-3">
    <a class="inline-block cursor-pointer border border-white rounded hover:border-gray-200 text-blue-500 hover:bg-gray-200 py-2 px-4" v-on:click="MeRoute"  >Me</a>
  </li>
  <li class="mr-3">
    <a class="inline-block border border-white rounded hover:border-gray-200 text-blue-500 hover:bg-gray-200 py-2 px-4" href="/search">Search</a>
  </li>
</ul>


</template>

<script setup>

const router = useRouter()

const { $getWithExpiry } = useNuxtApp()

function MeRoute(){
  const user = $getWithExpiry("user")
  if (user==null) {

router.push({
        path: '/account',
      })
  } else {
    router.push({
        path: `/user/${user}`,
      })
  }

}


</script>
