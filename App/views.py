import secrets
import uuid

from django.core.cache import cache

from django.core.mail import send_mail
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from django.template import loader
from django.urls import reverse

from App.models import MainWheel, MainNav, MainMustBuy, MainShop, MainMainShow, FoodType, Goods, UserModel, CarModel

ALL_TYPE = '0'
TOTAL_RULE = '0'
PRICE_AESC = '1'
PRICE_DESC = '2'


def home(request):
    main_wheels = MainWheel.objects.all()

    main_navs = MainNav.objects.all()

    main_mustbuys = MainMustBuy.objects.all()

    main_shops = MainShop.objects.all()

    main_shops0_1 = main_shops[0:1]

    main_shops1_3 = main_shops[1:3]

    main_shops3_7 = main_shops[3:7]

    main_shops7_11 = main_shops[7:11]

    main_shows = MainMainShow.objects.all()

    data = {
        'title': '首页',
        'main_wheels': main_wheels,
        'main_navs': main_navs,
        'main_mustbuys': main_mustbuys,
        'main_shops0_1': main_shops0_1,
        'main_shops1_3': main_shops1_3,
        'main_shops3_7': main_shops3_7,
        'main_shops7_11': main_shops7_11,
        'main_shows': main_shows,
    }

    return render(request, 'main/home.html', context=data)


def market(request):
    return redirect(reverse('axf:market_with_params', args=('104749', '0', '0')))


def market_with_params(request, categoryid, childcid, sort_rule):

    foodtypes = FoodType.objects.all()

    if childcid == ALL_TYPE:
        goods_list = Goods.objects.filter(categoryid=categoryid)
    else:
        goods_list = Goods.objects.filter(categoryid=categoryid).filter(childcid=childcid)

    if sort_rule == TOTAL_RULE:
        pass
    elif sort_rule == PRICE_AESC:
        goods_list = goods_list.order_by('price')
    elif sort_rule == PRICE_DESC:
        goods_list = goods_list.order_by('-price')
    else:
        goods_list = Goods.c_goods_num


    foodtype = FoodType.objects.get(typeid=categoryid)

    childtypenames = foodtype.childtypenames

    childtypename_list = childtypenames.split("#")

    child_type_name_list = []

    for childtypename in childtypename_list:
        child_type_name_list.append(childtypename.split(":"))

    data = {
        'title': '闪购',
        'foodtypes': foodtypes,
        'goods_list': goods_list,
        'categoryid': int(categoryid),
        'childcid': childcid,
        'child_type_name_list': child_type_name_list,
    }

    return render(request, 'main/market.html', context=data)


def cart(request):
    userid = request.session.get('user_id')

    if not userid:
        return redirect(reverse('axf:user_login'))

    carmodels = CarModel.objects.filter(c_user_id=userid)

    data = {
        'title': '购物车',
        'carmodels': carmodels,
    }

    return render(request, 'main/cart.html', context=data)


def mine(request):
    is_login = False

    user_id = request.session.get('user_id')

    data = {
        'title': '我的',
        'is_login': is_login,
    }

    if user_id:
        user = UserModel.objects.get(pk=user_id)
        is_login = True
        data['is_login'] = is_login
        data['user_icon'] = '/static/uploads/' + user.u_icon.url
        data['username'] = user.u_name

    return render(request, 'main/mine.html', context=data)


def user_register(request):
    if request.method == "GET":
        data = {
            'title': '用户注册',
        }
        return render(request, 'main/user_register.html', context=data)
    elif request.method == "POST":

        u_name = request.POST.get("u_name")
        u_email = request.POST.get("u_email")
        u_password = request.POST.get("u_password")
        u_icon = request.FILES.get("u_icon")

        user = UserModel()
        user.u_name = u_name
        user.u_email = u_email
        user.u_icon = u_icon
        user.set_password(u_password)

        user.save()

        request.session['user_id'] = user.id

        # 发送邮件
        # token = str(uuid.uuid4())
        token = secrets.token_hex(16)

        cache.set(token, user.id, timeout=60)

        send_mail_learn(u_name, u_email, token)

        return redirect(reverse('axf:mine'))


def user_logout(request):
    request.session.flush()

    return redirect(reverse('axf:mine'))


def check_user(request):
    u_name = request.GET.get("u_name")

    users = UserModel.objects.filter(u_name=u_name)

    data = {
        'msg': 'ok',
        'status': 200,
    }

    if users.exists():
        data['status'] = '901'
        data['msg'] = 'already exists'
    else:
        data['status'] = '200'
        data['msg'] = 'avaliable'
    return JsonResponse(data)


def check_email(request):
    u_email = request.GET.get("u_email")

    users = UserModel.objects.filter(u_email=u_email)

    data = {
        'msg': 'ok',
        'status': 200,
    }

    if users.exists():
        data['msg'] = 'already exists'
        data['status'] = '902'
    else:
        data['status'] = '200'
        data['msg'] = 'avaliable'

    return JsonResponse(data)


def user_login(request):
    if request.method == "GET":
        msg = request.session.get('msg')
        data = {
            'title': '用户登陆',
        }
        if msg:
            data['msg'] = msg
        return render(request, 'main/user_login.html', context=data)

    elif request.method == "POST":
        username = request.POST.get('u_name')
        upassword = request.POST.get('u_password')

        users = UserModel.objects.filter(u_name=username)

        if users.exists():
            user = users.first()
            if user.check_password(upassword):
                if user.is_active:
                    request.session['user_id'] = user.id
                    return redirect(reverse('axf:mine'))
                else:
                    # 用户未激活
                    request.session['msg'] = '用户未激活'
                    return redirect(reverse('axf:user_login'))
            else:
                request.session['msg'] = '密码错误'
                return redirect(reverse('axf:user_login'))
        else:
            request.session['msg'] = '用户名不存在'
            return redirect(reverse('axf:user_login'))


def send_mail_learn(username, receive_email, token):
    subject = "%s激活邮件" % username

    message = "hahahah"

    from_email = 'carzylty@163.com'

    recipient_list = [receive_email]

    temp = loader.get_template('main/user_active.html')

    data = {
        'username': username,
        # 'active_url': 'http://127.0.0.1:8000/axf/activeaccount/?user_id=%d' % user_id,
        'active_url': 'http://127.0.0.1:8000/axf/activeaccount/?user_token=%s' % token,
    }

    html_message = temp.render(data)

    send_mail(subject, message, from_email, recipient_list, html_message=html_message)


def active_account(request):
    user_token = request.GET.get('user_token')

    user_id = cache.get(user_token)

    if not user_id:
        return HttpResponse("激活已过期，请重新申请激活邮件")

    cache.delete(user_token)

    # user_id = request.GET.get('user_id')

    user = UserModel.objects.get(pk=user_id)

    user.is_active = True

    user.save()

    return HttpResponse('用户激活成功')


def add_to_cart(request):
    goodsid = request.GET.get('goodsid')

    userid = request.session.get('user_id')

    data = {
        'status': 200,
        'msg': "ok",
    }

    if not userid:
        data['status'] = 302
    else:
        # 先查询数据库
        car_models = CarModel.objects.filter(c_goods_id=goodsid).filter(c_user_id=userid)
        # 如果存在商品，对原有数量 + 1
        if car_models.exists():
            car_model = car_models.first()
            car_model.c_goods_num = car_model.c_goods_num + 1
            car_model.save()
        # 如果不存在， 需要新建一个对象， 来存储信息
        else:
            car_model = CarModel()
            car_model.c_goods_id = goodsid
            car_model.c_user_id = userid
            car_model.save()
        data['goods_num'] = car_model.c_goods_num

    return JsonResponse(data)


def sub_to_cart(request):
    goodsid = request.GET.get('goodsid')

    userid = request.session.get('user_id')

    data = {
        'status': 200,
        'msg': "ok",
    }

    if not userid:
        data['status'] = 302
    else:

        # 先查询数据库
        car_models = CarModel.objects.filter(c_goods_id=goodsid).filter(c_user_id=userid)
        # 如果存在商品，对原有数量 - 1
        if car_models.exists():
            car_model = car_models.first()
            if car_model.c_goods_num >= 1:
                car_model.c_goods_num -= 1
                car_model.save()
                data['goods_num'] = car_model.c_goods_num
            else:
                car_models.delete()
                data['goods_num'] = 0

    return JsonResponse(data)


def change_cart_status(request):

    cartid = request.GET.get('cartid')

    carmodel = CarModel.objects.get(pk=cartid)

    carmodel.c_goods_select = not carmodel.c_goods_select

    carmodel.save()

    data = {
        'msg': 'ok',
        'status': 200,
        'select': carmodel.c_goods_select
    }

    return JsonResponse(data)