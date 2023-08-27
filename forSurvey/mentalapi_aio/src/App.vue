<script setup>
import PollItem0 from './components/PollItem0.vue'
import PollItem1 from './components/PollItem1.vue'
import PollItem2 from './components/PollItem2.vue'
import PollItem2_1 from './components/PollItem2_1.vue'

</script>

<template>
  <div class="container">
    <div class="row justify-content-md-center">
      <div class="card text-center mb-3 mt-3" :class="{'col-7':!isMobile}">
        <nav class="navbar navbar-light bg-p">
          <div class="input-group">
            <span class="input-group-text">{{ week }} 주차</span>
            <input type="text" class="form-control" placeholder="Userid" aria-label="Userid" v-model="userid">
            <span class="btn btn btn-primary" @click="setUserId">Login</span>
          </div>

        </nav>
        <div v-if="render">
          <div class="card-header mt-2">
            <h5 class="card-title">
              {{ polls.meta.title }}
            </h5>
          </div>
          <div class="card-body">
            <p class="card-text">
              {{ polls.meta.description }}
            </p>
          </div>
        </div>
      </div>
    </div>

  </div>

  <div class="container">
    <div v-if="render">
      <div class="row justify-content-md-center" v-if="(type === 'form0')">
        <h3 :class="{'col-7':!isMobile, 'col-12':isMobile}"><span
            class="badge bg-dark badge-edit"><strong><em>{{ polls.meta.status }}</em></strong></span></h3>
        <div :class="{'col-7':!isMobile, 'col-12':isMobile}">
          <PollItem0 :item="item" :meta="polls.meta" :isMobile="isMobile" v-for="item in polls.item"
                     :key="item['poll_key']"
          />
        </div>
      </div>

      <div class="row justify-content-md-center" v-if="(type === 'form1')">
        <h3 :class="{'col-7':!isMobile, 'col-12':isMobile}"><span
            class="badge bg-dark badge-edit"><strong><em>{{ polls.meta.status }}</em></strong></span></h3>
        <div :class="{'col-7':!isMobile, 'col-12':isMobile}">
          <PollItem1 :item="item" :meta="polls.meta" :isMobile="isMobile" v-for="item in polls.item"
                     :key="item['poll_key']"
          />
        </div>
      </div>
      <div class="row justify-content-md-center" v-if="(type === 'form2')">
        <div :class="{'col-7':!isMobile, 'col-12':isMobile}">
          <PollItem2_1 :item="item" :meta="polls.meta" :isMobile="isMobile" v-for="item in [polls.item[0]]"
                       :key="item['poll_key']"/>
          <div class="row justify-content-md-center">
            <h3><span
                class="badge bg-dark badge-edit"><strong><em>{{ polls.meta.status }}</em></strong></span></h3>
          </div>
          <PollItem2 :item=item :meta="polls.meta" :isMobile="isMobile" v-for="item in polls.item.slice(1)"
                     :key="item['poll_key']"/>
        </div>
      </div>
      <div class="row justify-content-md-center" v-if="(type === 'form3')">
        <h3 :class="{'col-7':!isMobile, 'col-12':isMobile}"><span
            class="badge bg-dark badge-edit"><strong><em>{{ polls.metas[0].status }}</em></strong></span></h3>
        <div :class="{'col-7':!isMobile, 'col-12':isMobile}">
          <PollItem1 :item="item" :meta="polls.meta" :isMobile="isMobile" v-for="item in polls.item.slice(0,3)"
                     :key="item['poll_key']"/>
        </div>
        <h3 :class="{'col-7':!isMobile, 'col-12':isMobile}"><span
            class="badge bg-dark badge-edit"><strong><em>{{ polls.metas[0].status2 }}</em></strong></span></h3>
        <div :class="{'col-7':!isMobile, 'col-12':isMobile}">
          <PollItem1 :item="item" :meta="polls.metas[0]" :isMobile="isMobile" v-for="item in polls.item.slice(3,4)"
                     :key="item['poll_key']"/>
          <PollItem1 :item="item" :meta="polls.metas[1]" :isMobile="isMobile" v-for="item in polls.item.slice(4,5)"
                     :key="item['poll_key']"/>
          <PollItem1 :item="item" :meta="polls.metas[2]" :isMobile="isMobile" v-for="item in polls.item.slice(5,6)"
                     :key="item['poll_key']"/>
          <PollItem1 :item="item" :meta="polls.metas[3]" :isMobile="isMobile" v-for="item in polls.item.slice(6,8)"
                     :key="item['poll_key']"/>
        </div>
      </div>
      <div class="row justify-content-md-center">
        <div class="btn-group" :class="{'col-7':!isMobile, 'col-12':isMobile}">
          <button v-if="!done" class="btn btn-default btn-outline-dark" @click="next">다음</button>
          <div v-else class="btn btn-primary" @click="next">제출</div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import apiHandler from "@/services/apiHandler";
import * as d3 from "d3";
import _ from "lodash";

export default {
  name: 'App',
  data: () => ({
    session: 0,
    polls: [],
    remains: [],
    results: {},
    results_final: [],
    dataset: [],
    isMobile: false,
    nextpage: true,
    page_num: 0,
    week: null,
    render: false,
    type: '',
    done: false,
    userid: undefined
  }),
  watch: {},
  created() {
    if (window.innerWidth <= 760) {
      this.isMobile = true;
    }
  },
  mounted() {
    console.log('mobile', this.isMobile)

    let self = this
    /*
    apiHandler.loadPolls().then(res => {
      console.log('test', res)
      self.dataset = res
      if (self.page_num === 0) {
        self.renderPage(self.page_num, res.data[0].type, res.data[0].tag, res.data[0].data)
      }
    })
    /*
    apiHandler.postPolls().then(res => {
      self.polls = d3.csvParse(res)
      self.remains = self.polls.map(x => x.poll_key)
      console.log('postPolls', self.polls)
      console.log('remains', self.remains)
    })
     */

    self.emitter.on('poll', (x) => {
      self.results[x[0]] = x[1]
      if (x[1]) self.remains = self.remains.filter(item => item !== x[0])
      //console.log(self.remains, x)
    })
  },
  methods: {
    setUserId() {
      //alert('사용자 코드: ' + this.userid)
      let self = this
      apiHandler.loadUser(this.userid).then((res) => {
        this.week = res.data.week
        self.dataset = res.data['dataset']
        let valid_save = this.getCookie('userid');
        console.log('user', res, valid_save, self.userid)
        if (valid_save === self.userid) {
          if (typeof (Storage) !== "undefined") {
            // Code for localStorage/sessionStorage.
            // load the session
            let saved_data = JSON.parse(localStorage.getItem(valid_save))
            this.load(saved_data)
          } else {
            // Sorry! No Web Storage support..
            alert("임시 저장을 지원 하지 않는 브라우저 입니다.")
          }
        } else {
          self.renderPage(self.page_num, self.dataset[0].type, self.dataset[0].tag, self.dataset[0].data)
        }
      })
    },
    submit() {
      console.log('submit', JSON.stringify(this.results_final))
    },
    renderPage(page, type, tag, data) {
      this.render = false
      this.done = false
      if (this.page_num === this.dataset.length - 1) this.done = true
      switch (type) {
        case 'form0': {
          this.tag = tag
          this.type = type
          this.polls = this.parser0(data)
          break;
        }
        case 'form1': {
          this.tag = tag
          this.type = type
          this.polls = this.parser1(data)
          break;
        }
        case 'form2': {
          this.tag = tag
          this.type = type
          this.polls = this.parser2(data)
          break;
        }
        case 'form3': {
          console.log('form3')
          this.tag = tag
          this.type = type
          this.polls = this.parser3(data)
          break;
        }
      }
      this.render = true
      this.emitter.emit('reload', true)
    },
    parser0(data) {
      let item = []
      let meta = {'title': '', 'description': '', 'selections': [], 'value': [], 'status': '', 'tag': this.tag + ""}
      let spliter = 0
      data.forEach((line) => {
        if (line === "") {
          spliter += 1
          return
        }
        if (spliter === 0) {
          meta.title = line
        }
        if (spliter === 1) {
          meta.description = line
        }
        if (spliter === 2) {
          meta.status = line
        }
        if (spliter === 3) {
          let temp = line.split(' ')
          const poll_key = temp[0]
          temp.shift()
          const poll = temp.join(' ')
          item.push({poll_key, poll})
        }
      })
      this.remains = item.map(x => x.poll_key)
      this.results = []
      console.log({meta, item})
      return {meta, item}
    },
    parser1(data) {
      let item = []
      let meta = {'title': '', 'description': '', 'selections': [], 'value': [], 'status': '', 'tag': this.tag + ""}
      let spliter = 0
      data.forEach((line) => {
        if (line === "") {
          spliter += 1
          return
        }
        if (spliter === 0) {
          meta.title = line
        }
        if (spliter === 1) {
          meta.description = line
        }
        if (spliter === 2) {
          meta.selections = line.split(',')
        }
        if (spliter === 3) {
          meta.value = line.split(',')
        }
        if (spliter === 4) {
          meta.status = line
        }
        if (spliter === 5) {
          let temp = line.split(' ')
          const poll_key = temp[0]
          temp.shift()
          const poll = temp.join(' ')
          item.push({poll_key, poll})
        }
      })
      this.remains = item.map(x => x.poll_key)
      this.results = []
      console.log({meta, item})
      return {meta, item}
    },
    parser2(data) {
      let item = []
      let meta = {
        'title': '',
        'description': '',
        'selections': [],
        'value': [],
        'selections2': [],
        'value2': [],
        'status': '',
        'tag': this.tag + ""
      }
      let spliter = 0
      data.forEach((line) => {
        if (line === "") {
          spliter += 1
          return
        }
        if (spliter === 0) {
          meta.title = line
        }
        if (spliter === 1) {
          meta.description = line
        }
        if (spliter === 2) {
          meta.selections2 = line.split(';')
        }
        if (spliter === 3) {
          meta.value2 = line.split(',')
        }
        if (spliter === 4) {
          meta.status = line
        }
        if (spliter === 5) {
          meta.selections = line.split(',')
          item.push({poll_key: 1, poll: ''})
        }
        if (spliter === 6) {
          meta.value = line.split(',')
        }
        if (spliter === 7) {
          let temp = line.split(' ')
          const poll_key = ((+temp[0]) + 1) + ''
          temp.shift()
          const poll = temp.join(' ')
          item.push({poll_key, poll})
        }
      })
      this.remains = item.map(x => x.poll_key)
      this.results = []
      console.log({meta, item})
      return {meta, item}
    },
    parser3(data) {
      let item = []
      let meta = {
        'title': '',
        'description': '',
        'selections': [],
        'value': [],
        'status': '',
        'status2': '',
        'tag': this.tag + ""
      }
      let spliter = 0
      data.forEach((line) => {
        if (line === "") {
          spliter += 1
          return
        }
        if (spliter === 0) {
          meta.title = line
        }
        if (spliter === 1) {
          meta.description = line
        }
        if (spliter === 2) {
          meta.selections = line.split(',')
        }
        if (spliter === 3) {
          meta.value = line.split(',')
        }
        if (spliter === 4) {
          meta.status = line
        }
        if (spliter === 5) {
          let temp = line.split(' ')
          const poll_key = temp[0]
          temp.shift()
          const poll = temp.join(' ')
          item.push({poll_key, poll})
        }
        if (spliter === 6) {
          meta.status2 = line
        }
      })
      let metas = []

      //metas.push(_.cloneDeep(meta))
      metas.push(_.cloneDeep(meta))
      metas.push(_.cloneDeep(meta))
      metas.push(_.cloneDeep(meta))
      metas.push(_.cloneDeep(meta))

      console.log('test meta', metas)
      spliter = 0
      data.forEach((line) => {
        if (line === "") {
          spliter += 1
          return
        }
        if (spliter === 7) {
          metas[0].selections = line.split(',')
        }
        if (spliter === 8) {
          let temp = line.split(' ')
          const poll_key = temp[0]
          temp.shift()
          const poll = temp.join(' ')
          item.push({poll_key, poll})
        }

        if (spliter === 9) {
          metas[1].selections = line.split(',')
        }

        if (spliter === 10) {
          let temp = line.split(' ')
          const poll_key = temp[0]
          temp.shift()
          const poll = temp.join(' ')
          item.push({poll_key, poll})
        }

        if (spliter === 11) {
          metas[2].selections = line.split(',')
        }

        if (spliter === 12) {
          let temp = line.split(' ')
          const poll_key = temp[0]
          temp.shift()
          const poll = temp.join(' ')
          item.push({poll_key, poll})
        }
        if (spliter === 13) {
          metas[3].selections = line.split(',')
        }

        if (spliter === 14) {
          let temp = line.split(' ')
          const poll_key = temp[0]
          temp.shift()
          const poll = temp.join(' ')
          item.push({poll_key, poll})
        }
      })

      this.remains = item.map(x => x.poll_key)
      this.results = []
      console.log('metas', {meta, metas, item})
      return {'meta': meta, 'metas': metas, item}
    },
    load(data) {
      this.render = false
      this.page_num = (+data['page_num'])
      this.results_final = data['results_final']
      console.log('loaded', this.page_num, this.results_final)
      this.renderPage(this.page_num, this.dataset[this.page_num].type, this.dataset[this.page_num].tag, this.dataset[this.page_num].data)
    },
    save(userid, page_num, results_final) {
      if (typeof (Storage) !== "undefined") {
        // Code for localStorage/sessionStorage.
        // Store
        let data = JSON.stringify({userid, page_num, results_final})
        localStorage.setItem(userid, data);
      } else {
        // Sorry! No Web Storage support..
        alert("임시 저장을 지원 하지 않는 브라우저 입니다.")
      }
      let expire = new Date();
      expire.setHours(23);
      expire.setMinutes(59);
      document.cookie = `userid=${userid}; expires=${expire}"`
    },
    getCookie(cname) {
      let name = cname + "=";
      let decodedCookie = decodeURIComponent(document.cookie);
      let ca = decodedCookie.split(';');
      for (let i = 0; i < ca.length; i++) {
        let c = ca[i];
        while (c.charAt(0) == ' ') {
          c = c.substring(1);
        }
        if (c.indexOf(name) == 0) {
          return c.substring(name.length, c.length);
        }
      }
      return null;
    },
    eraseCookie(cname) {
      document.cookie = cname + '=; Max-Age=-99999999;';
    },
    next() {
      // check userid
      let self = this
      console.log(this.dataset.length, this.page_num)
      if (this.page_num === this.dataset.length - 1) this.done = true
      if (this.dataset.length < this.page_num) {
        alert('해당 주차에 설문지가 없습니다.')
        return
      }
      if (!this.userid) {
        alert('사용자 코드를(Userid) 입력해주세요.')
        return
      }
      // check remaining items
      if (this.remains.length !== 0) {
        alert("미확인 문제: " + JSON.stringify(this.remains))
      } else {
        this.render = false
        this.page_num = this.page_num + 1
        if (this.dataset.length > this.page_num) {
          // store results
          let store_this = Object.keys(this.results).map((key, idx) => {
            return {'userid': this.userid, tag: this.tag, poll_key: key, poll: this.results[key]}
          })
          store_this = store_this.filter(x => x.poll)
          self.results_final = self.results_final.concat(store_this)
          // save current results
          self.save(self.userid, this.page_num, self.results_final)
          // render new page
          this.renderPage(this.page_num, this.dataset[this.page_num].type, this.dataset[this.page_num].tag, this.dataset[this.page_num].data)
        }
        if (this.done) {
          let store_this = Object.keys(this.results).map((key, idx) => {
            return {'userid': this.userid, tag: this.tag, poll_key: key, poll: this.results[key]}
          })
          store_this = store_this.filter(x => x.poll)
          self.results_final = self.results_final.concat(store_this)
          console.log('submit', JSON.stringify(this.results_final))
          apiHandler.submitPolls(this.results_final)
          self.eraseCookie('userid')
        }
      }
    }
  }

}
</script>
<style scoped>
.badge-edit {
  white-space: normal;
  text-align: justify-all;
}
</style>