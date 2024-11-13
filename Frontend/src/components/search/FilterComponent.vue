<template>
   <div class="filter-component">
     <h3>Filter Search Results</h3>
 
     <!-- Role Filter -->
     <div class="filter-group">
       <label for="role">Role</label>
       <select v-model="filters.role" @change="applyFilters">
         <option value="">All</option>
         <option value="Missionary">Missionary</option>
         <option value="Supporter">Supporter</option>
       </select>
     </div>
 
     <!-- Tags Filter -->
     <div class="filter-group">
       <label for="tags">Tags</label>
       <input
         type="text"
         id="tags"
         placeholder="e.g., Youth, Outreach"
         v-model="filters.tags"
         @input="applyFilters"
       />
     </div>
 
     <!-- Location Filter -->
     <div class="filter-group">
       <label for="location">Location</label>
       <input
         type="text"
         id="location"
         placeholder="Enter location"
         v-model="filters.location"
         @input="applyFilters"
       />
     </div>
 
     <!-- Additional Filters -->
     <!-- Add other filter options as needed -->
   </div>
 </template>
 
 <script>
 export default {
   name: "FilterComponent",
   props: {
     onUpdateFilters: {
       type: Function,
       required: true,
     },
   },
   data() {
     return {
       filters: {
         role: "",
         tags: "",
         location: "",
       },
     };
   },
   methods: {
     applyFilters() {
       // Emit the filter data to the parent component
       this.onUpdateFilters({ ...this.filters });
     },
   },
 };
 </script>
 
 <style scoped>
 .filter-component {
   padding: 16px;
   background-color: #f9f9f9;
   border: 1px solid #ddd;
   border-radius: 8px;
 }
 
 .filter-group {
   margin-bottom: 16px;
 }
 
 label {
   display: block;
   font-weight: bold;
   margin-bottom: 8px;
 }
 
 input,
 select {
   width: 100%;
   padding: 8px;
   border: 1px solid #ccc;
   border-radius: 4px;
 }
 </style>
 