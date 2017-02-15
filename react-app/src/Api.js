import axios from 'axios'

let baseUrl = 'http://localhost:5000/api/'


export default {
    Projects: {
        search() {
            return axios.get(baseUrl + 'project/search')
        }
    },
    Auth: {
        me(){
          return axios.get(baseUrl + 'me')
        },
        force_login(){
          return axios.get(baseUrl + 'force-login')
        },
        logout(){
          return axios.get(baseUrl + 'logout')
        }
    }
}