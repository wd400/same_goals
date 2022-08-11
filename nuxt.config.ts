import { defineNuxtConfig } from 'nuxt'

// https://v3.nuxtjs.org/api/configuration/nuxt.config
export default defineNuxtConfig({
    target: 'static',
    buildModules: ['@nuxtjs/tailwindcss'],
    publicRuntimeConfig: {
        API_BASE_URL: "https://f110-2a01-cb1d-83fc-e000-149c-2b12-3575-edfc.ngrok.io"
    },

    app: {
   //     buildAssetsDir:"/same_goals/"
   //publicRuntimeConfig


    }

    

})
