if (window.location.hash == "#message_success") {
    document.getElementById("message_alert").style.display = "block";
    var Url = window.location.toString();
    var clean_Url = Url.substring(0,Url.indexOf("#"));
    window.history.replaceState({},document.title, clean_Url);
    setTimeout(() => {
      document.getElementById("message_alert_button").click();
     }, 5000);
  };