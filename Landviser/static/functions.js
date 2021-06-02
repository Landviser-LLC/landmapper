let select = document.getElementById("VES-type-select");
let option_1 = document.getElementById("VES-type-1");
let option_2 = document.getElementById("VES-type-2");
function hide_input() {
    let AB_parameter = document.getElementById("input-a-parameter");
    let k_parameter = document.getElementById("input-k-parameter");
    if (select.value == "2"){
        console.log("Hello world!");
        //AB_parameter.style.visibility = "hidden";
        k_parameter.style.visibility = "hidden";
    }else{
        AB_parameter.style.visibility = "visible";
        k_parameter.style.visibility = "visible";
    }
}
select.addEventListener("change", hide_input, false);
