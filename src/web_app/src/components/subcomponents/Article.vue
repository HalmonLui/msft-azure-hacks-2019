<template>
  <a class="article" v-bind:href="article_link">
    <div class="article_image_container">
      <img
        v-bind:src="require('../../assets/images/logos/' + ticker + '.png')"
        v-bind:alt="ticker"
        class="article_image"
      />
    </div>
    <div class="article_text_container">
      <h2 class="article_title">{{ title }}</h2>
      <p class="article_description">
        {{ description }}
      </p>
      <div class="article_analysis_container">
        <div class="article_sentiment_container">
          <p>Sentiment:&nbsp;</p>
          <p v-bind:class="colorSentiment()">{{ sentiment }}</p>
        </div>
        <div class="article_change_container">
          <p v-bind:class="colorChange()">{{ change }}</p>
          <p v-bind:class="colorChange()">{{ arrow }}</p>
        </div>
      </div>
    </div>
  </a>
</template>

<script>
export default {
  name: "Article", //this is the name of the component
  props: [
    "title",
    "description",
    "article_image",
    "article_link",
    "ticker",
    "sentiment",
    "change"
  ],
  data() {
    return {
      arrow: "▶"
    };
  },
  mounted() {
    this.decodeHTML();
  },
  methods: {
    decodeHTML() {
      this.title = this.title.replace(/&#39;|&apos;/g, "'");
      this.description = this.description.replace(/&#39;|&apos;/g, "'");
    },
    colorChange() {
      if (this.change < 0) {
        this.arrow = "▼";
        return "article_change_red";
      } else {
        this.arrow = "▲";
        return "article_change_green";
      }
    },
    colorSentiment() {
      if (this.sentiment.includes("Positive")) {
        return "article_sentiment_green";
      } else if (this.sentiment.includes("Negative")) {
        return "article_sentiment_red";
      } else {
        return "article_sentiment";
      }
    }
  }
};
</script>
