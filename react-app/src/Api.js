import axios from 'axios'

let baseUrl = 'http://silverdeer.flask/api/'



axios.interceptors.request.use(function (config) {

  let token = localStorage.getItem('jwtToken');
  if(token){
    axios.defaults.headers.common['Authorization'] = `JWT ${token}`;
  }

  config.headers.common['Authorization'] = `JWT ${token}`;
  return config;
}, function (error) {
  return Promise.reject(error);
});

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
    login(user){
      return axios.post(baseUrl + 'login', user)
    },
    logout(){
      return axios.get(baseUrl + 'logout')
    }
  }
}