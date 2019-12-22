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

    $ExistForm.find('select').each(function () {
        let keyvalue = $('#' + "items-" + $(this).attr("data-id") + "-item_name").val();
        if ($('#' + "items-" + $(this).attr("data-id") + "-item_pre").text() == "无") {
            //$('#' + "items-" + $(this).attr("data-id") + "-item_pre").append("<option value='0'>无</option>");
            for (let i = 0; i < value.length; i++) {
                //new Option("text","value")方法
                let NewOption = new Option(value[i], value[i]);
                $('#' + "items-" + $(this).attr("data-id") + "-item_pre").append(NewOption);
                $('#' + "items-" + $(this).attr("data-id") + "-item_pre").selectpicker('refresh');
                $('#' + "items-" + $(this).attr("data-id") + "-item_pre").selectpicker('render');
            }
            //去除自身的option
            let optall = $('#' + "items-" + $(this).attr("data-id") + "-item_pre")[0].options;
            for (let i = 0; i < optall.length; i++) {
                if (optall[i].value == keyvalue) {
                    optall.remove(i);
                }
            }
            $('#' + "items-" + $(this).attr("data-id") + "-item_pre").selectpicker('refresh');
            $('#' + "items-" + $(this).attr("data-id") + "-item_pre").selectpicker('render');
        }
        else {
            let optionvalueorign = [];
            //获得当前select已有的option值
            let options = $('#' + "items-" + $(this).attr("data-id") + "-item_pre").find("option");
            for (let i = 0; i < options.length; i++) {
                optionvalueorign.push(options.eq(i).val());
            };

            let optionvalue = optionvalueorign.reverse().slice(0, (optionvalueorign.length - 1));

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

            for (let j = 0; j < inputvalue.length; j++) {
                //new Option("text","value")方法
                let NewOption = new Option(inputvalue[j], inputvalue[j]);
                $('#' + "items-" + $(this).attr("data-id") + "-item_pre").append(NewOption);
                $('#' + "items-" + $(this).attr("data-id") + "-item_pre").selectpicker('refresh');
                $('#' + "items-" + $(this).attr("data-id") + "-item_pre").selectpicker('render');
            }
                        let optall = $('#' + "items-" + $(this).attr("data-id") + "-item_pre")[0].options;
            for (let i = 0; i < optall.length; i++) {
                if (optall[i].value == keyvalue) {
                    optall.remove(i);
                }
            }
            $('#' + "items-" + $(this).attr("data-id") + "-item_pre").selectpicker('refresh');
            $('#' + "items-" + $(this).attr("data-id") + "-item_pre").selectpicker('render');
        }

    });
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

function FakeremoveForm() {
    alert("已提交的事项不提供删除方法哦");
}

function addEle(name, allvalue, pre_item, last_time) {
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

    $newForm.find('input:first').each(function () {
        let $item = $(this);
        $item.attr('id', $item.attr('id').replace('_', newIndex));
        $item.attr('name', $item.attr('name').replace('_', newIndex));
        $item.attr('data-id', $item.attr('data-id').replace('_', newIndex));
        $item.val(name);
    });

    $newForm.find('select').each(function () {
        let $item = $(this);
        $item.attr('id', $item.attr('id').replace('_', newIndex));
        $item.attr('name', $item.attr('name').replace('_', newIndex));
        $item.attr('data-id', $item.attr('data-id').replace('_', newIndex));
        let value = pre_item;
        console.log(value);
        if (pre_item != "无") {
            $item.append("<option value='0'>无</option>");
            for (let i = 0; i < allvalue.length; i++) {
                //new Option("text","value")方法
                let NewOption = new Option(allvalue[i], allvalue[i]);
                $item.append(NewOption);
                $item.selectpicker('refresh');
                $item.selectpicker('render');
            }
        } else {
            for (let i = 0; i < value.length; i++) {
                //new Option("text","value")方法
                let NewOption = new Option(value[i], value[i]);
                $item.append(NewOption);
                $item.selectpicker('refresh');
                $item.selectpicker('render');
            }
            for (let i = 0; i < allvalue.length; i++) {
                //new Option("text","value")方法
                let NewOption = new Option(allvalue[i], allvalue[i]);
                $item.append(NewOption);
                $item.selectpicker('refresh');
                $item.selectpicker('render');
            }
        }
        $item.val(value);
    });

    $newForm.find('.filter-option-inner-inner').text(pre_item);
    $newForm.find('.dropdown-toggle').removeClass('bs-placeholder');


    $newForm.find('input:last').each(function () {
        let $item = $(this);
        $item.attr('id', $item.attr('id').replace('_', newIndex));
        $item.attr('name', $item.attr('name').replace('_', newIndex));
        $item.attr('data-id', $item.attr('data-id').replace('_', newIndex));
        $item.val(last_time);
    });


    //Append
    $('#subforms_container').append($newForm);

    //增加新的class
    $newForm.addClass('subform');
    //删除旧的class
    $newForm.removeClass('is-hidden');
    //添加删除静态操作
    $newForm.find('.remove').click(FakeremoveForm);
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

function onSearch(searchContent) {
    let search = searchContent;
    let $ExistForm = $('.subform');
    console.log(search);
    $ExistForm.find('input:first').each(function () {
        console.log($('#' + "items-" + $(this).attr("data-id") + "-item_name").val());
        if (!($('#' + "items-" + $(this).attr("data-id") + "-item_name").val()).match(search)) {
            $(this).closest('.subform').hide();
        }
        else {
            $(this).closest('.subform').show();
        }
    });
}

function getQueryString(name) {
    let reg = new RegExp("(^|&)" + name + "=([^&]*)(&|$)", "i");
    let r = window.location.search.substr(1).match(reg);
    if (r != null) return unescape(r[2]);
    return null;
}

$(document).ready(function () {
    $(function () {
        // 获取item_json
        $.ajax({
            type: 'GET',
            url: '/getdbitem',
            data: {project_id: parseInt(getQueryString('project_id'))},
            dataType: 'json', // 注意：这里是指希望服务端返回json格式的数据
            success: function (items) { // 这里的data就是json格式的数据
                let allvalue = [];
                items.forEach(function(v){
                    allvalue.push(v.item_name);
                });
                items.forEach(function (v) {
                    let pre_item = [];
                    pre_item = v.item_pre_item.split(",");
                    addEle(v.item_name, allvalue, pre_item, v.item_last_time);
                });
                let $ExistForm = $('.subform');
                $ExistForm.find('select').each(function () {
                let keyvalue = $('#' + "items-" + $(this).attr("data-id") + "-item_name").val();
                let optall = $('#' + "items-" + $(this).attr("data-id") + "-item_pre")[0].options;
                    for (let i = 0; i < optall.length; i++) {
                        if (optall[i].value == keyvalue) {
                            optall.remove(i);
                        }
                    }
                $('#' + "items-" + $(this).attr("data-id") + "-item_pre").selectpicker('refresh');
                $('#' + "items-" + $(this).attr("data-id") + "-item_pre").selectpicker('render');
                });
            },
            error: function (xhr, type) {
                alert('Item数据获取异常')
            }
        });
    });

    $('#add').click(function () {
        if (Boolean($("#project_ST").val()) == false || Boolean($("#project_FT").val()) == false || Boolean($("#project_name").val()) == false) {
            alert("请先填充项目信息");
        } else if (($("#project_ST").val()) >= ($("#project_FT").val())) {
            alert("截止事件需晚于起始时间");
        } else if (checkEmpty()) {
            alert("该事项要填满丫")
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
                if (reName(name, id)) {
                    alert('事件名不可以重复喔');
                    $(this).val('');
                } else {
                    update();
                }
            });
            $('#' + "items-" + $(this).attr("data-id") + "-item_LT").blur(function () {
                let number = $(this).val();
                let re = /^[0-9]*[1-9][0-9]*$/;
                if(!re. test(number)){
                    alert("持续时间要填入整数喔");
                    $(this).val('');
                }
            });
        });
    });

    $('#search').click(function () {
        let searchname = $('#search_in').val();
        onSearch(searchname);
    });

    $('#ssubmit').click(function (){
        if (Boolean($("#project_ST").val()) == false || Boolean($("#project_FT").val()) == false || Boolean($("#project_name").val()) == false) {
            alert("项目信息未填满哦");
            return false;
        }
        else if(checkEmpty()) {
            alert("所有事项都要填满哦");
            return false;
        }
        else{
            document.$('#form_body').submit();
        }
    });

    $('#project_FT').click(function () {
        if (Boolean($("#project_ST").val()) == false) {
            alert("请先输入起始时间");
        }
    });


});



    // //'您输入的内容尚未保存，确定离开此页面吗？'chrome会将这句话渲染成自己的话，我也木得办法
    // $(window).bind('beforeunload',function(){return '您输入的内容尚未保存，确定离开此页面吗？';});




