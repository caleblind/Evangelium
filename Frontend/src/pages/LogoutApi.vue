<template>
   <button @click="handleLogout">Logout</button>
 </template>
 
 <script>
 export default {
   methods: {
     handleLogout() {
       localStorage.removeItem("accessToken");
       localStorage.removeItem("refreshToken");
       this.$router.push("/login");
     },
   },
 };
 </script>
 