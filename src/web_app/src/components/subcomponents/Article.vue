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
    </div>
  </a>
</template>

<script>
export default {
  name: "Article", //this is the name of the component
  props: ["title", "description", "article_image", "article_link", "ticker"],
  data() {
    return {};
  }
};
</script>
