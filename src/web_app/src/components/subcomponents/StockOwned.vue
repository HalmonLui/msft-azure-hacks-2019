<template>
  <a class="stockowned" href="https://www.google.com">
    <div class="stockowned_image_container">
      <img
        v-bind:src="require('../../assets/images/logos/' + ticker + '.png')"
        v-bind:alt="ticker"
        v-bind:title="ticker"
        class="stockowned_image"
      />
    </div>
    <div class="stockowned_text_container">
      <p class="stockowned_title">{{ ticker }}</p>
      <p class="stockowned_price">${{ price }}</p>
      <p class="stockowned_change">
        {{ change }}
      </p>
      <p class="stockowned_change">
        {{ quantity }}
      </p>
      <p class="stockowned_change">${{ amount }}</p>
      <p class="stockowned_change">${{ profit }}</p>
    </div>
  </a>
</template>

<script>
export default {
  name: "StockOwned", //this is the name of the component
  props: ["ticker", "price", "change", "quantity", "amount", "profit"],
  data() {
    return {};
  }
};
</script>
