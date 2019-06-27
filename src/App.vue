<template>
  <div id="app">
    <!--<h1 v-on:click="test">科技大擂台</h1>-->
    <h1 ref="h1">科技大擂台成果展示</h1>
    <v-container align-center>
    <v-layout row wrap fill-height height="160px" d-flex>
      <v-flex md1 fill-height>
      </v-flex>
      <v-flex md5 fill-height>
      <uploader id="context" :options="options" class="uploader-example" ref="context">
        <uploader-unsupport></uploader-unsupport>
        <uploader-drop>
          <p>Drop files here to upload or</p>
          <uploader-btn>select files</uploader-btn>
        </uploader-drop>
        <uploader-list></uploader-list>
      </uploader>
      </v-flex>
      <v-flex md5 fill-height>
        <v-textarea
          ref="context_text"
          label="context"
          auto-grow
          outline
          box
          disabled
          height="100px"
          class="text--darken-3 pa-0 ma-0"
        ></v-textarea>
      </v-flex>
      <v-flex md1 fill-height>
      </v-flex>
    </v-layout>

    <v-layout row wrap fill-height height="160px">
      <v-flex md1 fill-height>
      </v-flex>
      <v-flex md5 fill-height>
      <uploader id="question" :options="options" class="uploader-example" ref="question">
        <uploader-unsupport></uploader-unsupport>
        <uploader-drop>
          <p>Drop files here to upload or</p>
          <uploader-btn>select files</uploader-btn>
        </uploader-drop>
        <uploader-list></uploader-list>
      </uploader>
      </v-flex>
      <v-flex md5 fill-height>
        <v-textarea
          label="question"
          ref="question_text"
          outline
          auto-grow
          box
          disabled
          height="100px"
          class="pa-0 ma-0"
        ></v-textarea>
      </v-flex>
      <v-flex md1 fill-height>
      </v-flex>
    </v-layout>

    <v-layout row wrap fill-height height="160px">
      <v-flex md1 fill-height>
      </v-flex>
      <v-flex md5 fill-height>
      <uploader id="choices" :options="options" class="uploader-example" ref="choices">
        <uploader-unsupport></uploader-unsupport>
        <uploader-drop>
          <p>Drop files here to upload or</p>
          <uploader-btn>select files</uploader-btn>
        </uploader-drop>
        <uploader-list></uploader-list>
      </uploader>
      </v-flex>
      <v-flex md5 fill-height>
        <v-textarea
          label="choices"
          ref="choices_text"
          outline
          auto-grow
          box
          disabled
          height="100px"
          class="pa-0 ma-0"
        ></v-textarea>
      </v-flex>
      <v-flex md1 fill-height>
      </v-flex>
    </v-layout>

    <v-layout align-center fluid>
      <v-flex md2 fill-height>
      </v-flex>
      <v-flex md10 fill-height>
        <v-textarea
          label="answer"
          ref="answer_text"
          outline
          auto-grow
          box
          disabled
          height="100px"
          class="pa-0 ma-0"
        ></v-textarea>
      </v-flex>
      <v-flex md1 fill-height>
        <v-fab-transition>
        <v-btn
          dark
          fab
          top
          right
          color="pink"
          @click="get_answer"
        >
          ANS 
        </v-btn>
        </v-fab-transition>
      </v-flex>
      <v-flex md1 fill-height>
      </v-flex>
    </v-layout>
    </v-container>
    <div style="visibility: hidden">
      {{options}}
    </div>
  </div>
</template>

<script>
import axios from 'axios'
export default {
  name: 'app',
  data() {
      return {
          options: {
            // https://github.com/simple-uploader/Uploader/tree/develop/samples/Node.js
            target: '//localhost:8000/upload',
            testChunks: false,
            query: { 
                    key: this.$cookies.get("csrftoken"),
                    //fileType: this.$store.state.fileType,
                    fileType: '',
                   }
          },
          attrs: {
            accept: 'audio/*'
          },
      }
  },
  //watch: {
  //  options: {
  //    handler(newVal, oldVal) {
  //    },
  //    immediate: true,
  //    deep: true
  //  }
  //},
  methods: {
    updateFileType(setType) { 
      this.options.query.fileType = setType 
    },
    display_text(target,fa) {

      let text_display, uploader
      let dictionary = {
        context: {
          text_display:this.$refs.context_text,
          uploader:this.$refs.context.uploader
        },
        question: {
          text_display:this.$refs.question_text,
          uploader:this.$refs.question.uploader
        },
        choices: {
          text_display:this.$refs.choices_text,
          uploader:this.$refs.choices.uploader
        },
         
      }
      text_display = dictionary[target]["text_display"]
      uploader = dictionary[target]["uploader"]

      uploader.on('change', function () { 
        text_display.$refs["input-slot"].style.height = "150px"
      })
      uploader.on('fileAdded', function(file, event){
                   fa.updateFileType(target)
                 })
      uploader.on('fileSuccess', function (rootFile, file, message) { 
        message = JSON.parse(message)
        let fileType,m
        for(m of message) {
          fileType = m["fileType"] 
          text_display = dictionary[fileType]["text_display"]
          if (typeof text_display.value !== "undefined"){
            text_display.value += m["result"] 
          }
          else {
            text_display.value = m["result"] 
          }
        }
      })
    },
    get_answer(){
        const context_text = this.$refs.context_text.value
        const question_text = this.$refs.question_text.value
        const choices_text = this.$refs.choices_text.value
        let answer_text = this.$refs.answer_text

        axios
          .post('//localhost:8000/answer',{
            "context_text":context_text,
            "question_text":question_text,
            "choices_text":choices_text
          })
          .then(response => { 
              answer_text.value = response["data"]["result"]
            }
          )
    },
  },
  mounted() {
    this.display_text("context",this)
    this.display_text("question",this)
    this.display_text("choices",this)
  }
}
</script>

<style>
#app {
  font-family: 'Avenir', Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  margin-top: 60px;
}
a {
  display: inline-block;
  padding: 10px 20px;
  color: #474747;
}
a:not(:last-child) {
  border-right: 1px solid #aaaaaa;
}
a:hover {
  color: #888888;
  cursor: pointer;
  background-color: #dedede;
}
.uploader-example {
  width: 450px;
  padding: 10px;
  margin: 0px auto 0;
  font-size: 12px;
  box-shadow: 0 0 10px rgba(0, 0, 0, .4);
}
.uploader-example .uploader-btn {
  margin-right: 4px;
}
.uploader-example .uploader-list {
  max-height: 450px;
  overflow: auto;
  overflow-x: hidden;
  overflow-y: auto;
}
</style>
