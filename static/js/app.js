function edditComment(id, value) {
    $("#evalue").val(value)
    $("#eid_comment").val(id)
    $("#comment_text").text($("#commentp" + id).text());
    $("#exampleModal2").modal("show");
}

function deleteComment(id, value) {
    console.log(value)
    $("#dvalue").val(value)
    $("#did_comment").val(id)
    $("#exampleModal3").modal("show");
}

function register(){
    alert("registrate hombre")
}

$(document).ready(function () {

    $("form#form_comentar").submit(function () {
        $.ajax({
            url: '/comentario/',
            data: {
                'article': $('#article').val(),
                'author': $('#author').val(),
                'comment': $('#comment').val(),
            },
            dataType: 'json',
            success: function (response) {
                $("#comment_panel").prepend(`
        <div class="mb-4 bg-light rounded p-2" id="comment_pane${response.id}">
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
            </span><span class="mb-1 ms-2"><i class="fa-solid fa-clock-rotate-left"></i>${response.date}</span>
        </div>
        <div class="comment-text-sm mb-2">
            <p id="commentp${response.id}" style="margin-left: 36px;">${response.comment}</p>
        </div>
        <div>
            <a class="link text-secondary" href="#" style="font-size: 18px;">
                <i class="fa-solid fa-heart"></i>
                0 Me gusta
            </a>
            <a class="link text-secondary ms-2" href="#" style="font-size: 18px;">
                <i class="fa-solid fa-heart-crack"></i>
                0 No me gusta |
            </a>
            <a class="link text-secondary ms-3" href="#" data-bs-toggle="modal" data-bs-target="#exampleModal" onclick="document.getElementById('sid_comment').value='${response.id}'" >Responder a ${response.author}</a>
        </div>
    </div>
    <div id="subcomment_panel${response.id}"></div>
          `);
            }
        });

        $('form#form_comentar').trigger("reset");
        return false;

    });


    $("#btn_ecomment").click(function () {
        let id = $("#eid_comment").val()
        let value = $("#evalue").val()
        $.ajax({
            url: '/edit-comments/',
            data: {
                'value': value,
                'id_comment': id,
                'article': $('#article').val(),
                'author': $('#author').val(),
                'comment': $("#comment_text").val(),
            },
            dataType: 'json',
            success: function (response) {
                if (response.action == 'comment') {
                    $("#commentp" + id).text($("#comment_text").val());
                    $('#form_comments').trigger("reset");
                } else {
                    alert("vamos a eliminar")
                }
            }
        });
        $("#exampleModal2").modal("hide");
        return false;
    });


    $("#btn_dcomment").click(function () {
        let id = $("#did_comment").val()
        let value = $("#dvalue").val()
        $.ajax({
            url: '/delete-comments/',
            data: {
                'value': value,
                'id_comment': id,
                'article': $('#article').val(),
                'author': $('#author').val(),
            },
            dataType: 'json',
            success: function (response) {
                if (response.action == 'comment') {
                    $(".delete" + id).remove();
                    $("#comment_pane" + id).remove();
                } else {
                    alert("vamos a eliminar")
                }
            }
        });
        $("#exampleModal3").modal("hide");
        return false;
    });


    $("form#form_subcomentar").submit(function () {
        $.ajax({
            url: '/subcomentario/',
            data: {
                'article': $('#sarticle').val(),
                'author': $('#sauthor').val(),
                'father': $('#sid_comment').val(),
                'comment': $('#subcomment').val(),
            },
            dataType: 'json',
            success: function (response) {
                $("#subcomment_panel" + response.father).prepend(`
        <div class="ms-5 mb-4 bg-light rounded p-2" id="subcomment_panel">
        <div class="d-flex flex-row align-items-center commented-user">
            <img class="mr-2" src="${response.image}" width="34" height="34"
                style="border-radius: 50%;">
            <h5 class="mr-2">${response.author} - </h5>
            </span><span class="mb-1 ms-2"><i class="fa-solid fa-clock-rotate-left"></i>${response.date}</span>
        </div>
        <div class="comment-text-sm mb-2">
            <p style="margin-left: 36px;">${response.comment}</p>
        </div>
    </div>
          `);
            }
        });
        $('#exampleModal').modal('hide')
        $('form#form_subcomentar').trigger("reset");
        return false;

    });


    $("form#form_delete").submit(function () {
        $.ajax({
            url: '/eliminar-articulo/',
            data: {
                'id_article': $('#id_article').val(),
            },
            dataType: 'json',
            success: function (response) {
                $("#article" + response.article_id).remove();
                new Noty({
                    theme: 'metroui',
                    type: 'success',
                    layout: 'topCenter',
                    text: 'Articulo eliminado',
                    timeout: 2000,
                }).show();
            },
            error: function (e) {
                alert(e)
            }
        });
        $('#exampleModal').modal('hide')
        return false;
    });


    $("#btn_like").click(function () {
        $.ajax({
            url: '/article-nuevo-like/',
            data: {
                'id_article': $('#article').val(),
                'value': 1,
            },
            dataType: 'json',
            success: function (response) {
                if (response.like == "Like") {
                    let ht = `<i class="fa-solid fa-heart"></i> ${response.likes} Me gusta`;
                    $("#btn_like").html(ht);
                    $("#btn_like").removeClass("btn-outline-primary").addClass("btn-primary");
                } else if (response.like == "None") {
                    let ht = `<i class="fa-solid fa-heart"></i> ${response.likes} Me gusta`;
                    $("#btn_like").html(ht);
                    $("#btn_like").removeClass("btn-primary").addClass("btn-outline-primary");
                } else if (response.like == "DislikeRemove") {
                    let ht = `<i class="fa-solid fa-heart"></i> ${response.likes} Me gusta`;
                    let ht2 = `<i class="fa-solid fa-heart"></i> ${response.dislikes} No me gusta`;
                    $("#btn_like").html(ht);
                    $("#btn_dislike").html(ht2);
                    $("#btn_dislike").removeClass("btn-danger").addClass("btn-outline-danger");
                    $("#btn_like").removeClass("btn-outline-primary").addClass("btn-primary");
                }
            },
            error: function (e) {
                alert(e)
            }
        });
        return false;
    });


    $("#btn_dislike").click(function () {
        $.ajax({
            url: '/article-nuevo-dislike/',
            data: {
                'id_article': $('#article').val(),
                'value': 1,
            },
            dataType: 'json',
            success: function (response) {
                if (response.like == "Dislike") {
                    let ht = `<i class="fa-solid fa-heart"></i> ${response.dislikes} No me gusta`;
                    $("#btn_dislike").html(ht);
                    $("#btn_dislike").removeClass("btn-outline-danger").addClass("btn-danger");
                } else if (response.like == "None") {
                    let ht = `<i class="fa-solid fa-heart"></i> ${response.dislikes} No me gusta`;
                    $("#btn_dislike").html(ht);
                    $("#btn_dislike").removeClass("btn-danger").addClass("btn-outline-danger");
                } else if (response.like == "LikeRemove") {
                    let ht = `<i class="fa-solid fa-heart"></i> ${response.likes} Me gusta`;
                    let ht2 = `<i class="fa-solid fa-heart"></i> ${response.dislikes} No me gusta`;
                    $("#btn_like").html(ht);
                    $("#btn_dislike").html(ht2);
                    $("#btn_dislike").removeClass("btn-outline-danger").addClass("btn-danger");
                    $("#btn_like").removeClass("btn-primary").addClass("btn-outline-primary");
                }
            },
            error: function (e) {
                alert(e)
            }
        });
        return false;
    });





});