import { createRouter, createWebHistory } from "vue-router";
import AppLogin from "@/pages/AppLogin.vue";
import UserProfile from "@/pages/UserProfile.vue";
import LandingPage from "@/pages/LandingPage.vue";
import SearchPage from "@/pages/SearchPage.vue";

function isAuthenticated() {
   return !!localStorage.getItem('access_token'); // Check if user is logged in
}

const routes = [
  { path: "/", component: AppLogin },
   { path: "/AppLogin", component: AppLogin },

   // Protected routes (require authentication)
   { path: "/LandingPage", component: LandingPage, meta: { requiresAuth: true } },
   { path: "/SearchPage", component: SearchPage, meta: { requiresAuth: true } },
   { path: "/UserProfile", component: UserProfile, meta: { requiresAuth: true } },
];

const router = createRouter({
   history: createWebHistory(),
   routes,
});

//    Global Navigation Guard (runs before every route change)
router.beforeEach((to, from, next) => {
   if (to.meta.requiresAuth && !isAuthenticated()) {
      next("/"); // Redirect to login if not authenticated
   } else {
      next(); // Proceed as normal
   }
});

export default router;
