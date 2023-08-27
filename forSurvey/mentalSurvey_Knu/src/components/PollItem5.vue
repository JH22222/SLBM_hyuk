<script setup>
</script>
<template>
  <div v-if=item.poll_key class="card text-center mb-5"
       v-bind:class="{ 'border':!poll,'border-2':!poll,'border-dark': !poll }">
    <div class="card-body bg-info">
      <h5 class="card-text text-light"><strong>{{item.poll_key}}. {{ item.poll }} </strong></h5>
    </div>
    <div class="card-footer text-muted">
      <!-- <div v-if="item.poll_key === '이름.'" class="form-check form-check-inline btn btn-group btn-outline-dark px-3">
        <input type="text" class="form-control" placeholder="홍길동" aria-label="이름" v-model="poll">
      </div>        -->

      <div v-if="item.poll_key === '1'" class="btn-group" role="group" aria-label="Gender Selection">
        <div v-for="(option, index) in meta.selections[0]" :key="index" class="form-check form-check-inline btn btn-outline-dark px-3" @click="clickBtn(meta.value[0], item.poll_key)">
          <input class="form-check-input" :name="'inlineRadioOptions_' + meta.tag + '_' + item.poll_key" :id="'inlineRadio_' + item.poll_key + '_' + index" :value="option" v-model="poll" type="radio">
          <label class="form-check-label" :for="'inlineRadio_' + item.poll_key + '_' + index">
            <span style="padding-left: 4px">{{ option }}</span>
          </label>        
        </div>
      </div>

      <div v-if="item.poll_key === '2'" class="form-check form-check-inline btn btn-group btn-outline-dark px-3">
        <input type="text" class="form-control" placeholder="2000" aria-label="Birth year" v-model="poll">
      </div> 

      <div v-if="item.poll_key === '3'" class="btn-group" role="group" aria-label="Gender Selection">
        <div v-for="(option, index) in meta.selections[2]" :key="index" class="form-check form-check-inline btn btn-outline-dark px-3" @click="clickBtn(meta.value[0], item.poll_key)">
          <input class="form-check-input" :name="'inlineRadioOptions_' + meta.tag + '_' + item.poll_key" :id="'inlineRadio_' + item.poll_key + '_' + index" :value="option" v-model="poll" type="radio">
          <label class="form-check-label" :for="'inlineRadio_' + item.poll_key + '_' + index">
            <span style="padding-left: 4px">{{ option }}</span>
          </label>        
        </div>
      </div>

      <div v-if="item.poll_key === '4'" class="btn-group" role="group" aria-label="Gender Selection">
        <div v-for="(option, index) in meta.selections[3]" :key="index" class="form-check form-check-inline btn btn-outline-dark px-3" @click="clickBtn(meta.value[0], item.poll_key)">
          <input class="form-check-input" :name="'inlineRadioOptions_' + meta.tag + '_' + item.poll_key" :id="'inlineRadio_' + item.poll_key + '_' + index" :value="option" v-model="poll" type="radio">
          <label class="form-check-label" :for="'inlineRadio_' + item.poll_key + '_' + index">
            <span style="padding-left: 4px">{{ option }}</span>
          </label>        
        </div>
      </div>

      <div v-if="item.poll_key === '5'" class="btn-group" role="group" aria-label="Gender Selection">
        <div v-for="(option, index) in meta.selections[4]" :key="index" class="form-check form-check-inline btn btn-outline-dark px-3" @click="clickBtn(meta.value[0], item.poll_key)">
          <input class="form-check-input" :name="'inlineRadioOptions_' + meta.tag + '_' + item.poll_key" :id="'inlineRadio_' + item.poll_key + '_' + index" :value="option" v-model="poll" type="radio">
          <label class="form-check-label" :for="'inlineRadio_' + item.poll_key + '_' + index">
            <span style="padding-left: 4px">{{ option }}</span>
          </label>        
        </div>
      </div>

      <div v-if="item.poll_key === '6'" class="btn-group" role="group" aria-label="Gender Selection">
        <div v-for="(option, index) in meta.selections[5]" :key="index" class="form-check form-check-inline btn btn-outline-dark px-3" @click="clickBtn(meta.value[0], item.poll_key)">
          <input class="form-check-input" :name="'inlineRadioOptions_' + meta.tag + '_' + item.poll_key" :id="'inlineRadio_' + item.poll_key + '_' + index" :value="option" v-model="poll" type="radio">
          <label class="form-check-label" :for="'inlineRadio_' + item.poll_key + '_' + index">
            <span style="padding-left: 4px">{{ option }}</span>
          </label>        
        </div>
      </div>

      <div v-if="item.poll_key === '7'" class="btn-group" role="group" aria-label="Gender Selection">
        <div v-for="(option, index) in meta.selections[6]" :key="index" class="form-check form-check-inline btn btn-outline-dark px-3" @click="clickBtn(meta.value[0], item.poll_key)">
          <input class="form-check-input" :name="'inlineRadioOptions_' + meta.tag + '_' + item.poll_key" :id="'inlineRadio_' + item.poll_key + '_' + index" :value="option" v-model="poll" type="radio">
          <label class="form-check-label" :for="'inlineRadio_' + item.poll_key + '_' + index">
            <span style="padding-left: 4px">{{ option }}</span>
          </label>        
        </div>
      </div>

      <div v-if="item.poll_key === '8'" class="btn-group" role="group" aria-label="Gender Selection">
        <div v-for="(option, index) in meta.selections[7]" :key="index" class="form-check form-check-inline btn btn-outline-dark px-3" @click="clickBtn(meta.value[0], item.poll_key)">
          <input class="form-check-input" :name="'inlineRadioOptions_' + meta.tag + '_' + item.poll_key" :id="'inlineRadio_' + item.poll_key + '_' + index" :value="option" v-model="poll" type="radio">
          <label class="form-check-label" :for="'inlineRadio_' + item.poll_key + '_' + index">
            <span style="padding-left: 4px">{{ option }}</span>
          </label>        
        </div>
      </div>

      <div v-if="item.poll_key === '9'" class="btn-group" role="group" aria-label="Gender Selection">
        <div v-for="(option, index) in meta.selections[8]" :key="index" class="form-check form-check-inline btn btn-outline-dark px-3" @click="clickBtn(meta.value[0], item.poll_key)">
          <input class="form-check-input" :name="'inlineRadioOptions_' + meta.tag + '_' + item.poll_key" :id="'inlineRadio_' + item.poll_key + '_' + index" :value="option" v-model="poll" type="radio">
          <label class="form-check-label" :for="'inlineRadio_' + item.poll_key + '_' + index">
            <span style="padding-left: 4px">{{ option }}</span>
          </label>        
        </div>
      </div>

      <div v-if="item.poll_key === '10'" class="btn-group" role="group" aria-label="Gender Selection">
        <div v-for="(option, index) in meta.selections[9]" :key="index" class="form-check form-check-inline btn btn-outline-dark px-3" @click="clickBtn(meta.value[0], item.poll_key)">
          <input class="form-check-input" :name="'inlineRadioOptions_' + meta.tag + '_' + item.poll_key" :id="'inlineRadio_' + item.poll_key + '_' + index" :value="option" v-model="poll" type="radio">
          <label class="form-check-label" :for="'inlineRadio_' + item.poll_key + '_' + index">
            <span style="padding-left: 4px">{{ option }}</span>
          </label>        
        </div>
      </div>

      <div v-if="item.poll_key === '11'" class="btn-group" role="group" aria-label="Gender Selection">
        <div v-for="(option, index) in meta.selections[10]" :key="index" class="form-check form-check-inline btn btn-outline-dark px-3" @click="clickBtn(meta.value[0], item.poll_key)">
          <input class="form-check-input" :name="'inlineRadioOptions_' + meta.tag + '_' + item.poll_key" :id="'inlineRadio_' + item.poll_key + '_' + index" :value="option" v-model="poll" type="radio">
          <label class="form-check-label" :for="'inlineRadio_' + item.poll_key + '_' + index">
            <span style="padding-left: 4px">{{ option }}</span>
          </label>        
        </div>
      </div>

      <div v-if="item.poll_key === '12-1'" class="btn-group" role="group" aria-label="Gender Selection">
        <div v-for="(option, index) in meta.selections[12]" :key="index" class="form-check form-check-inline btn btn-outline-dark px-3" @click="clickBtn(meta.value[0], item.poll_key)">
          <input class="form-check-input" :name="'inlineRadioOptions_' + meta.tag + '_' + item.poll_key" :id="'inlineRadio_' + item.poll_key + '_' + index" :value="option" v-model="poll" type="radio">
          <label class="form-check-label" :for="'inlineRadio_' + item.poll_key + '_' + index">
            <span style="padding-left: 4px">{{ option }}</span>
          </label>        
        </div>
      </div>

      <div v-if="item.poll_key === '12-2'" class="btn-group" role="group" aria-label="Gender Selection">
        <div v-for="(option, index) in meta.selections[13]" :key="index" class="form-check form-check-inline btn btn-outline-dark px-3" @click="clickBtn(meta.value[0], item.poll_key)">
          <input class="form-check-input" :name="'inlineRadioOptions_' + meta.tag + '_' + item.poll_key" :id="'inlineRadio_' + item.poll_key + '_' + index" :value="option" v-model="poll" type="radio">
          <label class="form-check-label" :for="'inlineRadio_' + item.poll_key + '_' + index">
            <span style="padding-left: 4px">{{ option }}</span>
          </label>        
        </div>
      </div>

      <div v-if="item.poll_key === '12-3'" class="btn-group" role="group" aria-label="Gender Selection">
        <div v-for="(option, index) in meta.selections[14]" :key="index" class="form-check form-check-inline btn btn-outline-dark px-3" @click="clickBtn(meta.value[0], item.poll_key)">
          <input class="form-check-input" :name="'inlineRadioOptions_' + meta.tag + '_' + item.poll_key" :id="'inlineRadio_' + item.poll_key + '_' + index" :value="option" v-model="poll" type="radio">
          <label class="form-check-label" :for="'inlineRadio_' + item.poll_key + '_' + index">
            <span style="padding-left: 4px">{{ option }}</span>
          </label>        
        </div>
      </div>

      <div v-if="item.poll_key === '13'" class="btn-group" role="group" aria-label="Gender Selection">
        <div v-for="(option, index) in meta.selections[15]" :key="index" class="form-check form-check-inline btn btn-outline-dark px-3" @click="clickBtn(meta.value[0], item.poll_key)">
          <input class="form-check-input" :name="'inlineRadioOptions_' + meta.tag + '_' + item.poll_key" :id="'inlineRadio_' + item.poll_key + '_' + index" :value="option" v-model="poll" type="radio">
          <label class="form-check-label" :for="'inlineRadio_' + item.poll_key + '_' + index">
            <span style="padding-left: 4px">{{ option }}</span>
          </label>        
        </div>
      </div>

      <div v-if="item.poll_key === '14'" class="btn-group" role="group" aria-label="Gender Selection">
        <div v-for="(option, index) in meta.selections[16]" :key="index" class="form-check form-check-inline btn btn-outline-dark px-3" @click="clickBtn(meta.value[0], item.poll_key)">
          <input class="form-check-input" :name="'inlineRadioOptions_' + meta.tag + '_' + item.poll_key" :id="'inlineRadio_' + item.poll_key + '_' + index" :value="option" v-model="poll" type="radio">
          <label class="form-check-label" :for="'inlineRadio_' + item.poll_key + '_' + index">
            <span style="padding-left: 4px">{{ option }}</span>
          </label>        
        </div>
      </div>

      <div v-if="item.poll_key === '15'" class="btn-group" role="group" aria-label="Gender Selection">
        <div v-for="(option, index) in meta.selections[17]" :key="index" class="form-check form-check-inline btn btn-outline-dark px-3" @click="clickBtn(meta.value[0], item.poll_key)">
          <input class="form-check-input" :name="'inlineRadioOptions_' + meta.tag + '_' + item.poll_key" :id="'inlineRadio_' + item.poll_key + '_' + index" :value="option" v-model="poll" type="radio">
          <label class="form-check-label" :for="'inlineRadio_' + item.poll_key + '_' + index">
            <span style="padding-left: 4px">{{ option }}</span>
          </label>        
        </div>
      </div>

      <div v-if="item.poll_key === '16'" class="btn-group" role="group" aria-label="Gender Selection">
        <div v-for="(option, index) in meta.selections[18]" :key="index" class="form-check form-check-inline btn btn-outline-dark px-3" @click="clickBtn(meta.value[0], item.poll_key)">
          <input class="form-check-input" :name="'inlineRadioOptions_' + meta.tag + '_' + item.poll_key" :id="'inlineRadio_' + item.poll_key + '_' + index" :value="option" v-model="poll" type="radio">
          <label class="form-check-label" :for="'inlineRadio_' + item.poll_key + '_' + index">
            <span style="padding-left: 4px">{{ option }}</span>
          </label>        
        </div>
      </div>

      <div v-if="item.poll_key === '17-1'" class="btn-group" role="group" aria-label="Gender Selection">
        <div v-for="(option, index) in meta.selections[20]" :key="index" class="form-check form-check-inline btn btn-outline-dark px-3" @click="clickBtn(meta.value[0], item.poll_key)">
          <input class="form-check-input" :name="'inlineRadioOptions_' + meta.tag + '_' + item.poll_key" :id="'inlineRadio_' + item.poll_key + '_' + index" :value="option" v-model="poll" type="radio">
          <label class="form-check-label" :for="'inlineRadio_' + item.poll_key + '_' + index">
            <span style="padding-left: 4px">{{ option }}</span>
          </label>        
        </div>
      </div>

      <div v-if="item.poll_key === '17-2'" class="btn-group" role="group" aria-label="Gender Selection">
        <div v-for="(option, index) in meta.selections[21]" :key="index" class="form-check form-check-inline btn btn-outline-dark px-3" @click="clickBtn(meta.value[0], item.poll_key)">
          <input class="form-check-input" :name="'inlineRadioOptions_' + meta.tag + '_' + item.poll_key" :id="'inlineRadio_' + item.poll_key + '_' + index" :value="option" v-model="poll" type="radio">
          <label class="form-check-label" :for="'inlineRadio_' + item.poll_key + '_' + index">
            <span style="padding-left: 4px">{{ option }}</span>
          </label>        
        </div>
      </div>

      <div v-if="item.poll_key === '17-3'" class="btn-group" role="group" aria-label="Gender Selection">
        <div v-for="(option, index) in meta.selections[22]" :key="index" class="form-check form-check-inline btn btn-outline-dark px-3" @click="clickBtn(meta.value[0], item.poll_key)">
          <input class="form-check-input" :name="'inlineRadioOptions_' + meta.tag + '_' + item.poll_key" :id="'inlineRadio_' + item.poll_key + '_' + index" :value="option" v-model="poll" type="radio">
          <label class="form-check-label" :for="'inlineRadio_' + item.poll_key + '_' + index">
            <span style="padding-left: 4px">{{ option }}</span>
          </label>        
        </div>
      </div>

      <div v-if="item.poll_key === '17-4'" class="btn-group" role="group" aria-label="Gender Selection">
        <div v-for="(option, index) in meta.selections[23]" :key="index" class="form-check form-check-inline btn btn-outline-dark px-3" @click="clickBtn(meta.value[0], item.poll_key)">
          <input class="form-check-input" :name="'inlineRadioOptions_' + meta.tag + '_' + item.poll_key" :id="'inlineRadio_' + item.poll_key + '_' + index" :value="option" v-model="poll" type="radio">
          <label class="form-check-label" :for="'inlineRadio_' + item.poll_key + '_' + index">
            <span style="padding-left: 4px">{{ option }}</span>
          </label>        
        </div>
      </div>

      <div v-if="item.poll_key === '17-5'" class="btn-group" role="group" aria-label="Gender Selection">
        <div v-for="(option, index) in meta.selections[24]" :key="index" class="form-check form-check-inline btn btn-outline-dark px-3" @click="clickBtn(meta.value[0], item.poll_key)">
          <input class="form-check-input" :name="'inlineRadioOptions_' + meta.tag + '_' + item.poll_key" :id="'inlineRadio_' + item.poll_key + '_' + index" :value="option" v-model="poll" type="radio">
          <label class="form-check-label" :for="'inlineRadio_' + item.poll_key + '_' + index">
            <span style="padding-left: 4px">{{ option }}</span>
          </label>        
        </div>
      </div>

      <div v-if="item.poll_key === '17-6'" class="btn-group" role="group" aria-label="Gender Selection">
        <div v-for="(option, index) in meta.selections[25]" :key="index" class="form-check form-check-inline btn btn-outline-dark px-3" @click="clickBtn(meta.value[0], item.poll_key)">
          <input class="form-check-input" :name="'inlineRadioOptions_' + meta.tag + '_' + item.poll_key" :id="'inlineRadio_' + item.poll_key + '_' + index" :value="option" v-model="poll" type="radio">
          <label class="form-check-label" :for="'inlineRadio_' + item.poll_key + '_' + index">
            <span style="padding-left: 4px">{{ option }}</span>
          </label>        
        </div>
      </div>

      <div v-if="item.poll_key === '17-7'" class="btn-group" role="group" aria-label="Gender Selection">
        <div v-for="(option, index) in meta.selections[26]" :key="index" class="form-check form-check-inline btn btn-outline-dark px-3" @click="clickBtn(meta.value[0], item.poll_key)">
          <input class="form-check-input" :name="'inlineRadioOptions_' + meta.tag + '_' + item.poll_key" :id="'inlineRadio_' + item.poll_key + '_' + index" :value="option" v-model="poll" type="radio">
          <label class="form-check-label" :for="'inlineRadio_' + item.poll_key + '_' + index">
            <span style="padding-left: 4px">{{ option }}</span>
          </label>        
        </div>
      </div>

      <div v-if="item.poll_key === '17-8'" class="btn-group" role="group" aria-label="Gender Selection">
        <div v-for="(option, index) in meta.selections[27]" :key="index" class="form-check form-check-inline btn btn-outline-dark px-3" @click="clickBtn(meta.value[0], item.poll_key)">
          <input class="form-check-input" :name="'inlineRadioOptions_' + meta.tag + '_' + item.poll_key" :id="'inlineRadio_' + item.poll_key + '_' + index" :value="option" v-model="poll" type="radio">
          <label class="form-check-label" :for="'inlineRadio_' + item.poll_key + '_' + index">
            <span style="padding-left: 4px">{{ option }}</span>
          </label>        
        </div>
      </div>

      <div v-if="item.poll_key === '17-9'" class="btn-group" role="group" aria-label="Gender Selection">
        <div v-for="(option, index) in meta.selections[28]" :key="index" class="form-check form-check-inline btn btn-outline-dark px-3" @click="clickBtn(meta.value[0], item.poll_key)">
          <input class="form-check-input" :name="'inlineRadioOptions_' + meta.tag + '_' + item.poll_key" :id="'inlineRadio_' + item.poll_key + '_' + index" :value="option" v-model="poll" type="radio">
          <label class="form-check-label" :for="'inlineRadio_' + item.poll_key + '_' + index">
            <span style="padding-left: 4px">{{ option }}</span>
          </label>        
        </div>
      </div>

      <div v-if="item.poll_key === '18-1'" class="btn-group" role="group" aria-label="Gender Selection">
        <div v-for="(option, index) in meta.selections[30]" :key="index" class="form-check form-check-inline btn btn-outline-dark px-3" @click="clickBtn(meta.value[0], item.poll_key)">
          <input class="form-check-input" :name="'inlineRadioOptions_' + meta.tag + '_' + item.poll_key" :id="'inlineRadio_' + item.poll_key + '_' + index" :value="option" v-model="poll" type="radio">
          <label class="form-check-label" :for="'inlineRadio_' + item.poll_key + '_' + index">
            <span style="padding-left: 4px">{{ option }}</span>
          </label>        
        </div>
      </div>

      <div v-if="item.poll_key === '18-2'" class="btn-group" role="group" aria-label="Gender Selection">
        <div v-for="(option, index) in meta.selections[31]" :key="index" class="form-check form-check-inline btn btn-outline-dark px-3" @click="clickBtn(meta.value[0], item.poll_key)">
          <input class="form-check-input" :name="'inlineRadioOptions_' + meta.tag + '_' + item.poll_key" :id="'inlineRadio_' + item.poll_key + '_' + index" :value="option" v-model="poll" type="radio">
          <label class="form-check-label" :for="'inlineRadio_' + item.poll_key + '_' + index">
            <span style="padding-left: 4px">{{ option }}</span>
          </label>        
        </div>
      </div>

      <div v-if="item.poll_key === '18-3'" class="btn-group" role="group" aria-label="Gender Selection">
        <div v-for="(option, index) in meta.selections[32]" :key="index" class="form-check form-check-inline btn btn-outline-dark px-3" @click="clickBtn(meta.value[0], item.poll_key)">
          <input class="form-check-input" :name="'inlineRadioOptions_' + meta.tag + '_' + item.poll_key" :id="'inlineRadio_' + item.poll_key + '_' + index" :value="option" v-model="poll" type="radio">
          <label class="form-check-label" :for="'inlineRadio_' + item.poll_key + '_' + index">
            <span style="padding-left: 4px">{{ option }}</span>
          </label>        
        </div>
      </div>

      <div v-if="item.poll_key === '18-4'" class="btn-group" role="group" aria-label="Gender Selection">
        <div v-for="(option, index) in meta.selections[33]" :key="index" class="form-check form-check-inline btn btn-outline-dark px-3" @click="clickBtn(meta.value[0], item.poll_key)">
          <input class="form-check-input" :name="'inlineRadioOptions_' + meta.tag + '_' + item.poll_key" :id="'inlineRadio_' + item.poll_key + '_' + index" :value="option" v-model="poll" type="radio">
          <label class="form-check-label" :for="'inlineRadio_' + item.poll_key + '_' + index">
            <span style="padding-left: 4px">{{ option }}</span>
          </label>        
        </div>
      </div>

      <div v-if="item.poll_key === '18-5'" class="btn-group" role="group" aria-label="Gender Selection">
        <div v-for="(option, index) in meta.selections[34]" :key="index" class="form-check form-check-inline btn btn-outline-dark px-3" @click="clickBtn(meta.value[0], item.poll_key)">
          <input class="form-check-input" :name="'inlineRadioOptions_' + meta.tag + '_' + item.poll_key" :id="'inlineRadio_' + item.poll_key + '_' + index" :value="option" v-model="poll" type="radio">
          <label class="form-check-label" :for="'inlineRadio_' + item.poll_key + '_' + index">
            <span style="padding-left: 4px">{{ option }}</span>
          </label>        
        </div>
      </div>

      <div v-if="item.poll_key === '18-6'" class="btn-group" role="group" aria-label="Gender Selection">
        <div v-for="(option, index) in meta.selections[35]" :key="index" class="form-check form-check-inline btn btn-outline-dark px-3" @click="clickBtn(meta.value[0], item.poll_key)">
          <input class="form-check-input" :name="'inlineRadioOptions_' + meta.tag + '_' + item.poll_key" :id="'inlineRadio_' + item.poll_key + '_' + index" :value="option" v-model="poll" type="radio">
          <label class="form-check-label" :for="'inlineRadio_' + item.poll_key + '_' + index">
            <span style="padding-left: 4px">{{ option }}</span>
          </label>        
        </div>
      </div>

      <div v-if="item.poll_key === '18-7'" class="btn-group" role="group" aria-label="Gender Selection">
        <div v-for="(option, index) in meta.selections[36]" :key="index" class="form-check form-check-inline btn btn-outline-dark px-3" @click="clickBtn(meta.value[0], item.poll_key)">
          <input class="form-check-input" :name="'inlineRadioOptions_' + meta.tag + '_' + item.poll_key" :id="'inlineRadio_' + item.poll_key + '_' + index" :value="option" v-model="poll" type="radio">
          <label class="form-check-label" :for="'inlineRadio_' + item.poll_key + '_' + index">
            <span style="padding-left: 4px">{{ option }}</span>
          </label>        
        </div>
      </div>

      <div v-if="item.poll_key === '19'" class="btn-group" role="group" aria-label="Gender Selection">
        <div v-for="(option, index) in meta.selections[37]" :key="index" class="form-check form-check-inline btn btn-outline-dark px-3" @click="clickBtn(meta.value[0], item.poll_key)">
          <input class="form-check-input" :name="'inlineRadioOptions_' + meta.tag + '_' + item.poll_key" :id="'inlineRadio_' + item.poll_key + '_' + index" :value="option" v-model="poll" type="radio">
          <label class="form-check-label" :for="'inlineRadio_' + item.poll_key + '_' + index">
            <span style="padding-left: 4px">{{ option }}</span>
          </label>        
        </div>
      </div>

      <div v-if="item.poll_key === '20'" class="btn-group" role="group" aria-label="Gender Selection">
        <div v-for="(option, index) in meta.selections[38]" :key="index" class="form-check form-check-inline btn btn-outline-dark px-3" @click="clickBtn(meta.value[0], item.poll_key)">
          <input class="form-check-input" :name="'inlineRadioOptions_' + meta.tag + '_' + item.poll_key" :id="'inlineRadio_' + item.poll_key + '_' + index" :value="option" v-model="poll" type="radio">
          <label class="form-check-label" :for="'inlineRadio_' + item.poll_key + '_' + index">
            <span style="padding-left: 4px">{{ option }}</span>
          </label>        
        </div>
      </div>

      <div v-if="item.poll_key === '21'" class="btn-group" role="group" aria-label="Gender Selection">
        <div v-for="(option, index) in meta.selections[39]" :key="index" class="form-check form-check-inline btn btn-outline-dark px-3" @click="clickBtn(meta.value[0], item.poll_key)">
          <input class="form-check-input" :name="'inlineRadioOptions_' + meta.tag + '_' + item.poll_key" :id="'inlineRadio_' + item.poll_key + '_' + index" :value="option" v-model="poll" type="radio">
          <label class="form-check-label" :for="'inlineRadio_' + item.poll_key + '_' + index">
            <span style="padding-left: 4px">{{ option }}</span>
          </label>        
        </div>
      </div>

      <div v-if="item.poll_key === '22'" class="btn-group" role="group" aria-label="Gender Selection">
        <div v-for="(option, index) in meta.selections[40]" :key="index" class="form-check form-check-inline btn btn-outline-dark px-3" @click="clickBtn(meta.value[0], item.poll_key)">
          <input class="form-check-input" :name="'inlineRadioOptions_' + meta.tag + '_' + item.poll_key" :id="'inlineRadio_' + item.poll_key + '_' + index" :value="option" v-model="poll" type="radio">
          <label class="form-check-label" :for="'inlineRadio_' + item.poll_key + '_' + index">
            <span style="padding-left: 4px">{{ option }}</span>
          </label>        
        </div>
      </div>

      <div v-if="item.poll_key === '23'" class="btn-group" role="group" aria-label="Gender Selection">
        <div v-for="(option, index) in meta.selections[41]" :key="index" class="form-check form-check-inline btn btn-outline-dark px-3" @click="clickBtn(meta.value[0], item.poll_key)">
          <input class="form-check-input" :name="'inlineRadioOptions_' + meta.tag + '_' + item.poll_key" :id="'inlineRadio_' + item.poll_key + '_' + index" :value="option" v-model="poll" type="radio">
          <label class="form-check-label" :for="'inlineRadio_' + item.poll_key + '_' + index">
            <span style="padding-left: 4px">{{ option }}</span>
          </label>        
        </div>
      </div>

      <div v-if="item.poll_key === '24'" class="btn-group" role="group" aria-label="Gender Selection">
        <div v-for="(option, index) in meta.selections[42]" :key="index" class="form-check form-check-inline btn btn-outline-dark px-3" @click="clickBtn(meta.value[0], item.poll_key)">
          <input class="form-check-input" :name="'inlineRadioOptions_' + meta.tag + '_' + item.poll_key" :id="'inlineRadio_' + item.poll_key + '_' + index" :value="option" v-model="poll" type="radio">
          <label class="form-check-label" :for="'inlineRadio_' + item.poll_key + '_' + index">
            <span style="padding-left: 4px">{{ option }}</span>
          </label>        
        </div>
      </div>

      <div v-if="item.poll_key === '25'" class="btn-group" role="group" aria-label="Gender Selection">
        <div v-for="(option, index) in meta.selections[43]" :key="index" class="form-check form-check-inline btn btn-outline-dark px-3" @click="clickBtn(meta.value[0], item.poll_key)">
          <input class="form-check-input" :name="'inlineRadioOptions_' + meta.tag + '_' + item.poll_key" :id="'inlineRadio_' + item.poll_key + '_' + index" :value="option" v-model="poll" type="radio">
          <label class="form-check-label" :for="'inlineRadio_' + item.poll_key + '_' + index">
            <span style="padding-left: 4px">{{ option }}</span>
          </label>        
        </div>
      </div>

      <div v-if="item.poll_key === '26'" class="btn-group" role="group" aria-label="Gender Selection">
        <div v-for="(option, index) in meta.selections[44]" :key="index" class="form-check form-check-inline btn btn-outline-dark px-3" @click="clickBtn(meta.value[0], item.poll_key)">
          <input class="form-check-input" :name="'inlineRadioOptions_' + meta.tag + '_' + item.poll_key" :id="'inlineRadio_' + item.poll_key + '_' + index" :value="option" v-model="poll" type="radio">
          <label class="form-check-label" :for="'inlineRadio_' + item.poll_key + '_' + index">
            <span style="padding-left: 4px">{{ option }}</span>
          </label>        
        </div>
      </div>

      <div v-if="item.poll_key === '27'" class="btn-group" role="group" aria-label="Gender Selection">
        <div v-for="(option, index) in meta.selections[45]" :key="index" class="form-check form-check-inline btn btn-outline-dark px-3" @click="clickBtn(meta.value[0], item.poll_key)">
          <input class="form-check-input" :name="'inlineRadioOptions_' + meta.tag + '_' + item.poll_key" :id="'inlineRadio_' + item.poll_key + '_' + index" :value="option" v-model="poll" type="radio">
          <label class="form-check-label" :for="'inlineRadio_' + item.poll_key + '_' + index">
            <span style="padding-left: 4px">{{ option }}</span>
          </label>        
        </div>
      </div>

      <div v-if="item.poll_key === '28'" class="btn-group" role="group" aria-label="Gender Selection">
        <div v-for="(option, index) in meta.selections[46]" :key="index" class="form-check form-check-inline btn btn-outline-dark px-3" @click="clickBtn(meta.value[0], item.poll_key)">
          <input class="form-check-input" :name="'inlineRadioOptions_' + meta.tag + '_' + item.poll_key" :id="'inlineRadio_' + item.poll_key + '_' + index" :value="option" v-model="poll" type="radio">
          <label class="form-check-label" :for="'inlineRadio_' + item.poll_key + '_' + index">
            <span style="padding-left: 4px">{{ option }}</span>
          </label>        
        </div>
      </div>

      <div v-if="item.poll_key === '29'" class="btn-group" role="group" aria-label="Gender Selection">
        <div v-for="(option, index) in meta.selections[47]" :key="index" class="form-check form-check-inline btn btn-outline-dark px-3" @click="clickBtn(meta.value[0], item.poll_key)">
          <input class="form-check-input" :name="'inlineRadioOptions_' + meta.tag + '_' + item.poll_key" :id="'inlineRadio_' + item.poll_key + '_' + index" :value="option" v-model="poll" type="radio">
          <label class="form-check-label" :for="'inlineRadio_' + item.poll_key + '_' + index">
            <span style="padding-left: 4px">{{ option }}</span>
          </label>        
        </div>
      </div>

      <div v-if="item.poll_key === '30'" class="btn-group" role="group" aria-label="Gender Selection">
        <div v-for="(option, index) in meta.selections[48]" :key="index" class="form-check form-check-inline btn btn-outline-dark px-3" @click="clickBtn(meta.value[0], item.poll_key)">
          <input class="form-check-input" :name="'inlineRadioOptions_' + meta.tag + '_' + item.poll_key" :id="'inlineRadio_' + item.poll_key + '_' + index" :value="option" v-model="poll" type="radio">
          <label class="form-check-label" :for="'inlineRadio_' + item.poll_key + '_' + index">
            <span style="padding-left: 4px">{{ option }}</span>
          </label>        
        </div>
      </div>

      <div v-if="item.poll_key === '31'" class="btn-group" role="group" aria-label="Gender Selection">
        <div v-for="(option, index) in meta.selections[49]" :key="index" class="form-check form-check-inline btn btn-outline-dark px-3" @click="clickBtn(meta.value[0], item.poll_key)">
          <input class="form-check-input" :name="'inlineRadioOptions_' + meta.tag + '_' + item.poll_key" :id="'inlineRadio_' + item.poll_key + '_' + index" :value="option" v-model="poll" type="radio">
          <label class="form-check-label" :for="'inlineRadio_' + item.poll_key + '_' + index">
            <span style="padding-left: 4px">{{ option }}</span>
          </label>        
        </div>
      </div>

      <div v-if="item.poll_key === '32'" class="btn-group" role="group" aria-label="Gender Selection">
        <div v-for="(option, index) in meta.selections[50]" :key="index" class="form-check form-check-inline btn btn-outline-dark px-3" @click="clickBtn(meta.value[0], item.poll_key)">
          <input class="form-check-input" :name="'inlineRadioOptions_' + meta.tag + '_' + item.poll_key" :id="'inlineRadio_' + item.poll_key + '_' + index" :value="option" v-model="poll" type="radio">
          <label class="form-check-label" :for="'inlineRadio_' + item.poll_key + '_' + index">
            <span style="padding-left: 4px">{{ option }}</span>
          </label>        
        </div>
      </div>

      <div v-if="item.poll_key === '33'" class="btn-group" role="group" aria-label="Gender Selection">
        <div v-for="(option, index) in meta.selections[51]" :key="index" class="form-check form-check-inline btn btn-outline-dark px-3" @click="clickBtn(meta.value[0], item.poll_key)">
          <input class="form-check-input" :name="'inlineRadioOptions_' + meta.tag + '_' + item.poll_key" :id="'inlineRadio_' + item.poll_key + '_' + index" :value="option" v-model="poll" type="radio">
          <label class="form-check-label" :for="'inlineRadio_' + item.poll_key + '_' + index">
            <span style="padding-left: 4px">{{ option }}</span>
          </label>        
        </div>
      </div>

      <div v-if="item.poll_key === '34'" class="btn-group" role="group" aria-label="Gender Selection">
        <div v-for="(option, index) in meta.selections[52]" :key="index" class="form-check form-check-inline btn btn-outline-dark px-3" @click="clickBtn(meta.value[0], item.poll_key)">
          <input class="form-check-input" :name="'inlineRadioOptions_' + meta.tag + '_' + item.poll_key" :id="'inlineRadio_' + item.poll_key + '_' + index" :value="option" v-model="poll" type="radio">
          <label class="form-check-label" :for="'inlineRadio_' + item.poll_key + '_' + index">
            <span style="padding-left: 4px">{{ option }}</span>
          </label>        
        </div>
      </div>

      <div v-if="item.poll_key === '35'" class="form-check form-check-inline btn btn-group btn-outline-dark px-3">
        <input type="text" class="form-control" placeholder="오전 8:00 ~ 오후 1:00" aria-label="Preffer Working Time" v-model="poll">
      </div>

      <div v-if="item.poll_key === '36'" class="form-check form-check-inline btn btn-group btn-outline-dark px-3">
        <input type="text" class="form-control" placeholder="오후5:00" aria-label="Best Time" v-model="poll">
      </div>

      <div v-if="item.poll_key === '37'" class="btn-group" role="group" aria-label="Gender Selection">
        <div v-for="(option, index) in meta.selections[55]" :key="index" class="form-check form-check-inline btn btn-outline-dark px-3" @click="clickBtn(meta.value[0], item.poll_key)">
          <input class="form-check-input" :name="'inlineRadioOptions_' + meta.tag + '_' + item.poll_key" :id="'inlineRadio_' + item.poll_key + '_' + index" :value="option" v-model="poll" type="radio">
          <label class="form-check-label" :for="'inlineRadio_' + item.poll_key + '_' + index">
            <span style="padding-left: 4px">{{ option }}</span>
          </label>        
        </div>
      </div>

      





    </div>
  </div>
</template>
<script>

export default {
  name: 'PollItem5',
  components: {},
  props:{
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
  methods:{
    clickBtn(item, poll_key) {
      console.log(poll_key, item)
      this.poll = item + ''
    }
  }
}
</script>
<style scoped>
</style>
