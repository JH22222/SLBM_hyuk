import axios from 'axios'

export default {
    checkAuth() {},
    loadUser(authCode){
        console.log('submitPolls')
        return axios.post('mentalapi/load_user/', {authCode})
            .then(res => {
                return res.data
            })
    },
    loadPolls() {
        console.log('loading polls')
        return axios.post('mentalapi/load_polls/', {})
            .then(res => {
                return res.data
            })
    },
    postPolls() {
        console.log('getEvent')
        return axios.post('mentalapi/post_polls/', {})
            .then(res => {
                return res.data
            })
    },
    submitPolls(polls) {
        console.log('submitPolls')
        return axios.post('mentalapi/submit_polls/', {polls})
            .then(res => {
                return res.data
            })
    },
    postRoutes(start, end, eventId, datetime, num_traj, start_latlng, end_latlng, session) {
        console.log('getEvent')
        return axios.post('post_routes', {
            start, end, eventId, datetime, num_traj,
            start_latlng, end_latlng, session
        })
            .then(res => {
                return res.data
            })
    }
}
