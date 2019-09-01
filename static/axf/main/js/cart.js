$(function () {
    $(".addShopping").click(function () {
        var $addShopping = $(this);
        // console.log($addShopping.prop("class"));
        // console.log($addShopping.attr("goodsid"));
        var goodsid = $addShopping.attr("goodsid");
        $.getJSON('/axf/addtocart/', {"goodsid": goodsid}, function (data) {
            if (data['status'] == '302') {
                window.open('/axf/userlogin', target = '_self');
            } else if (data['status'] == '200') {
                $addShopping.prev().html(data['goods_num'])
                $("#total_price").html(data['total_price']);
            }

        })
    })

    $(".subShopping").click(function () {
        var $subShopping = $(this);
        var $li = $subShopping.parents("li")
        // console.log($addShopping.prop("class"));
        // console.log($addShopping.attr("goodsid"));
        var goodsid = $subShopping.attr("goodsid");
        $.getJSON('/axf/subtocart/', {"goodsid": goodsid}, function (data) {
            if (data['status'] == '200') {
                if (data['goods_num'] == '0') {
                    $li.remove()
                } else {
                    $subShopping.next().html(data['goods_num'])
                }
                $("#total_price").html(data['total_price']);
            } else if (data['status'] == '302') {
                window.open('/axf/userlogin', target = '_self');
            }
        })
    })

    $(".confirm").click(function () {
        var $confirm = $(this);
        var $li = $confirm.parents("li");
        var cartid = $li.attr('cartid');
        $.getJSON('/axf/changecartstatus/', {'cartid': cartid}, function (data) {
            if (data['status'] == '200') {
                if (data['select']) {
                    // $confirm.find('span').find('span').html('X')
                    $confirm.children().children('.selsect').html('✔️')
                    if (data['is_all_select']) {
                        $('.all_select').find('span').find('span').html('✔️')
                    }
                } else {
                    // $confirm.find('span').find('span').html('')
                    $confirm.children().children('.selsect').html('')
                    $('.all_select').find('span').find('span').html('️')
                }
                $("#total_price").html(data['total_price']);
            }
        })
    })

    $(".all_select").click(function () {

        selects = [];

        unselects = [];

        $(".confirm").each(function () {
            var $confirm = $(this);
            if ($confirm.find('.selsect').html() != '✔️') {
                unselects.push($confirm.parents('li').attr('cartid'));
            } else {
                selects.push($confirm.parents('li').attr('cartid'));
            }
        })
        // console.log(unselects)
        // console.log(selects)



        if(unselects.length > 0){
        //    将未选中的发送给服务器   使用#号连接每一个元素
            $.getJSON('/axf/changecartsstatus/', {'carts': unselects.join("#"), 'select': true}, function (data) {
                // console.log(data)
                if (data['status'] == '200'){
                    $('.all_select > span > span').html('✔️');
                    $('.selsect').html('✔️');
                    $("#total_price").html(data['total_price']);
                    // console.log(unselects)
                }
            })
        }else {
            $.getJSON('/axf/changecartsstatus/', {'carts': selects.join("#"), 'select': false}, function (data) {
                if (data['status'] == '200'){
                    $('.all_select > span > span').html('');
                    $('.selsect').html('');
                    $("#total_price").html(data['total_price']);
                }
            })
        }

    })

    $("#make_order").click(function () {

        var selects = [];

        $(".selsect").each(function () {
            if ($(this).html() == '✔️') {
                selects.push($(this).parents('li').attr('cartid'));
            }
        })
        // console.log(selects)

        if (selects.length == 0){
            alert("请选择商品")
            return
        } else {
            $.getJSON('/axf/makeorder/', {'carts': selects.join('#')}, function (data) {
                console.log(data);

                if (data['status'] == '200'){
                    window.open('/axf/orderdetail/?orderid=' + data['order'], target='_self')
                }
            })
        }
    })
})