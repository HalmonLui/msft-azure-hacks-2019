<template>
  <a class="article" href="https://www.google.com">
    <div class="article_image_container">
      <img
        src="https://i.ytimg.com/vi/if-2M3K1tqk/maxresdefault.jpg"
        alt="Finance Boi Logo"
        class="article_image"
      />
    </div>
    <div class="article_text_container">
      <h2 class="article_title">{{ title }}</h2>
      <p class="article_info">
        {{ text }}
      </p>
    </div>
  </a>
</template>

<script>
export default {
  name: "Article", //this is the name of the component
  props: ["title", "text", "article_image"],
  data() {
    return {};
  }
};
</script>
