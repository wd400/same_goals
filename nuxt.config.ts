import { defineNuxtConfig } from 'nuxt'

// https://v3.nuxtjs.org/api/configuration/nuxt.config
export default defineNuxtConfig({
    target: 'static',
    buildModules: ['@nuxtjs/tailwindcss'],
    publicRuntimeConfig: {
        API_BASE_URL: "https://48a4-2a01-cb1d-83fc-e000-d1ea-1056-6e67-b6b1.eu.ngrok.io"
    },

    app: {
   //     buildAssetsDir:"/same_goals/"
   //publicRuntimeConfig


    }

    

})
