<template>
  <div class="footer">
    <div class="footer_company_info">
      <router-link class="navbar_link" id="navbar_logo" to="/"
        ><img
          class="footer_logo"
          src="../assets/images/logo.png"
          alt="Finance Boi Logo"
          title="Finance Boi"
      /></router-link>
      <p class="footer_copyright">
        Copyright &copy; {{ new Date().getFullYear() }} FinanceBoi, Inc. All
        rights reserved.
      </p>
      <p class="footer_text">
        By using this site you agree to the
        <router-link to="/tos">Terms of Service</router-link>,
        <router-link to="/privacypolicy">Privacy Policy</router-link>, and
        <router-link to="/cookiepolicy">Cookie Policy</router-link>.
      </p>
      <a href="https://github.com/HalmonLui/msft-azure-hacks-2019"
        ><img
          class="footer_media"
          src="../assets/images/icons/github.svg"
          alt="Github"
          title="Github"
      /></a>
      <a
        href="mailto: luih@wit.edu,brianhe@bu.edu,nchen357@bu.edu,sonamg@bu.edu"
        ><img
          class="footer_media"
          src="../assets/images/icons/email.svg"
          alt="Email"
          title="Email"
      /></a>
    </div>
  </div>
</template>
