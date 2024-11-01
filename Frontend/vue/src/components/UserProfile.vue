<template>
   <div class="profile-page">
     <h2>{{ isEditing ? 'Edit Profile' : 'Profile' }}</h2>
     <div v-if="isEditing">
       <input type="file" @change="onFileChange" />
       <textarea v-model="profile.description" placeholder="Describe yourself..."></textarea>
       <input v-model="profile.tags" placeholder="Add tags, separated by commas" />
       <button @click="saveProfile">Save</button>
     </div>
     <div v-else>
       <img :src="profile.profile_picture || defaultImage" alt="Profile Picture" />
       <p>{{ profile.description || 'No description provided.' }}</p>
       <p><strong>Tags:</strong> {{ profile.tags }}</p>
       <button @click="toggleEdit">Edit Profile</button>
     </div>
   </div>
 </template>
 
 <script>
 import axios from "axios";
 
 export default {
   data() {
     return {
       profile: {
         profile_picture: "",
         description: "",
         tags: "",
       },
       isEditing: false,
       defaultImage: "/path/to/default-image.jpg", // Replace with default image path
     };
   },
   methods: {
     async fetchProfile() {
       try {
         const response = await axios.get("/api/profiles/");
         this.profile = response.data;
       } catch (error) {
         console.error("Error fetching profile:", error);
       }
     },
     async saveProfile() {
       try {
         const formData = new FormData();
         formData.append("description", this.profile.description);
         formData.append("tags", this.profile.tags);
         if (this.profile.profile_picture) {
           formData.append("profile_picture", this.profile.profile_picture);
         }
         await axios.put("/api/profiles/", formData);
         this.isEditing = false;
       } catch (error) {
         console.error("Error saving profile:", error);
       }
     },
     toggleEdit() {
       this.isEditing = !this.isEditing;
     },
     onFileChange(event) {
       this.profile.profile_picture = event.target.files[0];
     },
   },
   mounted() {
     this.fetchProfile();
   },
 };
 </script>
 
 <style scoped>
 .profile-page {
   max-width: 600px;
   margin: auto;
 }
 img {
   width: 150px;
   height: 150px;
   border-radius: 50%;
 }
 </style>
 