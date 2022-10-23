document.addEventListener("DOMContentLoaded", function () {

    // Set all the edit views at none
    document.querySelectorAll(".edit_view").forEach(element => element.style.display="none")

    // Search for every button with the id edit
    document.querySelectorAll("#edit").forEach(element => {
        element.onclick = function (){
            // get the dataset property with the name Post (index.html) of the button that was pressed
            edit_post(this.dataset.post);}
        })

});


function edit_post(post_id){

    // Disable the input field
    document.querySelector("#post_input").style.display = "none";
    // Disable the post view
    document.querySelector(`#view_${post_id}`).style.display = "none";
    // enable the edit view for the searched post
    document.querySelector(`#edit_view_${post_id}`).style.display = "block"


    // Get the content of the post
    fetch(`posts/${post_id}`)
    .then(response => response.json())
    .then(post => {

        // make the form for the edit of the post and add the class
        const edit_form = document.createElement("div");
        edit_form.className = "mb-1"
        edit_form.innerHTML = ` 
        <textarea class="form-control-center" id="content" rows="5" style="width: 100%;"></textarea>`

        // Make the save button 
        const button_save = document.createElement("button")
        button_save.className = "btn btn-info"
        button_save.innerHTML = "Save"
        // add a EventListener to the button and call the function save_post when clicked on it
        button_save.addEventListener("click", function (){
        save_post(post_id)

        })


        document.querySelector(`#edit_view_${post_id}`).append(edit_form, button_save)

        document.querySelector("#content").value = post.content;
    });







}


function save_post(post_id){


    // Get the content of the changed post
    const post_content = document.querySelector("#content").value

 

    console.log(post_content)

}



// Es dürfen keine anderen Posts editieret werden die noch auf der Siete sind
// Disable die buttons, oder disable die anderen Posts
// Es darf nur der Post von dem User editiet werden (vorne in python glaube ich )

