<template>
  <div class="container-fluid">
    <div class="row main-content text-center">
      <div class="col-md-8 col-xs-36 col-sm-36 login_form">
        <div class="container-fluid">
          <form class="form-signin form__input">
            <img class="mb-4" src="../../assets/img/cut-logo.png" alt="blog logo"
                 width="523"
                 height="133"
            />
            <b-form-group
              label="Email:"
              class="text-left"
              label-cols-sm="2"
              label-cols-lg="2"
              content-cols-sm
              content-cols-lg="10"
            >
              <b-form-input type="text" id="inputEmail"
                            class="form-control"
                            placeholder="Enter Email"
                            v-model="loginData.email"
                            :invalid-feedback="schema"
                            required autofocus>
              </b-form-input>
            </b-form-group>

            <b-form-group
              label="Password:"
              class="text-left"
              label-cols-sm="2"
              label-cols-lg="2"
              content-cols-sm
              content-cols-lg="10"
            >
              <b-form-input type="password" id="inputPassword"
                            class="form-control"
                            placeholder="Enter Password"
                            v-model="loginData.password" required
                            @keyup.enter="onSubmit"
              >
              </b-form-input>
            </b-form-group>
            <router-link to="/user/reset/password">forget password</router-link>
            <div class="center-block">
              <button class="btn btn-lg btn-primary btn-block" type="button"
                      @click="onSubmit">Sign in
              </button>
            </div>
          </form>
        </div>
      </div>
    </div>
  </div>
</template>

<script lang="ts">
import { defineComponent, reactive } from "vue";
import axiosInstance from "@/config";
import { useLoginStatusStore } from "@/stores";
import { useRouter } from "vue-router";
import { Form, Field } from "vee-validate";
import * as Yup from "yup";


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
  components: {
    Form,
    Field
  },
  setup() {
    const loginData: LoginData = reactive({
      email: "",
      password: ""
    });

    const schema = Yup.object().shape({
      email: Yup.string()
        .required("Email is required")
        .email("Email is invalid"),
      password: Yup.string().required("Password is required")
    });

    const router = useRouter();

    async function onSubmit() {
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
        window.alert("Empty email or password is not allowed!");
        console.log("Empty email or password is not allowed!");
      }

    }

    return {
      loginData,
      schema,
      onSubmit
    };

  }
});
</script>

<style lang="less" scoped>
.main-content {
  width: 60%;
  margin-top: 10em;
  margin-left: 35em;
  display: flex;
}

b-link{
  font-size: large;
  padding: 1em .5em .5em 1em;
  margin-left: 1em;
}

.login_form {
  background-color: #fff;
  border-top: 1px solid #ccc;
  border-right: 1px solid #ccc;
  border-radius: 20px;
  box-shadow: 0 5px 5px rgba(0, 0, 0, .4);
}

form {
  padding: 0 2em;
}


.form__input {
  width: 70%;
  border: 1px solid transparent;
  border-radius: 0;
  border-bottom: 1px solid #aaa;
  padding: 1em .5em .5em 2em;
  outline: none;
  margin: 1.5em auto;
  /*margin-left: 4em;*/
  transition: all .5s ease;
}


.btn {
  transition: all .5s ease;
  width: 60%;
  border-radius: 30px;
  color: #61777F;
  font-weight: 600;
  background-color: white;
  border: 1px solid #61777F;
  margin-top: 1.5em;
  margin-bottom: 1em;
  margin-left: 1em;
}

.btn:hover, .btn:focus {
  background-color: #61777F;
  color: white;
}


</style>
