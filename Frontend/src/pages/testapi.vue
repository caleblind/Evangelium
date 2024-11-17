<template>
   <div class="test-api">
     <h1>API Connection Test</h1>
 
     <!-- GET Request Test -->
     <button @click="testGetRequest" class="api-button">Test GET Request</button>
 
     <!-- POST Request Test -->
     <button @click="testPostRequest" class="api-button">Test POST Request</button>
 
     <!-- Response Display -->
     <div v-if="responseData" class="response">
       <h2>Response Data:</h2>
       <pre>{{ responseData }}</pre>
     </div>
 
     <div v-if="error" class="error">
       <h2>Error:</h2>
       <pre>{{ error }}</pre>
     </div>
   </div>
 </template>
 
 <script>
 import axios from 'axios';
 
 // Function to get CSRF token from cookies (for POST requests)
 function getCSRFToken() {
   const name = 'csrftoken';
   const value = `; ${document.cookie}`;
   const parts = value.split(`; ${name}=`);
   if (parts.length === 2) return parts.pop().split(';').shift();
 }
 
 export default {
   name: "TestApi",
   data() {
     return {
       responseData: null,  // Holds response data from API requests
       error: null          // Holds error messages from API requests
     };
   },
   methods: {
     // Test GET request to the Django backend
     testGetRequest() {
       this.error = null;
       this.responseData = null;
       axios
         .get('http://127.0.0.1:8000/user) // Replace with your actual test endpoint
         .then(response => {
           this.responseData = response.data;
         })
         .catch(error => {
           this.error = `Failed GET request: ${error.message}`;
           console.error("GET API Error:", error);
         });
     },
 
     // Test POST request to the Django backend
     testPostRequest() {
       this.error = null;
       this.responseData = null;
 
       // Add CSRF token to request headers
       const csrfToken = getCSRFToken();
       axios
         .post(
           'http://127.0.0.1:8000/user/', // Replace with your actual test endpoint
           { message: "Hello from Vue!" },
           { headers: { 'X-CSRFTOKEN': csrfToken } }
         )
         .then(response => {
           this.responseData = response.data;
         })
         .catch(error => {
           this.error = `Failed POST request: ${error.message}`;
           console.error("POST API Error:", error);
         });
     }
   }
 };
 </script>
 
 <style scoped>
 .test-api {
   padding: 20px;
   font-family: Arial, sans-serif;
 }
 
 .api-button {
   margin: 10px;
   padding: 10px 20px;
   font-size: 16px;
   color: #fff;
   background-color: #007bff;
   border: none;
   border-radius: 4px;
   cursor: pointer;
 }
 
 .api-button:hover {
   background-color: #0056b3;
 }
 
 .response, .error {
   margin-top: 20px;
   padding: 10px;
   border-radius: 4px;
   background-color: #f9f9f9;
 }
 
 .response pre {
   color: #28a745;
 }
 
 .error pre {
   color: #dc3545;
 }
 </style>
 