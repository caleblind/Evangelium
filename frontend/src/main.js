import { createApp } from "vue";
import App from "./App.vue";
import router from "./router"; // Initialize the router
import "./assets/styles.css"; // Import global styles

const app = createApp(App);
app.use(router);
app.mount("#app");
