<template>
  <a class="stocklist" href="https://www.google.com">
    <div class="stocklist_image_container">
      <img
        src="http://www.freedigitalphotos.net/images/previews/blue-line-chart-100101521.jpg"
        alt="Finance Boi Logo"
        class="stocklist_image"
      />
    </div>
    <div class="stocklist_text_container">
      <h4 class="stocklist_title">{{ symbol }}</h4>
      <p class="stocklist_price">${{ price }}</p>
      <p class="stocklist_change">
        {{ change }}
      </p>
    </div>
  </a>
</template>

<script>
export default {
  name: "Stocklist", //this is the name of the component
  props: ["symbol", "price", "change"],
  data() {
    return {};
  }
};
</script>
