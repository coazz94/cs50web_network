document.addEventListener("DOMContentLoaded", function () {

    // Set all the edit views at none
    document.querySelectorAll(".edit_view").forEach(element => element.style.display="none")

    // Search for every button with the id edit
    document.querySelectorAll("#edit").forEach(element => {
        element.onclick = function (){
            // get the dataset property with the name Post (index.html) of the button that was pressed
            edit_post(this.dataset.post);}
        })

    // Find all the like buttons on the Page and add the function that is triggered by the click event
    document.querySelectorAll("#like").forEach(button =>  {
        button.onclick = function () {
            like_post(this.dataset.lpost, this.dataset.liked)
        }
    })

});

const domain = window.location.origin   

function edit_post(post_id){

    // Disable the post view
    document.querySelector(`#view_${post_id}`).style.display = "none";
    // enable the edit view for the searched post
    document.querySelector(`#edit_view_${post_id}`).style.display = "block"

    var url = domain + `/posts/${post_id}`

    //fetch(domain + `/posts/${post_id}`)
    fetch(url)
    .then(response => response.json())
    .then(post => {

        // make the form for the edit of the post and add the class
        const edit_form = document.createElement("div");
        edit_form.className = "mb-1"
        edit_form.innerHTML = ` 
        <textarea class="form-control-center" id="content" rows="5" style="width: 100%;">${post.content}</textarea>`

        // Make the save button 
        const button_save = document.createElement("button")
        button_save.className = "btn btn-info"
        button_save.innerHTML = "Save"

        // add a EventListener to the button and call the function save_post when clicked on it
        button_save.addEventListener("click", function (){
            save_post(post_id)
        })

        // add the button and the form to the modul
        document.querySelector(`#edit_view_${post_id}`).append(edit_form, button_save)

    });

}


function save_post(post_id){

    // Get the content of the changed post
    const post_content = document.querySelector("#content").value;

    var url = domain + `/posts/${post_id}`

    // Fetch put
    fetch(url, {
        method:"PUT", 
        body: JSON.stringify({
            // what to change
            "content" : post_content
        })
    });

    // Enable the post view
    document.querySelector(`#view_${post_id}`).style.display = "block";
    // Add the post content to the view without reloading
    document.querySelector(`#post_${post_id}`).innerHTML = `<p>${post_content}</p>`;    
    // Disable the edit view for the searched post
    document.querySelector(`#edit_view_${post_id}`).style.display = "none"
    // Set the inner HTML of the edit view to blank
    document.querySelector(`#edit_view_${post_id}`).innerHTML= ""

}


async function like_post(post_id, liked){

    var url = domain + `/posts/${post_id}`
    var url_l = domain + `/like/${post_id}`

    // 1 = Like , 0 = Dislike
    // Add the like to the post
    await fetch(url, {
        method:"PUT", 
        body: JSON.stringify({
            // what to change
            "likes" : liked=="0" ? -1 : 1
        })
    });

    // get actual likes
    fetch(url)
    .then(response => response.json())
    .then(post => {
        document.querySelector(`#likes_${post_id}`).innerHTML = post.likes;
    });

    // change the like status in the db
    fetch(url_l, {
        method:"POST", 
        body: JSON.stringify({
            // what to change
            "like" : liked=="0" ? 0 : 1
        })
    });


    // add a new button to the position of the current button (delete the old one)
    document.querySelector(`.lbutton_pos_${post_id}`).innerHTML = `
    <button data-lpost=${post_id} data-liked=${!liked} type="button" id="like"></button> `
    
    // get the button 
    let button = document.querySelector(`[data-lpost="${post_id}"]`)

    // add the class depending on the state of the previous button, and add a eventlistener for the next click
    button.className = liked == "0" ? "ml-2 bi i bi-hand-thumbs-up":"ml-2 bi i bi-hand-thumbs-down"
    button.addEventListener("click", function(){
        like_post(post_id, !liked)
    })

}