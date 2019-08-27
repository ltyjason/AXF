$(function () {
    $(".addShopping").click(function () {
        var $addShopping = $(this);
        // console.log($addShopping.prop("class"));
        // console.log($addShopping.attr("goodsid"));
        var goodsid = $addShopping.attr("goodsid");
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
        var $li = $subShopping.parents("li")
        console.log($li)
        // console.log($addShopping.prop("class"));
        // console.log($addShopping.attr("goodsid"));
        var goodsid = $subShopping.attr("goodsid");
        console.log(goodsid)
        $.getJSON('/axf/subtocart/', {"goodsid": goodsid}, function (data){
            if (data['status'] == '200'){
                if (data['goods_num'] == '0'){
                    $li.remove()
                }else {
                    $subShopping.next().html(data['goods_num'])
                }
            }else if (data['status'] == '302') {
                window.open('/axf/userlogin', target='_self');
            }
            })
    })

    $(".confirm").click(function () {
        var $confirm = $(this);
        var $li = $confirm.parents("li");
        var cartid = $li.attr('cartid');
        $.getJSON('/axf/changecartstatus/', {'cartid': cartid}, function (data) {
            console.log(data)
            if (data['status'] == '200'){
                if (data['select'] == 'true') {
                    $('.select').html('X')

                }else {
                    $('.select').html('')
                }
            }
        })
    })
})