function removeProject() {
    let removeIndex = $(this).attr("data-id");
    $.ajax({
        url: "/deleteproject",
        type: "POST",
        contentType: "application/json;charset=utf-8",
        datatype: 'json',
        data: JSON.stringify({'project_id': removeIndex}),
        success: function (data) {
            alert('删除成功');
            window.location.reload(true);
        },
        error: function (xhr, type) {
            alert('删除失败')
        }
    });
}

function showProject() {
    window.location.href = "/view/?project_id=" + $(this).attr("data-id");
}

function addProject(id, name) {
    let $templateForm = $('#project-_-form');

    if (!$templateForm) {
        console.log('ERROR Cannot find template');
        return;
    }

    //Add elements
    let $newForm = $templateForm.clone();
    $newForm.attr('id', $newForm.attr('id').replace('_', id));
    $newForm.data('index', id);

    $newForm.find('div').each(function () {
        let $item = $(this);
        $item.html(name);
    });

    $newForm.find('button:first').each(function () {
        let $item = $(this);
        $item.attr('data-id', $item.attr('data-id').replace('_', id));

    });

    $newForm.find('button:last').each(function () {
        let $item = $(this);
        $item.attr('data-id', $item.attr('data-id').replace('_', id));
    });


    //Append
    $('#projects_container').append($newForm);

    //增加新的class
    $newForm.addClass('subform');
    //删除旧的class
    $newForm.removeClass('is-hidden');
    //添加查看操作
    $newForm.find('.show').click(showProject);
    //添加删除操作
    $newForm.find('.remove').click(removeProject);
}


$(function () {
    $.ajax({
        type: 'GET',
        url: '/getproject',
        data: {"object": "project"},
        dataType: 'json', // 注意：这里是指希望服务端返回json格式的数据
        success: function (projects) { // 这里的data就是json格式的数据
            projects.forEach(function (v) {
                addProject(v.project_id, v.project_name);
            });
        },
        error: function (xhr, type) {
            alert('异常')
        }
    });
});
