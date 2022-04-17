window.onload = ()=>{

    //Eliminar un articulo
    document.getElementById("form_delete").addEventListener("submit",(e)=>{
        e.preventDefault()
        let form=document.getElementById("form_delete")
        let formData=new FormData(form)
        fetch("/eliminar-articulo/",{
            method: 'POST',
            body: formData,
        }).then(response => response.json())
        .then(response =>{
            document.getElementById("article"+response.article_id).remove()
            let modal = document.getElementById("exampleModal")
            const modal2 = bootstrap.Modal.getInstance(modal);
            modal2.hide();
            new Noty({
                theme: 'metroui',
                type: 'success',
                layout: 'topCenter',
                text: 'Articulo eliminado',
                timeout: 2000,
            }).show();
        }).catch(error =>{
            alert(error)
        })
    })





}