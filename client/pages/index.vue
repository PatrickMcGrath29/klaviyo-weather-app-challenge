<template>
  <div class="container">
    <el-card>
      <el-form>
        <el-form-item label="Email Address">
          <el-input v-model="formData.emailAddress"></el-input>
        </el-form-item>
        <el-form-item label="Location">
          <el-input v-model="formData.location"></el-input>
        </el-form-item>
        <el-form-item>
          <el-button @click="signUp">Sign Me Up</el-button>
        </el-form-item>
      </el-form>
    </el-card>
  </div>
</template>

<script>
export default {
  data () {
    return {
      formData: {
        emailAddress: null,
        location: null
      }
    }
  }
}
</script>
