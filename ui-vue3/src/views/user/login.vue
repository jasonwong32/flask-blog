<template>
  <h1>Login</h1>

</template>

<script lang="ts">
import { defineComponent, reactive } from "vue";
import axiosInstance from "@/config";
import { useLoginStatusStore } from "@/stores";
import { useRouter } from "vue-router";

interface LoginData {
  email: string,
  password: string
}

interface LoginStatusData {
  email: string,
  token: string,
  isLogin: boolean
}

export default defineComponent({
  name: "login",
  setup() {
    const loginData: LoginData = reactive({
      email: "",
      password: ""
    });

    const router = useRouter();

    async function signup() {
      if (loginData.email && loginData.email) {
        axiosInstance.post("/api/v1/user/login", loginData).then(response => {
          const userData: LoginStatusData = {
            email: loginData.email,
            token: response.data.access_token,
            isLogin: !!response.data.access_token
          };
          const loginDataStore = useLoginStatusStore();
          loginDataStore.setLoginStatus(userData);

          // redirect to home page.
          router.push({
            name: "home"
          });
        }).catch(err => {
          console.log(err);
        });
      } else {
        window.alert("Empty email or password is not allowed!")
        console.log("Empty email or password is not allowed!");
      }

    }

    return {
      loginData
    };

  }
});
</script>

<style scoped>

</style>
