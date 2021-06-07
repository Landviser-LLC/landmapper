function hide_input() {
    let AB_parameter = document.getElementById("input-a-parameter");
    let k_parameter = document.getElementById("input-k-parameter");
    let input_k = document.getElementById("input-k");

    if (select.value == "2"){
        //AB_parameter.style.visibility = "hidden";
        input_k.style.visibility = "hidden";
        k_parameter.style.visibility = "hidden";
    }else{
        if(document.getElementById("k-mode-select").value == "Custom"){
          input_k.style.visibility = "visible";
        }
        AB_parameter.style.visibility = "visible";
        k_parameter.style.visibility = "visible";
    }
}

function show_input_a(){
    let input_a = document.getElementById("input-a");
    select_mn_mode.selectedIndex = select_a_mode.selectedIndex;
    if(select_a_mode.value == "Custom"){
        input_a.style.visibility = "visible";
    }else{
        input_a.style.visibility = "hidden";
    }
    show_input_mn();    
}
function show_input_mn(){
    let input_mn = document.getElementById("input-mn");
    if(select_mn_mode.value == "Custom"){
        input_mn.style.visibility = "visible";
    }else{
        input_mn.style.visibility = "hidden";
    }
}
function show_input_k(){
    let input_k = document.getElementById("input-k");
    if(select_k_mode.value == "Custom"){
        input_k.style.visibility = "visible";
    }else{
        input_k.style.visibility = "hidden";
    }
}

function show_filename(){
    let file_name = document.getElementById("file-name");
    file_name.textContent = file_form.value.substring(file_form.value.lastIndexOf('\\') + 1);
}






let select = document.getElementById("VES-type-select");
select.addEventListener("change", hide_input, false);


let select_a_mode = document.getElementById("a-mode-select");
select_a_mode.addEventListener("change", show_input_a, false);

let select_k_mode = document.getElementById("k-mode-select");
select_k_mode.addEventListener("change", show_input_k, false);

let select_mn_mode = document.getElementById("mn-mode-select");
select_mn_mode.addEventListener("change", show_input_mn, false);

let file_form = document.getElementById("uploaded-file");
file_form.addEventListener("change", show_filename, false);