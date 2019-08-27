$(function () {
    $("#all_types").click(function () {
        $("#all_type_container").show();
        $(this).find("span").find("span").removeClass("glyphicon glyphicon-chevron-down").addClass("glyphicon glyphicon-chevron-up");
        $("#sort_rule_container").hide()
        $("#sort_rule").find("span").find("span").removeClass("glyphicon glyphicon-chevron-up").addClass("glyphicon glyphicon-chevron-down");
    })


    $("#all_type_container").click(function () {
        $(this).hide()
        $("#all_types").find("span").find("span").removeClass("glyphicon glyphicon-chevron-up").addClass("glyphicon glyphicon-chevron-down");
    })



    $("#sort_rule").click(function () {
        $("#sort_rule_container").show()
        $(this).find("span").find("span").removeClass("glyphicon glyphicon-chevron-down").addClass("glyphicon glyphicon-chevron-up")
        $("#all_type_container").hide()
        $("#all_types").find("span").find("span").removeClass("glyphicon glyphicon-chevron-up").addClass("glyphicon glyphicon-chevron-down");
    })

    $("#sort_rule_container").click(function () {
        $(this).hide()
        $("#sort_rule").find("span").find("span").removeClass("glyphicon glyphicon-chevron-up").addClass("glyphicon glyphicon-chevron-down");
    })

    $(".addShopping").click(function () {
        var $addShopping = $(this);
        // console.log($addShopping.prop("class"));
        // console.log($addShopping.attr("goodsid"));
        var goodsid = $addShopping.attr("goodsid")
        $.getJSON('/axf/addtocart/', {"goodsid": goodsid}, function (data) {
            if(data['status'] == '302'){
                window.open('/axf/userlogin', target='_self');
            }else if(data['status'] == '200'){
                $addShopping.prev().html(data['goods_num'])
            }
        })
    })

    $(".subShopping").click(function () {
        var $subShopping = $(this);
        // console.log($addShopping.prop("class"));
        // console.log($addShopping.attr("goodsid"));
        var goodsid = $subShopping.attr("goodsid")
        $.getJSON('/axf/subtocart/', {"goodsid": goodsid}, function (data) {
            if(data['status'] == '302'){
                window.open('/axf/userlogin', target='_self');
            }else if(data['status'] == '200'){
                $subShopping.next().html(data['goods_num'])
            }
        })
    })
})