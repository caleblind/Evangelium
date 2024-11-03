<template>
  <div id="app">
    <AppNav />

    <div class="auth-wrapper">
      <div class="auth-inner">
        <router-view />
      </div>
    </div>
  </div>
</template>

<script>
import AppNav from "./components/AppNav.vue";

export default {
  name: "App",
  components: {
    AppNav,
  },
};
</script>

<style>
@import url("https://fonts.googleapis.com/css?family=Fira+Sans:400,500,600,700");
* {
  box-sizing: border-box;
}

body {
  background: #64afe5 !important;
  min-height: 100vh;
  display: flex;
  font-weight: 400;
  font-family: "Fira Sans", sans-serif;
}

body,
html,
#app,
#root,
.auth-wrapper {
  width: 100%;
  height: 100%;
}

#app {
  text-align: right;
}
h1 {
  border-bottom: 1px solid #167bff;
  display: inline-block;
  padding-bottom: 10px;
}
.navbar-light {
  background-color: #000000;
  box-shadow: epx 14px 80px rgba(34, 35, 58, 0.2);
}

.auth-wrapper .form-control:focus {
  border-color: #167bff;
  box-shadow: none;
}

auth-wrapper h3 {
  text-align: right;
  margin: 0;
  line-height: 1;
  padding-bottom: 20px;
}

.custom-control-label {
  font-weight: 400;
}

.forgot-password,
.forgot-password a {
  text-align: right;
  font-size: 13px;
  padding-top: 10px;
  color: #7f7d7d;
  margin: 0;
}

.forgot-password a {
  color: #ffff;
}
</style>
