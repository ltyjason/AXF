function check() {

    var email_color = $("#u_email_info").css('color');

    if (email_color == 'rgb(255, 0, 0)') {
        return false
    }

    var email_value = $("#u_email").val();

    if (email_value == "") {
        return false
    }

    const name_color = $("#u_name_info").css('color');

    if (name_color === 'rgb(255, 0, 0)') {
        return false
    }

    var password = $("#u_password").val();

    if (password.length < 6 | password.length > 16) {
        return false
    }

    var password_comfirl = $("#u_password_confirm").val();

    if (password_comfirl === password) {
        // md5密码加密
        $("#u_password").val(md5(password));
        return true
    }
}

$(function () {
    //用户名不能为空、不能重复
    $("#username").change(function () {
        var username = $(this).val();
        if (username.length === 0) {
            $("#u_name_info").html("用户名不能为空").css('color', 'red');
        } else {
            $.getJSON('/axf/checkuser/', {'u_name': username}, function (data) {
                if (data['status'] === '200') {
                    $("#u_name_info").html("用户名可用").css('color', 'green');
                } else {
                    $("#u_name_info").html("用户名已存在").css('color', 'red');
                }
            })
        }
    })
    // 邮箱长度不能为空、不能重复
    $("#u_email").change(function () {
        var email = $(this).val();
        console.log(email)
        if (email.length === 0) {
            $("#u_email_info").html("邮箱不能为空").css('color', 'red');
        } else {
            $.getJSON('/axf/checkemail', {'u_email': email}, function (data) {
                if (data['status'] === '200') {
                    $("#u_email_info").html("邮箱可用").css('color', 'green');
                } else {
                    $("#u_email_info").html("邮箱已经被使用").css('color', 'red');
                }
            })
        }
    })
    // 再次确认密码
    $("#u_password_confirm").change(function () {
        var password_confirm = $("#u_password_confirm").val()
        var password = $("#u_password").val()

        if (password === password_confirm) {
            $("#u_password_confirm_info").html("密码一致").css('color', 'green')
        } else {
            $("#u_password_confirm_info").html("密码不一致").css('color', 'red')
        }
    })
    // 密码不能为空、密码长度不能小于9、长于16。
    $("#u_password").change(function () {
        var password = $("#u_password").val();

        if (password.length === 0) {
            $("#u_password_info").html("密码不能为空").css('color', 'red')
        } else if (password.length < 6) {
            $("#u_password_info").html("密码太短").css('color', 'red')
        } else if (password.length > 16) {
            $("#u_password_info").html("密码太长").css('color', 'red')
        } else {
            $("#u_password_info").html(null)
        }
    })
})

function checkFileType(_this) {
    var $this = $(_this);
    var acceptType = $this.attr('accept');
    var selectedFile = $this.val();
    var fileType = selectedFile.substring(selectedFile.indexOf('.') + 1, selectedFile.length);
    var location = acceptType.indexOf(fileType);
    if (location > -1) {
        return true;
    } else {
        $this.attr('value', '');
        alert('请选择' + acceptType + '格式文件');
        return;
    }
}


