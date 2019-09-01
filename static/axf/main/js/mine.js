$(function () {

    $("#wait_pay").click(function () {
        console.log("123")
        window.open('/axf/orderlist/?order_type=0', target='_self')
    })
})