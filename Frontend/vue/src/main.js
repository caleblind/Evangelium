// src/main.js

import { createApp } from 'vue';
import App from './App.vue'; // Root Vue component
import router from './src/router.js'; // Vue Router configuration
import store from './store'; // Vuex store (optional, for state management)
import api from './api'; // Axios instance for API requests

// Import global styles
import './assets/styles/main.css'; // Customize this path based on your project structure

// Import a CSS framework like Bootstrap or Tailwind CSS if needed
import 'bootstrap/dist/css/bootstrap.min.css';

// Create Vue application
const app = createApp(App);

// Set up a global property to access the Axios instance throughout the app
app.config.globalProperties.$api = api;

// Use router, store, and any other plugins
app.use(router); // Register the router
app.use(store); // Register Vuex store (if using Vuex)

// Mount the app to the DOM element with ID `#app`
app.mount('#app');

createApp(App).mount('#app');

new Vue({
   router,
   render: h=> h(App),
}).$mount('#app')
