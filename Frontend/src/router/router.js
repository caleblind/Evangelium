import { createRouter, createWebHistory } from "vue-router";
import AppLogin from "@/pages/AppLogin.vue";
import UserProfile from "@/pages/UserProfile.vue";
import LandingPage from "@/pages/LandingPage.vue";
import AccountCreation from "@/pages/AccountCreation.vue";
import MissionaryForm from "@/components/accountcreation/MissionaryForm.vue";
import MainForm from "@/components/accountcreation/MainForm.vue";
import DonorForm from "@/components/accountcreation/DonorForm.vue";

const routes = [
  { path: "/", component: LandingPage },
  { path: "/AppLogin", component: AppLogin },
  { path: "/UserProfile", component: UserProfile },
  { path: "/LandingPage", component: LandingPage }, // duplicate. remove when sure it won't break anything
  { path: "/AccountCreation", component: AccountCreation },
  { path: "/MissionaryForm", component: MissionaryForm },
  { path: "/MainForm", component: MainForm },
  { path: "/DonorForm", component: DonorForm },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

export default router;
