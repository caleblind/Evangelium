import { createRouter, createWebHistory } from "vue-router";
import AppLogin from "@/pages/AppLogin.vue";
import UserProfile from "@/pages/UserProfile.vue";
import LandingPage from "@/pages/LandingPage.vue";
import AccountCreation from "@/pages/AccountCreation.vue";

const routes = [
  { path: "/", component: LandingPage },
  { path: "/AppLogin", component: AppLogin },
  { path: "/UserProfile", component: UserProfile },
  { path: "/LandingPage", component: LandingPage }, // duplicate. remove when sure it won't break anything
  { path: "/AccountCreation", component: AccountCreation },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

export default router;
