document.addEventListener('DOMContentLoaded', function(){
    document.querySelector('#id_listingImage').addEventListener('change', preview);
    document.querySelector('#rem-img').addEventListener('click', remImg);
});


// Display image in the form before upload
function preview(event){
    let up = event.currentTarget;
    const [img] = up.files;
    console.log(img)
    
    if (img != undefined) {
        document.querySelector('#img-preview').src = URL.createObjectURL(img);
        document.querySelector('#prev-container').style.display = 'block';
    }
    else {
        document.querySelector('#prev-container').style.display = 'none';
    }
}


// Remove selected image
function remImg(event) {
    const imgInput = document.querySelector('#id_listingImage');
    imgInput.value = '';
    document.querySelector('#prev-container').style.display = 'none';
}












