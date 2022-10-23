import { defineNuxtConfig } from 'nuxt'

// https://v3.nuxtjs.org/api/configuration/nuxt.config
export default defineNuxtConfig({
    target: 'static',
    buildModules: ['@nuxtjs/tailwindcss'],
    publicRuntimeConfig: {
        API_BASE_URL: "https://22c1-81-64-42-202.eu.ngrok.io"
    },

    app: {
   //     buildAssetsDir:"/same_goals/"
   //publicRuntimeConfig


    }

    

})
