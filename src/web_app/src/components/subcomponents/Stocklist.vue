<template>
  <div class="stocklist">
    <div class="stocklist_image_container">
      <img
        v-bind:src="require('../../assets/images/logos/' + ticker + '.png')"
        alt="ticker"
        class="stocklist_image"
      />
    </div>
    <div class="stocklist_text_container">
      <h4 class="stocklist_title">{{ ticker }}</h4>
      <p class="stocklist_price">${{ price }}</p>
      <p class="stocklist_change">{{ change }}</p>
    </div>
  </div>
</template>

<script>
export default {
  name: "Stocklist", //this is the name of the component
  props: ["ticker", "price", "change"],
  data() {
    return {};
  }
};
</script>
