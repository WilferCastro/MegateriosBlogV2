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
        <div class="mb-4 bg-light rounded p-2" id="comment_pane">
        <div class="d-flex flex-row align-items-center commented-user">
            <img class="mr-2" src="${response.image}" width="34" height="34"
                style="border-radius: 50%;">
            <h5 class="mr-2">${response.author} - </h5>
            </span><span class="mb-1 ms-2"><i class="fa-solid fa-clock-rotate-left"></i>${response.date}</span>
        </div>
        <div class="comment-text-sm mb-2">
            <p style="margin-left: 36px;">${response.comment}</p>
        </div>
        <div>
            <a class="link text-secondary" href="{% url 'nuevo_likec' value=1 pk=i.id title=article.title pka=article.id %}" style="font-size: 18px;">
                <i class="fa-solid fa-heart"></i>
                0
            </a>
            <a class="link text-secondary ms-2" href="{% url 'nuevo_dislikec' value=2 pk=i.id title=article.title pka=article.id %}" style="font-size: 18px;">
                <i class="fa-solid fa-heart-crack"></i></i>
                0
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
                $("#subcomment_panel"+response.father).prepend(`
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
            error: function(e) {
                alert(e)
            }
        });
        $('#exampleModal').modal('hide')
        return false;
    });








});