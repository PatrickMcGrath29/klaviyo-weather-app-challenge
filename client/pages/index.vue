<template>
  <div class="container">
    <div class="weather-alert__form">
      <el-card>
        <el-form>
          <div class="sub-title">Email Address</div>
          <el-form-item>
            <el-input v-model="formData.emailAddress" type="email"></el-input>
          </el-form-item>
          <div class="sub-title">Location</div>
          <el-form-item>
            <el-autocomplete
              v-model="formData.location"
              class="inline-input"
              :fetch-suggestions="querySearch"
              placeholder="enter a location"
              :trigger-on-focus="false"
              @select="handleSelect"
            ></el-autocomplete>
          </el-form-item>
          <el-form-item>
            <el-button @click="signUp">Sign Me Up</el-button>
          </el-form-item>
        </el-form>
      </el-card>
    </div>
  </div>
</template>

<script>
import cityJson from '@/json/locations.json'

export default {
  data() {
    return {
      formData: {
        emailAddress: null,
        location: null
      },
      cities: null
    }
  },
  mounted() {
    this.cities = cityJson.cities.map((v) => {
      return { value: v }
    })
  },
  methods: {
    querySearch(query, callback) {
      const cityData = this.cities
      if (!query) return []
      callback(
        cityData
          .filter((city) => {
            return city.value.toLowerCase().startsWith(query.toLowerCase())
          })
          .splice(0, 10)
      )
    },
    handleSelect(entry) {
      this.formData.location = entry.value
    },
    signUp() {
    }
  }
}
</script>
<style scoped>
.container {
  max-width: 1020px;
  margin: auto;
}

.weather-alert__form {
  margin-top: 30px;
}

.weather-alert__form .el-autocomplete {
  width: 100%;
}

.sub-title {
  margin-bottom: 10px;
}
</style>
