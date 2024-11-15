<template>
   <header class="header-bar">
     <nav class="nav">
       <ul class="nav-list">
         <li class="nav-item">
           <router-link to="/" class="nav-link">Home</router-link>
         </li>
         <li class="nav-item">
           <router-link to="/landingpage" class="nav-link">Landing Page</router-link>
         </li>
         <!-- Add more navigation links as needed -->
       </ul>
     </nav>
   </header>
 </template>
 
 <script>
 export default {
   name: "HeaderBar",
 };
 </script>
 
 <style scoped>
 .header-bar {
   background-color: #007bff;
   padding: 10px 20px;
   color: #fff;
 }
 
 .nav {
   display: flex;
   align-items: center;
   justify-content: space-between;
 }
 
 .nav-list {
   list-style-type: none;
   padding: 0;
   margin: 0;
   display: flex;
 }
 
 .nav-item {
   margin-right: 15px;
 }
 
 .nav-link {
   color: #fff;
   text-decoration: none;
   font-weight: bold;
 }
 
 .nav-link:hover {
   text-decoration: underline;
 }
 </style>
 