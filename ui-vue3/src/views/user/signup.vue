<template>
  <b-card no-body class="mx-auto overflow-hidden">
    <b-row no-gutters>
      <b-col md="6">
        <b-card-img src="https://picsum.photos/400/400/?image=20"
                    class="rounded-0" alt="Signup image"></b-card-img>
      </b-col>
      <b-col md="6">
        <b-card-body>
          <h1>Welcome to sign up</h1>
          <Form @submit="onSubmit" :validation-schema="schema"
                v-slot="{ errors }">
            <div class="form-row">
              <div class="form-group col-8">
                <label>First Name</label>
                <Field name="firstName" type="text" class="form-control"
                       v-model="signupData.firstName"
                       :class="{ 'is-invalid': errors.firstName }" />
                <div class="invalid-feedback">{{ errors.firstName }}</div>
              </div>
              <div class="form-group col-8">
                <label>Last Name</label>
                <Field name="lastName" type="text" class="form-control"
                       v-model="signupData.lastName"
                       :class="{ 'is-invalid': errors.lastName }" />
                <div class="invalid-feedback">{{ errors.lastName }}</div>
              </div>
            </div>
            <div class="form-row">
              <div class="form-group col-8">
                <label>Date of Birth</label>
                <Field name="dob" type="date" class="form-control"
                       v-model="signupData.birthDate"
                       :class="{ 'is-invalid': errors.dob }" />
                <div class="invalid-feedback">{{ errors.dob }}</div>
              </div>
              <div class="form-group col-8">
                <label>Email</label>
                <Field name="email" type="text" class="form-control"
                       v-model="signupData.email"
                       :class="{ 'is-invalid': errors.email }" />
                <div class="invalid-feedback">{{ errors.email }}</div>
              </div>
            </div>
            <div class="form-row">
              <div class="form-group col-8">
                <label>Password</label>
                <Field name="password" type="password" class="form-control"
                       v-model="signupData.password"
                       :class="{ 'is-invalid': errors.password }" />
                <div class="invalid-feedback">{{ errors.password }}</div>
              </div>
              <div class="form-group col-8">
                <label>Confirm Password</label>
                <Field name="confirmPassword" type="password"
                       class="form-control"
                       v-model="signupData.confirmPassword"
                       :class="{ 'is-invalid': errors.confirmPassword }" />
                <div class="invalid-feedback">{{ errors.confirmPassword }}</div>
              </div>
            </div>
            <div class="form-group form-check">
              <Field name="acceptTerms" type="checkbox" id="acceptTerms"
                     value="true" class="form-check-input"
                     :class="{ 'is-invalid': errors.acceptTerms }" />
              <label for="acceptTerms" class="form-check-label check-term">Accept Terms &
                Conditions</label>
              <div class="invalid-feedback">{{ errors.acceptTerms }}</div>
            </div>
            <div class="form-group">
              <b-button class="button" size="default" variant="primary" type="submit" @click="onSubmit">Register</b-button>
            </div>
          </Form>
        </b-card-body>
      </b-col>
    </b-row>
  </b-card>
  <footer><span>The Tech Hub, Copy right@2023</span></footer>
</template>

<script lang="ts">
import { Form, Field } from "vee-validate";
import * as Yup from "yup";
import axiosInstance from "@/config";
import { reactive } from "vue";
import { useRouter } from "vue-router";

interface SignupData {
  email: string,
  password: string,
  confirmPassword: string,
  firstName: string,
  lastName: string,
  gender: boolean,
  birthDate: string
}

export default {
  name: "signup",
  components: {
    Form,
    Field
  },

  setup() {
    const schema = Yup.object().shape({
      dob: Yup.string()
        .required("Date of Birth is required")
        .matches(/^\d{4}-(0[1-9]|1[012])-(0[1-9]|[12][0-9]|3[01])$/, "Date of Birth must be a valid date in the format YYYY-MM-DD"),
      email: Yup.string()
        .required("Email is required")
        .email("Email is invalid"),
      password: Yup.string()
        .min(6, "Password must be at least 6 characters")
        .required("Password is required"),
      confirmPassword: Yup.string()
        .oneOf([Yup.ref("password"), null], "Passwords must match")
        .required("Confirm Password is required"),
      acceptTerms: Yup.string()
        .required("Accept Ts & Cs is required")
    });
    const signupData: SignupData = reactive({
      email: "",
      password: "",
      confirmPassword: "",
      firstName: "",
      lastName: "",
      gender: true,
      birthDate: ""
    });
    const router = useRouter();

    async function onSubmit() {
      axiosInstance.post("/api/v1/user/signup", signupData).then(response => {
        if (response.status === 201) {
          router.push({
            name: "signupsuccess"
          });
        }
      }).catch(error => {
        console.log(error);
      });
    }

    return {
      schema,
      signupData,
      onSubmit
    };
  }
};
</script>

<style lang="less" scoped>

.card {
  margin-top: 6em;
  max-width: 70%;
}

.card-body {
  margin-left: 3em;
}

.button {
  margin-top: .7em;
}

.check-term, .form-check-input{
  margin-top: .5em;
}

footer {
  text-align: center;
  margin-top: 8em;
  color: #304455;
}

</style>
