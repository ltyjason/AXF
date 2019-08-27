function password_security() {

    var $password = $("#u_password")

    var password = $password.val()

    $password.val(md5(password))

    return true
}