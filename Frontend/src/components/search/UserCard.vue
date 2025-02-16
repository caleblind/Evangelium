<template>
  <v-row align="center" justify="center" dense>
    <v-col cols="12" md="6">
      <div class="card_container">
        <v-card
          append-avatar="userImage"
          class="mx-auto"
          elevation="16"
          max-width="344"
          prepend-avatar="userImage"
          subtitle="prepend-avatar and append-avatar"
          title="Avatars"
        >
          <v-card-item>
            <v-card-title> Card title </v-card-title>

            <v-card-subtitle> Card subtitle secondary text </v-card-subtitle>
          </v-card-item>

          <v-card-text>
            <h2>
              <span>{{ first_name }}</span>
              <span>{{ last_name }}</span>
            </h2>
            <p>{{ city }}, {{ state }}</p>
            <p>{{ description }}</p>
            <p>Tags:</p>
          </v-card-text>
        </v-card>
      </div>
    </v-col>
  </v-row>
</template>

<script>
import userImage from "@/assets/pictures/missionaryprof.jpeg";
export default {
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
    };
  },
};
</script>

<style scoped>
h2 {
  display: flex;
  justify-content: flex-start;
  align-items: center;
}

h2 span {
  display: inline-block;
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
