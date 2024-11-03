<template>
   <div class="background-image">
     <div class="profile-wrapper">
       <div class="profile-inner">
         <h3>{{ isEditing ? 'Edit Profile' : 'My Profile' }}</h3>
         
         <div v-if="isEditing" class="edit-profile-form">
           <label for="profile-picture">Profile Picture</label>
           <input type="file" id="profile-picture" @change="onFileChange" />
 
           <label for="description">Description</label>
           <textarea
             id="description"
             v-model="profile.description"
             placeholder="Describe yourself..."
             class="form-control"
           ></textarea>
 
           <label for="tags">Tags</label>
           <input
             id="tags"
             v-model="profile.tags"
             placeholder="Add tags, separated by commas"
             class="form-control"
           />
 
           <button class="btn btn-primary w-100" @click="saveProfile">Save</button>
           <button class="btn btn-secondary w-100 mt-2" @click="toggleEdit">Cancel</button>
         </div>
 
         <div v-else class="view-profile">
           <img :src="profile.profile_picture || defaultImage" alt="Profile Picture" class="profile-picture" />
           <p>{{ profile.description || 'No description provided.' }}</p>
           <p><strong>Tags:</strong> {{ profile.tags || 'No tags added.' }}</p>
           <button class="btn btn-outline-dark w-100" @click="toggleEdit">Edit Profile</button>
         </div>
       </div>
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
       defaultImage: require("@/assets/world.jpg"), // Replace with your default image path
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
         if (this.profile.profile_picture instanceof File) {
           formData.append("profile_picture", this.profile.profile_picture);
         }
         await axios.put("/api/profiles/", formData);
         this.isEditing = false;
         this.fetchProfile(); // Refresh profile after saving
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
 .background-image {
   background-image: url("@/assets/world.jpg");
   background-size: cover;
   background-position: center;
   height: 100vh;
   display: flex;
   justify-content: center;
   align-items: center;
 }
 
 .profile-wrapper {
   display: flex;
   justify-content: center;
   flex-direction: column;
   width: 450px;
 }
 
 .profile-inner {
   background: #828282;
   padding: 40px 55px;
   border-radius: 15px;
   box-shadow: 0px 14px 80px rgba(34, 35, 58, 0.3);
 }
 
 h3 {
   text-align: center;
   color: #fff;
 }
 
 .view-profile,
 .edit-profile-form {
   text-align: center;
 }
 
 .profile-picture {
   width: 150px;
   height: 150px;
   border-radius: 50%;
   margin: 15px 0;
 }
 
 textarea,
 .form-control {
   width: 100%;
   margin-top: 10px;
 }
 
 textarea {
   resize: vertical;
   min-height: 80px;
   max-height: 150px;
   border-radius: 5px;
   padding: 10px;
 }
 
 .btn {
   margin-top: 15px;
 }
 </style>
 