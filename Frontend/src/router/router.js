import { createRouter, createWebHistory } from "vue-router";
import AppLogin from "@/pages/AppLogin.vue";
import UserProfile from "@/pages/UserProfile.vue";
import LandingPage from "@/pages/LandingPage.vue";
import SearchPage from "@/pages/SearchPage.vue";
import RegistrationPage from "@/pages/RegistrationPage.vue";

const routes = [
  { path: "/", component: LandingPage },
  { path: "/AppLogin", component: AppLogin },
  { path: "/UserProfile", component: UserProfile },
  { path: "/LandingPage", component: LandingPage },
  { path: "/SearchPage", component: SearchPage },
  { path: "/RegistrationPage", component: RegistrationPage },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

export default router;
