$(function () {
    $("#alipay").click(function () {

        var order_no = $(this).attr('orderid');

        $.getJSON('/axf/alipaycallback/', {'order_no': order_no}, function (data) {
            if(data['status'] == 200){
                window.open('/axf/mine', target='_self');
            }
        })
    })
})