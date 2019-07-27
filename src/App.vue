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
          v-model="context_text"
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
          ref="question_text"
          label="question"
          v-model="question_text"
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
          ref="choices_text"
          label="choices"
          v-model="choices_text"
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
          ref="answer_text"
          label="answer"
          v-model="answer_text"
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
                    fileType: this.$store.state.fileType,
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
  computed: {
    context_text() {
      return this.$store.state.context
    },
    question_text() {
      return this.$store.state.question
    },
    choices_text() {
      return this.$store.state.choices
    },
    answer_text() {
      return this.$store.state.answer
    },
  },
  methods: {
    display_text(target,dictionary) {

      let text_target, uploader
      text_target = dictionary[target]["text_target"]
      uploader = dictionary[target]["uploader"]
      const that = this

      uploader.on('change', function (e) { 
        text_target.$refs["input-slot"].style.height = "150px"
        that.options.query.fileType = e.target.parentNode.parentNode.parentNode.id
      })
      //uploader.on('fileAdded', function(file, event){
      //           })
      uploader.on('fileSuccess', function (rootFile, file, message) { 
        message = JSON.parse(message)
        let m
        for(m of message) {
          console.log("m: ",m)
          that.$store.commit({
            type: "fillText",
            tabType: m["fileType"],
            text: m["result"]
          })
        }
      })
    },
    get_answer(){

        const context_text = this.$store.state.context
        const question_text = this.$store.state.question
        const choices_text = this.$store.state.choices

        axios
          .post('//localhost:8000/answer',{
            "context_text":context_text,
            "question_text":question_text,
            "choices_text":choices_text
          })
          .then(response => { 
              this.$store.commit({
                type: "fillText",
                tabType: "answer",
                text: response["data"]["result"]
              })
            }
          )
    },
  },
  mounted() {
    const dictionary = {
      context: {
        text_target:this.$refs.context_text,
        uploader:this.$refs.context.uploader
      },
      question: {
        text_target:this.$refs.question_text,
        uploader:this.$refs.question.uploader
      },
      choices: {
        text_target:this.$refs.choices_text,
        uploader:this.$refs.choices.uploader
      },
       
    }
    this.display_text("context",dictionary)
    this.display_text("question",dictionary)
    this.display_text("choices",dictionary)
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
