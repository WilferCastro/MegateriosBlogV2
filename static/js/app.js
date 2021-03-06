function edditComment(id, value) {
    document.getElementById("evalue").value = value
    let ids = document.getElementById("eid_comment").value = id
    let text = ""
    if (value == 0) {
        text = document.getElementById("commentp" + ids).innerHTML
        document.getElementById("comment_text").innerHTML = text
    } else {
        text = document.getElementById("subcommentp" + ids).innerHTML
        document.getElementById("comment_text").innerHTML = text
    }

    let myModal = new bootstrap.Modal(document.getElementById("exampleModal2"), {});
    myModal.show();
}

function deleteComment(id, value) {
    document.getElementById("dvalue").value = value
    document.getElementById("did_comment").value = id
    let myModal = new bootstrap.Modal(document.getElementById("exampleModal3"), {});
    myModal.show();
}


window.onload = () => {

    //Agregar un nuevo comentario
    document.getElementById("form_comentar").addEventListener("submit", (e) => {
        e.preventDefault();
        let formInfo = document.getElementById("form_comentar");
        let formData = new FormData(formInfo);

        fetch('/comentario/', {
            method: 'POST',
            body: formData,
        }).then(response => response.json())
            .then(response => {
                formInfo.reset();
                document.getElementById("comment_panel").insertAdjacentHTML('afterend', `<div class="mb-4 bg-light rounded p-2" id="comment_pane${response.id}">
                <div class="btn-group" style="float: right;">
                                <button type="button" class="btn" data-bs-toggle="dropdown" data-bs-display="static" aria-expanded="false">
                                    <i class="fa-solid fa-ellipsis-vertical"></i>
                                </button>
                                <ul class="dropdown-menu dropdown-menu-lg-end">
                                  <li><button onclick="edditComment('${response.id}',0)" class="dropdown-item" type="button"><i class="fa-solid fa-pen-to-square"></i> Editar comentario</button></li>
                                  <li><button onclick="deleteComment('${response.id}',0)" id="btn_deletecomment" class="dropdown-item" type="button"><i class="fa-solid fa-trash-can"></i> Eliminar comentario</button></li>
                                </ul>
                              </div>
                <div class="d-flex flex-row align-items-center commented-user">
                    <img class="mr-2" src="${response.image}" width="34" height="34"
                        style="border-radius: 50%;">
                    <h5 class="mr-2">${response.author} - </h5>
                    <small class="mb-1 ms-2 text-secondary"><i class="fa-solid fa-clock-rotate-left"></i> ${response.date} <span id="span_edited${response.id}"></span></small>
                </div>
                <div class="comment-text-sm mb-2">
                    <p id="commentp${response.id}" style="margin-left: 36px;">${response.comment}</p>
                </div>
                <div>
                <a class="link text-secondary" href="#" style="font-size: 18px;margin-left: 35px;">
                        <i class="fa-solid fa-heart"></i>
                        0
                    </a>
                    <a class="link text-secondary ms-2" href="#" style="font-size: 18px;">
                        <i class="fa-solid fa-heart-crack"></i>
                        0
                    </a>
                    <a class="link text-secondary ms-3 w3-right me-3 w3-hover-text-indigo" href="#" data-bs-toggle="modal" data-bs-target="#exampleModal" onclick="document.getElementById('sid_comment').value='${response.id}'" >
                        <i class="fa-solid fa-reply"></i> Responder
                    </a>
                </div>
            </div>
            <div id="subcomment_panel${response.id}"></div>`)
                let total = parseInt(document.getElementById("total_comments").innerText) + 1
                document.getElementById("total_comments").innerText = total
            })
            .catch((error) => {
                alert(error)
            });
    })


    //Responder un comentario
    document.getElementById("form_subcomentar").addEventListener("submit", (e) => {
        e.preventDefault()
        let form = document.getElementById("form_subcomentar");
        let formData = new FormData(form);

        formData.append('author_id', document.getElementById("author_id").value)
        formData.append('article_id', document.getElementById("article_id").value)

        fetch('/subcomentario/', {
            method: 'POST',
            body: formData,
        }).then(response => response.json())
            .then(response => {
                form.reset();
                let modal = document.getElementById("exampleModal")
                const modal2 = bootstrap.Modal.getInstance(modal);
                document.getElementById("subcomment_panel" + response.comment_id).insertAdjacentHTML('afterend', `<div class="delete${response.comment_id} ms-5 mb-4 bg-light rounded p-2" id="subcomment_pane${response.id}">
                <div class="btn-group" style="float: right;">
                    <button type="button" class="btn" data-bs-toggle="dropdown" data-bs-display="static" aria-expanded="false">
                        <i class="fa-solid fa-ellipsis-vertical"></i>
                    </button>
                    <ul class="dropdown-menu dropdown-menu-lg-end">
                    <li><button onclick="edditComment('${response.id}',1)" class="dropdown-item" type="button"><i class="fa-solid fa-pen-to-square"></i> Editar comentario</button></li>
                    <li><button onclick="deleteComment('${response.id}',1)" id="btn_deletecomment" class="dropdown-item" type="button"><i class="fa-solid fa-trash-can"></i> Eliminar comentario</button></li>
                    </ul>
                </div>
                <div class="d-flex flex-row align-items-center commented-user">
                    <img class="mr-2" src="${response.image}" width="34" height="34"
                        style="border-radius: 50%;">
                    <h5 class="mr-2">${response.author} - </h5>
                    <small class="mb-1 ms-2 text-secondary"><i class="fa-solid fa-clock-rotate-left"></i> ${response.date} <span id="sspan_edited${response.id}"></span></small>
                </div>
                <div class="comment-text-sm mb-2">
                    <p id="subcommentp${response.id}" style="margin-left: 36px;">${response.comment}</p>
                </div>
            </div>`)
                let total = parseInt(document.getElementById("total_comments").innerText) + 1
                document.getElementById("total_comments").innerText = total
                modal2.hide();
            }).catch((error) => {
                alert(error)
            });

    })


    //Editar un comentario
    document.getElementById("form_editcomment").addEventListener('submit', (e) => {
        e.preventDefault()
        let form = document.getElementById("form_editcomment")
        let formData = new FormData(form)
        formData.append('article_id', document.getElementById("article_id").value)
        let id = document.getElementById("eid_comment").value
        fetch('/editar-comentarios/', {
            method: 'POST',
            body: formData,
        }).then(response => response.json())
            .then(response => {
                if (response.action == 'comment') {
                    let text = document.getElementById("comment_text").value
                    document.getElementById("commentp" + id).innerText = text
                    document.getElementById("span_edited" + id).innerText = '| editado'

                } else {
                    let text = document.getElementById("comment_text").value
                    document.getElementById("subcommentp" + id).innerText = text
                    document.getElementById("sspan_edited" + id).innerText = '| editado'
                }
                form.reset()
                let modal = document.getElementById("exampleModal2")
                const modal2 = bootstrap.Modal.getInstance(modal)
                modal2.hide()
            }).catch(error => {
                alert(error)
            })
    })



    //Eliminar un comentario
    document.getElementById("form_deletecomment").addEventListener("submit", (e) => {
        e.preventDefault()
        let form = document.getElementById("form_deletecomment");
        let id = document.getElementById("did_comment").value;
        let formData = new FormData(form);
        formData.append('article_id', document.getElementById("article_id").value)

        fetch('/eliminar-comentarios/', {
            method: 'POST',
            body: formData,
        }).then(response => response.json())
            .then(response => {
                if (response.action == 'comment') {
                    document.getElementById("comment_pane" + id).remove()
                    let elem = document.querySelectorAll("div.delete" + id).length + 1
                    document.querySelectorAll("div.delete" + id).forEach((node) => {
                        node.remove();
                    })
                    let total = parseInt(document.getElementById("total_comments").innerText) - elem
                    document.getElementById("total_comments").innerText = total
                } else {
                    let total = parseInt(document.getElementById("total_comments").innerText) - 1
                    document.getElementById("total_comments").innerText = total
                    document.getElementById("subcomment_pane" + id).remove()
                }
                new Noty({
                    theme: 'metroui',
                    type: 'success',
                    layout: 'topRight',
                    text: 'Comentario eliminado',
                    timeout: 2000,
                }).show();
                let modal = document.getElementById("exampleModal3")
                const modal2 = bootstrap.Modal.getInstance(modal);
                modal2.hide()
            }).catch((error) => {
                alert(error)
            });

    })


    //Dar un like
    document.getElementById("btn_like").addEventListener("click", (e) => {
        let id = document.getElementById("article_id").value
        let url = `/article-nuevo-like/?value=1&id_article=${id}`

        fetch(url, {
            method: 'GET',
            headers: {},
        }).then(response => response.json())    
            .then(response => {
                if (response.like == "Like") {
                    document.getElementById("span_likes").innerText = response.likes
                    let btn_like = document.getElementById("btn_like")
                    btn_like.classList.add("heart11")
                    btn_like.classList.remove("heart1")
                } else if (response.like == "None") {
                    document.getElementById("span_likes").innerText = response.likes
                    let btn_like = document.getElementById("btn_like")
                    btn_like.classList.add("heart1");
                    btn_like.classList.remove("heart11")
                } else if (response.like == "DislikeRemove") {
                    document.getElementById("span_likes").innerText = response.likes
                    document.getElementById("span_dislikes").innerText = response.dislikes
                    let btn_like = document.getElementById("btn_like")
                    btn_like.classList.add("heart11")
                    btn_like.classList.remove("heart1")
                    let btn_dislike = document.getElementById("btn_dislike")
                    btn_dislike.classList.add("heart2")
                    btn_dislike.classList.remove("heart22")
                }
            }).catch(error => {
                alert(error)
            })
    })

    //Dar un dislike
    document.getElementById("btn_dislike").addEventListener("click", (e) => {
        let id = document.getElementById("article_id").value
        let url = `/article-nuevo-dislike/?value=1&id_article=${id}`

        fetch(url, {
            method: 'GET',
            headers: {},
        }).then(response => response.json())
            .then(response => {
                if (response.like == "Dislike") {
                    document.getElementById("span_dislikes").innerText = response.dislikes
                    let btn_like = document.getElementById("btn_dislike")
                    btn_like.classList.add("heart22")
                    btn_like.classList.remove("heart2")
                } else if (response.like == "None") {
                    document.getElementById("span_dislikes").innerText = response.dislikes
                    let btn_like = document.getElementById("btn_dislike")
                    btn_like.classList.add("heart2")
                    btn_like.classList.remove("heart22")
                } else if (response.like == "LikeRemove") {
                    document.getElementById("span_likes").innerText = response.likes
                    document.getElementById("span_dislikes").innerText = response.dislikes
                    let btn_like = document.getElementById("btn_like")
                    btn_like.classList.add("heart1")
                    btn_like.classList.remove("heart11")
                    let btn_dislike = document.getElementById("btn_dislike")
                    btn_dislike.classList.add("heart22")
                    btn_dislike.classList.remove("heart2")
                }
            }).catch(error => {
                alert(error)
            })
    })




};