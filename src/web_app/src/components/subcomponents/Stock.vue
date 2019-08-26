<template>
  <a class="stock" href="https://www.google.com">
    <div class="stock_image_container">
      <img
        src="https://int-financial.com/wp-content/uploads/2018/08/Stock-Market-Adults-Online-copy-17072018090131-1000x0.jpg"
        alt="Finance Boi Logo"
        class="stock_image"
      />
    </div>
    <div class="stock_text_container">
      <h3 class="stock_title">{{ symbol }}</h3>
      <p class="stock_info">${{ price }}</p>
    </div>
  </a>
</template>

<script>
export default {
  name: "Stock", //this is the name of the component
  props: ["symbol", "price", "change"],
  data() {
    return {};
  }
};
</script>
