<template>

<ul class="flex justify-between">
  <li class="mr-3">
    <a class="inline-block text-3xl  cursor-pointer border border-white rounded hover:border-gray-200 text-blue-500 hover:bg-gray-200 py-2 px-4" v-on:click="MeRoute"  >Me</a>
  </li>
  <li class="mr-3">

    <NuxtLink class="inline-block text-3xl  border border-white rounded hover:border-gray-200 text-blue-500 hover:bg-gray-200 py-2 px-4" to="/search">
      Search
    </NuxtLink>

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
