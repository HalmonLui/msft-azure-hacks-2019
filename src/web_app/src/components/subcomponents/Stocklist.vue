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
      <div class="stocklist_change_container">
        <p v-bind:class="colorChange()">{{ change }}%</p>
        <p v-bind:class="colorChange()">{{ arrow }}</p>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: "Stocklist", //this is the name of the component
  props: ["ticker", "price", "change"],
  data() {
    return {
      arrow: null
    };
  },
  methods: {
    colorChange() {
      if (this.change < 0) {
        this.arrow = "▼";
        return "stocklist_change_red";
      } else if (this.change == 0) {
        this.arrow = "▶";
        return "stocklist_change_green";
      } else {
        this.arrow = "▲";
        return "stocklist_change_green";
      }
    }
  }
};
</script>
