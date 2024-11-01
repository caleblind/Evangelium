import { createRouter, createWebHistory } from "vue-router";
import LandingPage from "@/pages/LandingPage.vue";

const routes = [
  {
    path: "/", // Landing page route
    name: "LandingPage",
    component: LandingPage,
  },
  // insert other routes here
];

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes,
});

export default router;
