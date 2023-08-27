<script setup>
</script>
<template>
  <div v-if=item.poll_key class="card text-center mb-5"
       v-bind:class="{ 'border':!poll,'border-2':!poll,'border-dark': !poll }">
    <div class="card-body bg-info">
      <h5 class="card-text text-light"><strong>{{item.poll_key}}. {{ item.poll }} </strong></h5>
    </div>
    <div class="card-footer text-muted">
      <div class="form-check form-check-inline btn btn-group btn-outline-dark px-3" @click="clickBtn(0, item.poll_key)">
        <input class="form-check-input" type="radio" :name='"inlineRadioOptions" + item.poll_key'
               :id="'inlineRadio1' + item.poll_key"   value="0" v-model="poll">
        <label class="form-check-label" :for="'inlineRadio1' + item.poll_key">극히 드물게 (1일 이하)</label>
      </div>
      <div class="form-check form-check-inline btn btn-group btn-outline-dark px-3" @click="clickBtn(1, item.poll_key)">
        <input class="form-check-input" type="radio" :name='"inlineRadioOptions" + item.poll_key'
               :id="'inlineRadio2' + item.poll_key" value="1" v-model="poll">
        <label class="form-check-label" :for="'inlineRadio2' + item.poll_key">가끔 (1~2일)</label>
      </div>
      <div class="form-check form-check-inline btn btn-group btn-outline-dark px-3" @click="clickBtn(2, item.poll_key)">
        <input class="form-check-input" type="radio" :name='"inlineRadioOptions" + item.poll_key'
               :id="'inlineRadio3' + item.poll_key" value="2" v-model="poll">
        <label class="form-check-label" :for="'inlineRadio3' + item.poll_key">자주 (3~4일)</label>
      </div>
      <div class="form-check form-check-inline btn btn-group btn-outline-dark px-3" @click="clickBtn(3, item.poll_key)">
        <input class="form-check-input" type="radio" :name='"inlineRadioOptions" + item.poll_key'
               :id="'inlineRadio4' + item.poll_key" value="3" v-model="poll">
        <label class="form-check-label" :for="'inlineRadio4' + item.poll_key">거의 대부분 (5일 이상)</label>
      </div>
    </div>
  </div>
</template>
<script>

export default {
  name: 'PollItem',
  components: {},
  props:{
    item: {
      type: Object,
      default: {}
    },
    isMobile: {
      type: Boolean,
      default: false
    }
  },
  data: () => ({
    poll: null
  }),
  watch: {
    poll: function () {
      this.emitter.emit('poll', [this.item.poll_key, this.poll])
    }
  },
  mounted() {
    console.log('p')
  },
  methods:{
    clickBtn(item, poll_key) {
      this.poll = item + ''
    }
  }
}
</script>
<style scoped>
</style>
