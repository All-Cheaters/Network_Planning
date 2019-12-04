// 动态更新下拉框
function update() {
    let $ExistForm = $('.subform');
    // $('#items-1-item_pre option').remove();
    //for循环获得当前页面所有input的值
    let value = [];
    //find('input:first')只获取subform下的第一个input，否则因为subform下有两个input，一个subform会循环两遍，每次value会传入两个相同的值
    //find('input:first')可以而find('input').first()不可以，后者输出所有subform的第一个，既只输出一次
    $ExistForm.find('input:first').each(function () {
        if (($('#' + "items-" + $(this).attr("data-id") + "-item_name").val()) !== "") {
            value.push($('#' + "items-" + $(this).attr("data-id") + "-item_name").val());
        }
    });

    let optionvalueorign = [];
    //获得已有的option值
    let options = $("#items-0-item_pre").find("option");
    for (let i = 0; i < options.length; i++) {
        optionvalueorign.push(options.eq(i).val());
    }
    ;

    let optionvalue = optionvalueorign.reverse().slice(0, (optionvalueorign.length - 1));
    ;

    //利用.merge，.grep，.inArray方法求数组差集
    $.arrayIntersect = function (a, b) {
        return $.merge($.grep(a, function (i) {
                return $.inArray(i, b) == -1;
            }), $.grep(b, function (i) {
                return $.inArray(i, a) == -1;
            })
        );
    };

    let inputvalue = $.arrayIntersect(optionvalue, value);

    $ExistForm.find('select').each(function () {
        if ($('#' + "items-" + $(this).attr("data-id") + "-item_pre").text() == "无") {
            //$('#' + "items-" + $(this).attr("data-id") + "-item_pre").append("<option value='0'>无</option>")
            for (let i = 0; i < value.length; i++) {
                //new Option("text","value")方法
                let NewOption = new Option(value[i], value[i]);
                $('#' + "items-" + $(this).attr("data-id") + "-item_pre").append(NewOption);
                $('#' + "items-" + $(this).attr("data-id") + "-item_pre").selectpicker('refresh');
                $('#' + "items-" + $(this).attr("data-id") + "-item_pre").selectpicker('render');
            }
        } else {
            for (let j = 0; j < inputvalue.length; j++) {
                //new Option("text","value")方法
                let NewOption = new Option(inputvalue[j], inputvalue[j]);
                $('#' + "items-" + $(this).attr("data-id") + "-item_pre").append(NewOption);
                $('#' + "items-" + $(this).attr("data-id") + "-item_pre").selectpicker('refresh');
                $('#' + "items-" + $(this).attr("data-id") + "-item_pre").selectpicker('render');
            }
        }

    });
    //var options = [], _options;

    //$ExistSelect.find('select').each(function () {
    //    $('#' + "items-" + $(this).data('id') + "-item_pre").append("<option value='Value'>无</option>");
    //    for (var i = 0; i < value.length; i++) {
    //        var option = '<option value="' + i + '">value[i]</option>';
    //        options.push(option);
    //    }
    //    _options = options.join('');
    //    $ExistSelect.find('select').each(function () {
    //        $('#' + "items-" + $(this).data('id') + "-item_pre")[0].innerHTML = _options;
    //    });
    //});
}

//更改id
function adjustIndices(removedIndex) {
    let $forms = $('.subform');

    $forms.each(function () {
        let $form = $(this);
        // $form.data('index')获取form的data-index
        let index = parseInt($form.data('index'));
        let newIndex = index - 1;

        //change ID in form inputs
        if (index < removedIndex) {
            return true;
        }
        // .attr( attributeName [, value ] )设置或返回指定属性attributeName的值。如果指定了value参数，则表示设置属性attributeName的值为value；如果没有指定value参数，则表示返回属性attributeName的值。
        $form.attr('id', $form.attr('id').replace(index, newIndex));
        $form.data('index', newIndex);

        //change IDs in form inputs
        $form.find('input:first').each(function () {
            let $item = $(this);
            $item.attr('id', $item.attr('id').replace(index, newIndex));
            $item.attr('name', $item.attr('name').replace(index, newIndex));
            $item.attr('data-id', $item.attr('data-id').replace(index, newIndex));
        });
        $form.find('select').each(function () {
            let $item = $(this);
            $item.attr('id', $item.attr('id').replace(index, newIndex));
            $item.attr('name', $item.attr('name').replace(index, newIndex));
            $item.attr('data-id', $item.attr('data-id').replace(index, newIndex));
        });
        $form.find('input:last').each(function () {
            let $item = $(this);
            $item.attr('id', $item.attr('id').replace(index, newIndex));
            $item.attr('name', $item.attr('name').replace(index, newIndex));
            $item.attr('data-id', $item.attr('data-id').replace(index, newIndex));
        });
    });
}

function removeForm() {
    //$(this).closest('.subform')从当前位置向上搜寻DOM树，直到找到第一个class为subform的元素
    let $removeForm = $(this).closest('.subform');
    let removeIndex = parseInt($removeForm.data('index'));
    let optionval = $removeForm.find('input:first').val();
    let $ExistForm = $('.subform');
    $ExistForm.find('select').each(function () {
        $('#' + "items-" + $(this).attr("data-id") + "-item_pre option").filter(function () {
            return $(this).text() == optionval
        }).remove();
        $('#' + "items-" + $(this).attr("data-id") + "-item_pre").selectpicker('refresh');
        $('#' + "items-" + $(this).attr("data-id") + "-item_pre").selectpicker('render');
    });


    $removeForm.remove();

    //update indices
    adjustIndices(removeIndex);
}


function addForm() {
    let $templateForm = $('#item-_-form');

    if (!$templateForm) {
        console.log('ERROR Cannot find template');
        return;
    }

    //Get last index
    //$('.subform').last()获得最后一个class为subForm的元素
    let $lastForm = $('.subform').last();
    let newIndex = 0;

    if ($lastForm.length > 0) {
        newIndex = parseInt($lastForm.data('index')) + 1;
    }

    //Add elements
    let $newForm = $templateForm.clone();
    $newForm.attr('id', $newForm.attr('id').replace('_', newIndex));
    $newForm.data('index', newIndex);

    $newForm.find('input').each(function () {
        let $item = $(this);
        $item.attr('id', $item.attr('id').replace('_', newIndex));
        $item.attr('name', $item.attr('name').replace('_', newIndex));
        $item.attr('data-id', $item.attr('data-id').replace('_', newIndex));
    });

    $newForm.find('select').each(function () {
        let $item = $(this);
        $item.attr('id', $item.attr('id').replace('_', newIndex));
        $item.attr('name', $item.attr('name').replace('_', newIndex));
        $item.attr('data-id', $item.attr('data-id').replace('_', newIndex));
        $item.append("<option value='0'>无</option>");
        $item.selectpicker('refresh');
        $item.selectpicker('render');
    });


    //Append
    $('#subforms_container').append($newForm);

    //增加新的class
    $newForm.addClass('subform');
    //删除旧的class
    $newForm.removeClass('is-hidden');
    //添加删除静态操作
    $newForm.find('.remove').click(removeForm);
}

function reName(name,id){
    let value = false
    let $ExistForm = $('.subform');
    $ExistForm.find('input:first').each(function () {
        if($(this).attr("data-id")!=id){
            if (($('#' + "items-" + $(this).attr("data-id") + "-item_name").val()) == name) {
            value = true;
            }
        }
    });
    return value;
}

function checkEmpty(){
    let value = false
    let $ExistForm = $('.subform');
    $ExistForm.find('input:first').each(function () {
        if (($('#' + "items-" + $(this).attr("data-id") + "-item_name").val()) == '') {
        value = true;
        }
    });
    $ExistForm.find('select').each(function () {
        if (($('#' + "items-" + $(this).attr("data-id") + "-item_pre").val()) == null) {
        value = true;
        }
    });
    $ExistForm.find('input:last').each(function () {
        if (($('#' + "items-" + $(this).attr("data-id") + "-item_LT").val()) == '') {
        value = true;
        }
    });
    return value;
}


$(document).ready(function () {

    $('#add').click(function () {
        if (Boolean($("#project_ST").val()) == false || Boolean($("#project_FT").val()) == false || Boolean($("#project_name").val()) == false) {
            alert("请先填充项目信息");
        } else if (($("#project_ST").val()) >= ($("#project_FT").val())) {
            alert("截止事件需晚于起始时间");
        } else {
            addForm();
        }

        // 动态添加元素是从哪个函数里面添加的，其触发事件也需写在此函数下，否则查找不到动态添加元素的触发事件
        let $ExistForm = $('.subform');
        $ExistForm.find('input:first').each(function () {
            $('#' + "items-" + $(this).attr("data-id") + "-item_name").blur(function () {
                //$ExistForm.find('option').remove();
                let name = $(this).val();
                let id = $(this).attr("data-id");
                if(reName(name,id)){
                    alert('事件名不可以重复喔');
                    $(this).val('');
                }
                else{
                    update();}
            });
        });
        //$ExistForm.find('select').each(function () {
        //    $('#' + "items-" + $(this).data('id') + "-item_pre").change(function () {
        //        $ExistForm.find('option').remove();
        //        update();
        //        alert('aaa');
        //    });
        //});

    });

    $('#ssubmit').click(function (){
            if(checkEmpty()) {
                alert("所有事项都要填满哦");
                return false;
            }
            else{
                document.$('#form_body').submit();
            }
    });

    $('.remove').click(function () {
        removeForm();
    });


    $('#project_FT').click(function () {
        if (Boolean($("#project_ST").val()) == false) {
            alert("请先输入起始时间");
        }
    });


    // //'您输入的内容尚未保存，确定离开此页面吗？'chrome会将这句话渲染成自己的话，我也木得办法
    // $(window).bind('beforeunload',function(){return '您输入的内容尚未保存，确定离开此页面吗？';});

});


