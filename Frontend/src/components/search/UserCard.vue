<template>
  <v-row align="center" justify="center" dense>
    <v-col cols="12" md="6">
      <div class="card_container">
        <v-card
          append-avatar="userImage"
          class="mx-auto"
          prepend-avatar="userImage"
          subtitle="prepend-avatar and append-avatar"
          title="Avatars"
        >
          <v-card-text>
            <h2>
              <span>{{ first_name }} {{ last_name }}</span>
            </h2>
            <p>{{ city }}, {{ state }}</p>
            <p>{{ description }}</p>
            <p>Tags:</p>
          </v-card-text>
        </v-card>
      </div>
    </v-col>
  </v-row>
  <div id="ProfileWindow">
    <button class="button" @click="showModal = true">View Profile</button>
    <transition name="fade" appear>
      <div
        class="modal-overlay"
        v-if="showModal"
        @click="showModal = false"
      ></div>
    </transition>
    <transition name="slide" appear>
      <div class="modal" v-if="showModal">
        <h1>
          <span>{{ first_name }} {{ last_name }}</span>
        </h1>
        <p>
          <span>{{ city }}, {{ state }}, {{ country }}, {{ description }}</span>
        </p>
        <button class="button" @click="showModal = false">Close Profile</button>
      </div>
    </transition>
  </div>
</template>

<script>
import userImage from "@/assets/pictures/missionaryprof.jpeg";
export default {
  el: "#UserProfile",
  name: "UserCard",
  props: {
    first_name: {
      type: String,
      required: true,
    },
    last_name: {
      type: String,
      required: true,
    },
    city: {
      type: String,
      required: true,
    },
    state: {
      type: String,
      required: true,
    },
    country: {
      type: String,
      required: true,
    },
    description: {
      type: String,
      required: true,
    },
  },
  data() {
    return {
      userImage: userImage,
      showModal: true,
    };
  },
};
</script>

<style scoped>
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

body {
  font-family: "montserrat", sans-serif;
}

#UserProfile {
  position: relative;

  display: flex;
  justify-content: center;
  align-items: center;

  width: 60vw;
  min-height: 60vh;
  overflow-x: hidden;
}

.button {
  appearance: none;
  outline: none;
  border: none;
  background: none;
  cursor: pointer;

  display: inline-block;
  padding: 10px 15px;
  background-image: linear-gradient(to right, #0a0a0a, #0e0e0e);
  border-radius: 10px;

  color: #fff;
  font-size: 18px;
  font-weight: 700;

  box-shadow: 3px 3px rgba(0, 0, 0, 0.4);
  transition: 0.4s ease-out;

  &:hover {
    box-shadow: 6px 6px rgba(0, 0, 0, 0.6);
  }
}

.modal-overlay {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  z-index: 98;
  background-color: rgba(0, 0, 0, 0.3);
}

.modal {
  position: fixed;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  z-index: 99;

  width: 100%;
  max-width: 400px;
  background-color: #fff;
  border-radius: 16px;

  padding: 25px;

  h1 {
    color: #222;
    font-size: 25px;
    font-weight: 900;
    margin-bottom: 15px;
  }

  p {
    color: #666;
    font-size: 18px;
    font-weight: 400;
    margin-bottom: 15px;
  }
}

.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.5s;
}

.fade-enter,
.fade-leave-to {
  opacity: 0;
}

.slide-enter-active,
.slide-leave-active {
  transition: transform 0.5s;
}

.slide-enter,
.slide-leave-to {
  transform: translateY(-50%) translateX(100vw);
}
h2 {
  display: flex;
  justify-content: flex-start;
  align-items: center;
}

h2 span {
  display: inline-block;
  margin-right: 5px;
  white-space: nowrap;
}

.card_container {
  display: flex;
  width: 283px;
  height: fit-content;
  padding: 12px;
  align-items: center;
  gap: 12px;
  border-radius: 0;
  background: #ffff;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.card_info {
  display: flex;
  align-items: center;
  gap: 12px;
  align-self: stretch;
}

.card_picture {
  display: flex;
  width: 77px;
  height: 70px;
  align-items: center;
}

.card_tags-container {
  display: flex;
  align-items: center;
  align-content: center;
  justify-content: space-between;
  flex-wrap: wrap;
}

.card_pills {
  display: flex;
  padding: 4px 4px;
  justify-content: center;
  align-items: center;
  border-radius: 100px;
}

.card-flag {
  width: 20px;
  height: 20px;
  flex-shrink: 0;
  fill: #d9d9d9;
  stroke-width: 1px;
  stroke: #fff;
  font-size: 18px;
}
</style>
