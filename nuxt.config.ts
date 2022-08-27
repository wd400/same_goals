import { defineNuxtConfig } from 'nuxt'

// https://v3.nuxtjs.org/api/configuration/nuxt.config
export default defineNuxtConfig({
    target: 'static',
    buildModules: ['@nuxtjs/tailwindcss'],
    publicRuntimeConfig: {
        API_BASE_URL: "https://12d8-2a01-cb1d-83fc-e000-9a76-a338-17-44ae.eu.ngrok.io"
    },

    app: {
   //     buildAssetsDir:"/same_goals/"
   //publicRuntimeConfig


    }

    

})
