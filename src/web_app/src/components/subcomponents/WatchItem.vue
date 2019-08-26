<template>
  <a class="watchitem" href="https://www.google.com">
    <div class="watchitem_image_container">
      <img
        src="https://int-financial.com/wp-content/uploads/2018/08/Stock-Market-Adults-Online-copy-17072018090131-1000x0.jpg"
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
