<template>
  <a class="watchitem" href="https://www.google.com">
    <div class="watchitem_image_container">
      <img
        v-bind:src="require('../../assets/images/logos/' + ticker + '.png')"
        alt="Finance Boi Logo"
        class="watchitem_image"
      />
    </div>
    <div class="watchitem_text_container">
      <h3 class="watchitem_title">{{ ticker }}</h3>
      <p class="watchitem_info">${{ price }}</p>
    </div>
  </a>
</template>

<script>
export default {
  name: "WatchItem", //this is the name of the component
  props: ["ticker", "price", "change"],
  data() {
    return {};
  }
};
</script>
