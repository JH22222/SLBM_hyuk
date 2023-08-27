<script setup>
</script>
<template>
  <div v-if=item.poll_key class="card text-center mb-5"
       v-bind:class="{ 'border':!poll,'border-2':!poll,'border-dark': !poll }">
    <div v-for="(selection, idx) in meta.selections2"
         class="form-check form-check-inline btn btn-group btn-outline-dark mx-0" @click="clickBtn(idx+1, selection)">
      <input class="form-check-input" type="radio" :name='"inlineRadioOptions_" + meta.tag+ "_"+item.poll_key'
             :id="'inlineRadio_' + item.poll_key +'_' + idx" :value="meta.value2[idx]" v-model="poll">
      <label class="form-check-label" :for="'inlineRadio_' + item.poll_key +'_' + idx"><span style="padding-left: 4px"> {{ selection }}</span></label>
    </div>
  </div>
</template>
<script>

export default {
  name: 'PollItem2-1',
  components: {},
  props: {
    item: {
      type: Object,
      default: {}
    },
    meta: {
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
    let self = this
    this.emitter.on('reload', function () {
      self.poll = null
    })
  },
  methods: {
    clickBtn(item, poll_key) {
      this.poll = item
      console.log(item, poll_key, this.poll)
    }
  }
}
</script>
<style scoped>
</style>
