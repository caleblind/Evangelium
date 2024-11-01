import { createApp } from "vue";
import App from "./App.vue";
import router from "./router"; // initialize the router

const app = createApp(App);
app.mount("#app");
app.use(router);
