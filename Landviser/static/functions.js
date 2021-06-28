function changed_select_ves_type() {
    if (select.value == "1") {
        hide_2d();
        show_1d();
    } else {
        // Hiding all not needed fields for 2d calculation 
        hide_1d();
        show_2d();
    }
}
function show_1d() {
    // Showing all needed fields for 1d calculation
    document.getElementById("input-a-parameter").style = "display: flex;";
    document.getElementById("input-mn-parameter").style = "display: flex;";
    document.getElementById("input-k-parameter").style = "display: flex;";
    document.getElementById("dat-block").style = "display:none;";
    if (document.getElementById("tables-block").style.visibility != "hidden") {
        document.getElementById("slideshow-container").style = "display: block;";
        document.getElementById("dots-container").style = "display: block;";
        document.getElementById("tables-block").style = "display: flex;";
    }
    hide_2d();
}

function hide_2d() {
    document.getElementsByClassName("layers_number_block")[0].remove();
    document.getElementsByClassName("layers-block")[0].remove();
}
function hide_1d() {
    document.getElementById("input-a-parameter").style = "display: none;";
    document.getElementById("input-mn-parameter").style = "display: none;";
    document.getElementById("input-k-parameter").style = "display: none;";
    document.getElementById("slideshow-container").style = "display: none; visibility: hidden;";
    document.getElementById("dots-container").style = "display: none; visibility: hidden;";
    document.getElementById("tables-block").style = "display: none; visibility: hidden;";
}
function show_2d() {
    
    let layers_number_block = document.createElement("div");
    let layers_number_label = document.createElement("p");
    var layers_number_input = document.createElement("input");
    let file_name_block = document.createElement("div");
    let file_name_label = document.createElement("p");
    var file_name_input = document.createElement("input");

    let parent_node = document.getElementById("input-a-parameter").parentNode;

    layers_number_label.textContent = "Input layers number: ";
    file_name_label.textContent = "Enter name of calculation: ";
    file_name_input.name = "file_name";
    file_name_input.type = "text";
    file_name_input.className = "input is-normal file_name_input";
    layers_number_input.type = "text";
    layers_number_input.className = "input is-normal input-layers-number";
    layers_number_input.name = "layers_number";
    layers_number_block.className = "layers_number_block";
    file_name_block.className = "file_name_block";
    layers_number_block.appendChild(layers_number_label);
    layers_number_block.appendChild(layers_number_input);
    file_name_block.appendChild(file_name_label);
    file_name_block.appendChild(file_name_input);
    parent_node.insertBefore(layers_number_block, document.getElementById("select-VES-type").nextSibling);
    parent_node.insertBefore(file_name_block, document.getElementsByClassName("layers_number_block")[0]);
    let layers_block = document.createElement("div");
    layers_block.className = "layers-block";

    layers_number_input.addEventListener("keydown", function (event) {
        if (event.key === "Enter") {
            event.preventDefault();
            try {
                let layers_number = parseInt(layers_number_input.value, 10);
                for (let i = 0; i < layers_number; i++) {
                    let layer = createOneLayer(i + 1);
                    layers_block.appendChild(layer);
                }
                parent_node.insertBefore(layers_block, layers_number_block.nextSibling);

            }
            catch (error) {
                alert(error.textContent);
            }

        }
    });
}


function createOneLayer(layer_number) {
    let layer_title = document.createElement("span");
    layer_title.className = "title";
    layer_title.textContent = layer_number.toString() + " layer";
    layer_title.style = "align:center;";

    let layer_with_title_block = document.createElement("div");

    let step_block = document.createElement("div");
    let step_label = document.createElement("p");
    let step_input = document.createElement("input");
    let dipole_distance_block = document.createElement("div");
    let dipole_distance_label = document.createElement("p");
    let dipole_distance_input = document.createElement("input");
    let measurment_number_block = document.createElement("div");
    let measurment_num_input = document.createElement("input");
    let measurment_num_label = document.createElement("p");
    let first_plug_block = document.createElement("div");
    let first_plug_label = document.createElement("p");
    let first_plug_input = document.createElement("input");
    let end_plug_block = document.createElement("div");
    let end_plug_label = document.createElement("p");
    let end_plug_input = document.createElement("input");
    let first_measurement_point_block = document.createElement("div");
    let first_measurement_point_label = document.createElement("p");
    let first_measurement_point_input = document.createElement("input");
    
    dipole_distance_block.className = "dipole_distance_block";
    step_block.className = "step_block";
    first_plug_block.className = "first_plug_block";
    end_plug_block.className = "end_plug_block";
    first_measurement_point_block.className = "first_measurement_point_block";

    first_measurement_point_label.textContent = "Input first point for measuremnts: ";
    step_label.textContent = "Input step: ";
    dipole_distance_label.textContent = "Input dipole distance: ";
    first_plug_label.textContent = "Input first plug number: ";
    end_plug_label.textContent = "Input end plug number: ";

    step_input.name = "step";
    dipole_distance_input.name = "dipole_distance";
    first_plug_input.name = "first_plug_number";
    end_plug_input.name = "end_plug_number";
    first_measurement_point_input.name = "first_measurement_point_input";

    layer_with_title_block.className = "layer_with_title_block";

    measurment_num_label.textContent = "Input measurements number: ";
    measurment_num_input.name = "measurment_number_input";
    measurment_num_input.className = "input is-normal measurment_number_input";
    measurment_number_block.className = "measurment_number_block";
    measurment_number_block.appendChild(measurment_num_label);
    measurment_number_block.appendChild(measurment_num_input);

    step_input.className = "input is-normal step_input";
    dipole_distance_input.className = "input is-normal dipole_distance_input";
    first_plug_input.className = "input is-normal first_plug_input";
    end_plug_input.className = "input is-normal end_plug_input";
    first_measurement_point_input.className = "input is-normal first_measurement_point_input";

    step_block.appendChild(step_label);
    step_block.appendChild(step_input);

    dipole_distance_block.appendChild(dipole_distance_label);
    dipole_distance_block.appendChild(dipole_distance_input);

    first_plug_block.appendChild(first_plug_label);
    first_plug_block.appendChild(first_plug_input);

    end_plug_block.appendChild(end_plug_label);
    end_plug_block.appendChild(end_plug_input);

    first_measurement_point_block.appendChild(first_measurement_point_label);
    first_measurement_point_block.appendChild(first_measurement_point_input);

    layer_with_title_block.appendChild(layer_title);

    layer_with_title_block.appendChild(dipole_distance_block);
    layer_with_title_block.appendChild(step_block);
    layer_with_title_block.appendChild(measurment_number_block);
    layer_with_title_block.appendChild(first_plug_block);
    layer_with_title_block.appendChild(end_plug_block);
    layer_with_title_block.appendChild(first_measurement_point_block);
    return layer_with_title_block;
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
    select_a_mode.selectedIndex = select_mn_mode.selectedIndex;

    if (select_mn_mode.value == "Custom") {
        customCalculationsGenerate();
    } else {
        let n_block = document.getElementsByClassName("input-measurment-number");
        for (let i = 0; i < n_block.length; i++) {
            n_block[i].remove();
        }
        let distance_block = document.getElementsByClassName("measurments-block");
        for (let i = 0; i < distance_block.length; i++) {
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
select.addEventListener("change", changed_select_ves_type, false);


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
    mn_label.textContent = "MN: ";
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

    measurment_number_input.addEventListener("keydown", function (event) {
        if (event.key === "Enter") {
            event.preventDefault();
            try {
                iterations_number = parseInt(measurment_number_input.value, 10);
                for (let i = 0; i < iterations_number; i++) {
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