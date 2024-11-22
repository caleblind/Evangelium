<template>
  <div class="background-image">
    <div class="auth-wrapper">
      <div class="auth-inner">
        <h3>Login</h3>
        <form>
          <div class="form-group">
            <label>Email</label>
            <input type="email" class="form-control" placeholder="Email" />
          </div>

          <div class="form-group">
            <label>Password</label>
            <input
              type="password"
              class="form-control"
              placeholder="Password"
            />
          </div>

          <button class="btn btn-primary btn-block">Login</button>
        </form>
      </div>
    </div>
  </div>
</template>

<script>
import axios from "axios";

export default {
  name: "AppLogin",
  data() {
    return {
      loginData: {
        email: "",
        password: "",
      },
      errorMessage: null,
      successMessage: null,
    };
  },
  methods: {
    async handleLogin() {
      try {
        const csrfToken = this.getCookie("csrftoken");
        const response = await axios.post(
          "http://127.0.0.1:8000/login/",
          this.loginData,
          {
            headers: {
              "X-CSRFToken": csrfToken,
            },
          }
        );
        this.successMessage = response.data.message;
        this.errorMessage = null;
        console.log("Login successful:", response.data);
        // Handle successful login (e.g., redirect or store user session)
      } catch (error) {
        this.errorMessage =
          error.response?.data?.email ||
          error.response?.data?.password ||
          "Login failed. Please try again.";
        this.successMessage = null;
        console.error("Login failed:", error.response?.data);
      }
    },
    getCookie(name) {
      const value = `; ${document.cookie}`;
      const parts = value.split(`; ${name}=`);
      if (parts.length === 2) return parts.pop().split(";").shift();
      return null;
    },
  },
};

export default {
  name: "AppLogin",
};
</script>

<style scoped>
.background-image {
  background-image: url("@/assets/pictures/world.jpg");
  background-size: cover;
  background-position: center;
  height: 100vh;
  color: white;
  display: flex;
  justify-content: center;
  align-items: center;
  text-align: center;
}
.auth-wrapper {
  display: flex;
  justify-content: center;
  flex-direction: column;
  text-align: left;
}

.auth-inner {
  width: 450px;
  margin: auto;
  background: #828282;
  box-shadow: 0px 14px 80px rgba(34, 35, 58, 0.3);
  padding: 40px 55px 45px 55px;
  border-radius: 15px;
  transition: all 0.3s;
}

.auth-wrapper .form-control:focus {
  border-color: #167bff;
  box-shadow: none;
}
.auth-wrapper .form-control:focus {
  border-color: #ffff;
  box-shadow: none;
}

auth-wrapper h3 {
  text-align: right;
  margin: 0;
  line-height: 1;
  padding-bottom: 20px;
}
</style>
