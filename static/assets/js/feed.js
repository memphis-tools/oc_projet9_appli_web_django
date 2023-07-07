var new_date = new Date();
document.getElementById("footer_info").innerHTML = "&copy LitReview 2022-" + new_date.getFullYear();


function update_chosen_file() {
  document.getElementById("chosen_file").innerHTML = document.getElementById("btn_img").value.replace("C:\\fakepath\\", "");
}
