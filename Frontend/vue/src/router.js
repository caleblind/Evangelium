import Vue from 'vue'
import Router from 'vue-router'
import AppHome from './components/AppHome.vue'
import AppLogin from './components/AppLogin.vue'
import ProfileView from '../components/ProfileView.vue';
import EditProfile from '../components/EditProfile.vue';
import { createRouter, createWebHistory } from "vue-router";
import UserProfile from "@/components/UserProfile.vue";

/*Vue.use(Router)
export default Router({
    routes: [
        {path:'/', component: AppHome},
        {path:'/AppLogin',component: AppLogin}
    ]
});*/

Vue.use(VueRouter);

const routes = [
  {
    path: '/profile/:username',
    name: 'ProfileView',
    component: ProfileView,
  },
  {
    path: '/profile/edit',
    name: 'EditProfile',
    component: EditProfile,
  },
  {
    path: "/profile/:id",
    name: "UserProfile",
    component: UserProfile,
  },
];

const router = new VueRouter({
  mode: 'history',
  routes,
});

export default router;