import { createRouter, createWebHistory } from "vue-router";
import AppLogin from "@/pages/AppLogin.vue";
import UserProfile from "@/pages/UserProfile.vue";
import LandingPage from "@/pages/LandingPage.vue";
import SearchPage from "@/pages/SearchPage.vue";

import Login from "@/pages/LoginApi.vue";
import Register from "@/pages/RegisterApi.vue";
import DashboardApi from "@/pages/DashboardApi.vue"; // ✅ Example protected page

const routes = [
  { path: "/login", component: Login },
  { path: "/register", component: Register },
  { 
    path: "/DashboardApi",
    component: DashboardApi,
    meta: { requiresAuth: true }},  // ✅ Protect route
    
  { path: "/", component: LandingPage },
  { path: "/AppLogin", component: AppLogin },
  { path: "/UserProfile", component: UserProfile },
  { path: "/LandingPage", component: LandingPage },
  { path: "/SearchPage", component: SearchPage },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

// ✅ Route Guard to Protect Pages
router.beforeEach((to, from, next) => {
  const token = localStorage.getItem("accessToken");

  if (to.meta.requiresAuth && !token) {
    next("/login"); // Redirect unauthenticated users to login
  } else {
    next();
  }
});

export default router;
