function addEle(name, pre_item, suc_item, last_time, earliest_start_time, earliest_finish_time, latest_start_time, latest_finish_time, free_time_difference, total_time_difference, is_key) {
    let $row = $("<tr></tr>");
    $row.append($("<td>" + name + "</td>"));
    $row.append($("<td>" + pre_item + "</td>"));
    $row.append($("<td>" + suc_item + "</td>"));
    $row.append($("<td>" + last_time + "</td>"));
    $row.append($("<td>" + earliest_start_time + "</td>"));
    $row.append($("<td>" + earliest_finish_time + "</td>"));
    $row.append($("<td>" + latest_start_time + "</td>"));
    $row.append($("<td>" + latest_finish_time + "</td>"));
    $row.append($("<td>" + free_time_difference + "</td>"));
    $row.append($("<td>" + total_time_difference + "</td>"));
    $row.append($("<td>" + is_key + "</td>"));
    $("#table_body").children("table").children("tbody").append($row);
}


function onSearch(searchContent) {
    let search = searchContent.value;
    console.log(search);
    $("table").find("tbody tr").each(function () {
            let tableTr = $(this);
            let TrValue = tableTr.children("td:first").text();
            console.log(TrValue);
            if (!TrValue.match(search)) {
                tableTr.hide();
            } else {
                tableTr.show();
            }
        }
    );
}


$(function () {
    // 获取item_json
    $.ajax({
        type: 'GET',
        url: '/getpyitem',
        data: {"object": "item"},
        dataType: 'json', // 注意：这里是指希望服务端返回json格式的数据
        success: function (items) { // 这里的data就是json格式的数据
            console.log(items);
            items.forEach(function (v) {
                addEle(v.name, v.pre_item, v.suf_item, v.last_time, v.earliest_start_time, v.earliest_finish_time, v.latest_start_time, v.latest_finish_time, v.free_time_difference, v.total_time_difference, v.is_key);
            });
            $(document).on('blur', '#search', function () {
                onSearch(this);
            });
        },
        error: function (xhr, type) {
            alert('异常')
        }
    });
});