import { createRouter, createWebHistory } from "vue-router";
import HomeView from "../views/HomeView.vue";
import AppLogin from "../views/AppLogin.vue";
import RegistrationPage from "../views/RegistrationPage.vue";
import SearchPage from "../pages/SearchPage.vue";

const routes = [
  {
    path: "/",
    name: "home",
    component: HomeView,
  },
  {
    path: "/AppLogin",
    name: "AppLogin",
    component: AppLogin,
  },
  {
    path: "/RegistrationPage",
    name: "RegistrationPage",
    component: RegistrationPage,
  },
  {
    path: "/search",
    name: "SearchPage",
    component: SearchPage,
  },
];

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes,
});

export default router;
