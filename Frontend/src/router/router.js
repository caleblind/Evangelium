import { createRouter, createWebHistory } from "vue-router";
import AppLogin from "@/pages/AppLogin.vue";
import UserProfile from "@/pages/UserProfile.vue";
import LandingPage from "@/pages/LandingPage.vue";
import SearchPage from "@/pages/SearchPage.vue";
import MatchmakingPage from "@/pages/MatchmakingPage.vue";

const routes = [
  { path: "/", component: LandingPage },
  { path: "/AppLogin", component: AppLogin },
  { path: "/UserProfile", component: UserProfile },
  { path: "/LandingPage", component: LandingPage },
  { path: "/SearchPage", component: SearchPage },
  { path: "/Matchmaking", component: MatchmakingPage },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

export default router;
