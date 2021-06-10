function hide_input() {
    let AB_parameter = document.getElementById("input-a-parameter");
    let k_parameter = document.getElementById("input-k-parameter");
    let input_k = document.getElementById("input-k");

    if (select.value == "2") {
        //AB_parameter.style.visibility = "hidden";
        input_k.style.visibility = "hidden";
        k_parameter.style.visibility = "hidden";
    } else {
        if (document.getElementById("k-mode-select").value == "Custom") {
            input_k.style.visibility = "visible";
        }
        AB_parameter.style.visibility = "visible";
        k_parameter.style.visibility = "visible";
    }
}

function show_input_a() {
    select_mn_mode.selectedIndex = select_a_mode.selectedIndex;
    if (select_a_mode.value == "Custom") {
        ; // input_a.style.visibility = "visible";
    } else {
        ;//input_a.style.visibility = "hidden";
    }
    show_input_mn();
}
function show_input_mn() {
    select_a_mode.selectedIndex= select_mn_mode.selectedIndex;
    
    if (select_mn_mode.value == "Custom") {
        customCalculationsGenerate();
    } else {
        let n_block = document.getElementsByClassName("input-measurment-number");
        for(let i = 0; i < n_block.length; i++){
            n_block[i].remove();
        }
        let distance_block = document.getElementsByClassName("measurments-block");
        for(let i = 0; i < distance_block.length; i++){
            distance_block[i].remove();
        }
       
    }
}
function show_input_k() {
    let input_k = document.getElementById("input-k");
    if (select_k_mode.value == "Custom") {
        input_k.style.visibility = "visible";
    } else {
        input_k.style.visibility = "hidden";
    }
}

function show_filename() {
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



var slideIndex = 1;
showSlides(slideIndex);

// Next/previous controls
function plusSlides(n) {
    showSlides(slideIndex += n);
}

// Thumbnail image controls
function currentSlide(n) {
    showSlides(slideIndex = n);
}

function showSlides(n) {
    let i;
    let slides = document.getElementsByClassName("mySlides");
    let dots = document.getElementsByClassName("dot");
    if (n > slides.length) { slideIndex = 1 }
    if (n < 1) { slideIndex = slides.length }
    for (i = 0; i < slides.length; i++) {
        slides[i].style.display = "none";
    }
    for (i = 0; i < dots.length; i++) {
        dots[i].className = dots[i].className.replace(" active", "");
    }
    slides[slideIndex - 1].style.display = "block";
    dots[slideIndex - 1].className += " active";
}

function createOneMeasurment(index) {
    let measurment_block = document.createElement("div");
    let ab_label = document.createElement("p");
    let mn_label = document.createElement("p");
    let ab_input = document.createElement("input");
    let mn_input = document.createElement("input");
    ab_label.textContent = index.toString() + ". AB: ";
    mn_label.textContent ="MN: ";
    ab_input.type = "text";
    mn_input.type = "text";
    ab_input.className = "input input-a";
    mn_input.className = "input input-mn";
    ab_input.name = "ab-input";
    mn_input.name = "mn-input";
    measurment_block.className = "input-measurment";
    measurment_block.appendChild(ab_label);
    measurment_block.appendChild(ab_input);
    measurment_block.appendChild(mn_label);
    measurment_block.appendChild(mn_input);
    return measurment_block;
}

function customCalculationsGenerate() {
    let k_parameter = document.getElementById('input-k-parameter');
    let n_div = document.createElement("div");
    let measurment_number_label = document.createElement("p");
    let measurment_number_input = document.createElement("input");
    let measurment_block_filling = document.createElement("div");
    let parent = k_parameter.parentNode;

    measurment_block_filling.className = "measurments-block";
    
    measurment_number_label.textContent = "Input measurements number: ";
    
    measurment_number_input.type = "text";
    measurment_number_input.className = "input is-normal input-n";
    measurment_number_input.name = "measurment-number";
    
    measurment_number_input.addEventListener("keydown", function(event){
        if(event.key === "Enter"){
            event.preventDefault();
            try {
                iterations_number = parseInt(measurment_number_input.value, 10);
                for(let i = 0; i < iterations_number; i++){
                    measurment_block_filling.appendChild(createOneMeasurment(i + 1));
                }
                parent.insertBefore(measurment_block_filling, k_parameter);            
            } catch (error) {
                alert("Incorrect values!");
            }
        }
    });

    n_div.className = "input-measurment-number";
    n_div.appendChild(measurment_number_label);
    n_div.appendChild(measurment_number_input);
    parent.insertBefore(n_div, k_parameter);
}