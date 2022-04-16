function countChars(obj){
    let val=obj.value.length;
    document.getElementById("text_counter").innerText=val
}


window.onload = ()=> {

document.getElementById("button_filev2").addEventListener('click', function() {
    document.getElementById("id_image").click();
});

let file=document.getElementById("id_image")
let image=document.getElementById("img_avatar")

file.addEventListener("change", () => {
    const archivos = file.files;
    const primerArchivo = archivos[0];

    const objectURL = URL.createObjectURL(primerArchivo);

    image.src = objectURL;
    image=document.getElementById("img_avatar")

    document.getElementById("button_filev3").style.display="inline"
  });




  document.getElementById("button_filev3").addEventListener("click", ()=>{
    image.src = "/static/img/avatar.jpg";
    document.getElementById("button_filev3").style.display="none"
  })


  document.getElementById("form_registro").addEventListener("submit", (e)=>{
      e.preventDefault()
      let form = document.getElementById("form_registro")
      let formData = new FormData(form)
      fetch("/registrarme/",{
        method: 'POST',
        body: formData,
      }).then(response => response.json())
      .then(response =>{
          console.log(response)
        if (response.ok){
            form.reset()
            document.getElementById("btn_registrar").disabled = true
            new Noty({
                theme: 'metroui',
                type: 'success',
                layout: 'topCenter',
                text: "Cuenta creada con éxito",
                timeout: 3000,
            }).show();
            new Noty({
                theme: 'metroui',
                type: 'success',
                layout: 'topCenter',
                text: "Será redireccionado a la pagina de inicio de sesión",
                timeout: 3800,
            }).show();
            setTimeout(function(){
               window.location.href = "/accounts/login/";
            }, 5200);
            
        }else{
            if (response.password2){
                new Noty({
                    theme: 'metroui',
                    type: 'error',
                    layout: 'topCenter',
                    text: response.password2[0],
                    timeout: 5000,
                }).show();
              }if (response.username){
                new Noty({
                    theme: 'metroui',
                    type: 'error',
                    layout: 'topCenter',
                    text: response.username[0],
                    timeout: 5300,
                }).show();
              }if (response.email){
                new Noty({
                    theme: 'metroui',
                    type: 'error',
                    layout: 'topCenter',
                    text: response.email[0],
                    timeout: 5600,
                }).show();
              }
        }
          
      }).catch(error =>{
          alert(error)
      })
  })






}