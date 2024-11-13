<template>
   <div class="search-results">
     <p v-if="!results.length">No results found.</p>
     <ul v-else>
       <li v-for="result in results" :key="result.id">
         <!-- Display result data, e.g., name, role, location -->
         <h4>{{ result.name }}</h4>
         <p>{{ result.role }} - {{ result.location }}</p>
         <!-- Add other result fields as necessary -->
       </li>
     </ul>
   </div>
 </template>
 
 <script>
 export default {
   name: "SearchResults",
   props: {
     results: {
       type: Array,
       required: true
     }
   }
 };
 </script>
 
 <style scoped>
 .search-results {
   padding: 10px;
 }
 </style>
 