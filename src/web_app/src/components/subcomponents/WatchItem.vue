<template>
  <a class="watchitem" href="https://www.google.com">
    <div class="watchitem_image_container">
      <img
        src="http://www.freedigitalphotos.net/images/previews/blue-line-chart-100101521.jpg"
        alt="Finance Boi Logo"
        class="watchitem_image"
      />
    </div>
    <div class="watchitem_text_container">
      <h3 class="watchitem_title">{{ symbol }}</h3>
      <p class="watchitem_info">${{ price }}</p>
    </div>
  </a>
</template>

<script>
export default {
  name: "WatchItem", //this is the name of the component
  props: ["symbol", "price", "change"],
  data() {
    return {};
  }
};
</script>
