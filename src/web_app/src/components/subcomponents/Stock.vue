<template>
  <a class="stock" href="https://www.google.com">
    <div class="stock_image_container">
      <img
        v-bind:src="require('../../assets/images/logos/' + ticker + '.png')"
        alt="Finance Boi Logo"
        class="stock_image"
      />
    </div>
    <div class="stock_text_container">
      <h3 class="stock_title">{{ ticker }}</h3>
      <p class="stock_info">${{ price }}</p>
    </div>
  </a>
</template>

<script>
export default {
  name: "Stock", //this is the name of the component
  props: ["ticker", "price", "change"],
  data() {
    return {};
  }
};
</script>
