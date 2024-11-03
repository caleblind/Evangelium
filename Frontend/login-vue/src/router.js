import { createRouter, createWebHistory } from "vue-router";
import AppHome from "./components/AppHome.vue";
import AppLogin from "./components/AppLogin.vue";
import UserProfile from './components/UserProfile.vue';


const routes = [
  { path: "/", component: AppHome },
  { path: "/AppLogin", component: AppLogin },
  { path: "/UserProfile", component: UserProfile },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

export default router;
