function update_chosen_file() {
  let bt = document.getElementById("btn_img");
  bt.addEventListener("change", (event) => {
    file_path = event.target.value.split("\\");
    document.getElementById("chosen_file").innerHTML = file_path[(file_path.length-1)];
  });
};
