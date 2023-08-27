<script setup>
</script>
<template>
  <div v-if=item.poll_key class="card text-center mb-5"
       v-bind:class="{ 'border':!poll,'border-2':!poll,'border-dark': !poll }">
    <div class="card-body bg-info">
      <h5 class="card-text text-light"><strong>{{ item.poll_key }}. {{ item.poll }} </strong></h5>
    </div>
    <!-- <div class="card-footer text-muted" v-if="item.poll_key !== '3'">
      {{ poll }} 시<input class="form-range btn btn-outline-dark" type="range" min="0" max="24" step="0.5"
                       :id="'inlineRadio_' + item.poll_key +'_' + idx" v-model="poll">
    </div> -->
    <div class="card-footer text-muted" v-if="item.poll_key !== '3'">
      <template v-if="item.poll_key === '3-1'">
        {{ poll }}분<input class="form-range btn btn-outline-dark" type="range" min="0" max="500" step="1"
                             :id="'inlineRadio_' + item.poll_key +'_' + idx" v-model="poll">
      </template>
      <template v-else>
        {{ poll }}시<input class="form-range btn btn-outline-dark" type="range" min="0" max="24" step="0.5"
                            :id="'inlineRadio_' + item.poll_key +'_' + idx" v-model="poll">
      </template>
    </div>
    <!-- <div class="card-footer text-muted" v-if="item.poll_key == '3-1'">
      {{ poll }} 분<input class="form-range btn btn-outline-dark" type="range" min="0" max="180" step="1"
                       :id="'inlineRadio_' + item.poll_key +'_' + idx" v-model="poll">
    </div> -->
    <div class="card-footer text-muted" v-else>
      <div v-for="(selection, idx) in selections"
           class="form-check form-check-inline btn btn-group btn-outline-dark px-3"
           @click="clickBtn(idx+1, item.poll_key)">
        <input class="form-check-input" type="radio" :name='"inlineRadioOptions_" + "sleep" + "_"+item.poll_key'
               :id="'inlineRadio_sleep' + item.poll_key +'_' + idx" :value="idx + 1" v-model="poll">
        <label class="form-check-label" :for="'inlineRadio_sleep' + item.poll_key +'_' + idx"><span
            style="padding-left: 4px"> {{ selection }}</span></label>
      </div>
    </div>
  </div>
</template>
<script>

export default {
  name: 'PollItem0',
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
    poll: null,
    selections: ['예', '아니오']
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
      console.log(poll_key, item)
      this.poll = item + ''
    }
  }
}
</script>
<style scoped>
</style>
