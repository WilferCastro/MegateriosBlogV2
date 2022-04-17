let value = 0
function showPass() {
  if (value == 0) {
    document.getElementById("password").type = "text"
    let icon = document.getElementById("icon_eye")
    icon.classList.remove("fa-eye")
    icon.classList.add("fa-eye-slash")
    value = 1
  } else {
    document.getElementById("password").type = "password"
    let icon = document.getElementById("icon_eye")
    icon.classList.remove("fa-eye-slash")
    icon.classList.add("fa-eye")
    value = 0
  }
}


window.onload=()=>{

    document.getElementById("form_login").addEventListener('submit', (e) => {
        e.preventDefault()
        let form = document.getElementById("form_login")
        let formData = new FormData(form)
    
        fetch('/accounts/login/', {
          method: 'POST',
          body: formData,
        }).then(response => response.json())
          .then(response => {
              if (response.ok){
                window.location.href = "/";
              }else if(response.error){
                new Noty({
                    theme: 'metroui',
                    type: 'error',
                    layout: 'topCenter',
                    text: response.error,
                    timeout: 3800,
                  }).show();
              }
          }).catch(error => {
            alert(error)
          })
      })




}