

<script>
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
