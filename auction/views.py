from django.shortcuts import render
import random
import datetime

# Create your views here.

from django.http import HttpResponse
from .models import *


def index(request):
    return render(request, "auction/index.html")


def search(request, search_action):
    return render(request, "auction/search.html", {"search_action": search_action})


def search_result(request, search_action):
    all_shows = Show.objects.all()
    return render(request, "auction/search_result.html",
                  {"search_action": search_action, "all_shows": all_shows})


def publish_buy(request):
    showid = request.GET.get("show_id")
    show = Show.objects.filter(show_id=showid).all()[0]
    return render(request, "auction/publish_buy.html", {"show": show})


def publish_sell(request):
    showid = request.GET.get("show_id")
    show = Show.objects.filter(show_id=showid).all()[0]
    return render(request, "auction/publish_sell.html", {"show": show})


def preview_buy(request):
    pass


def decide_buy(request):
    showid = request.POST.get("show_id")
    show = Show.objects.filter(show_id=showid).all()[0]
    goods = Goods.objects.filter(show_id=showid).all()

    buy_case = BuyCase()
    buy_case.buy_case_id = random.randint(0, 2000000)
    print "buycaseid%s" % buy_case.buy_case_id
    buy_case.show = show
    buy_case.online_price = request.POST.get("begin_price")
    buy_case.offline_price = request.POST.get("last_price")
    buy_case.description = request.POST.get("buy_notes")
    buyer = Action_User.objects.filter(user_id="buyer").all()[0]
    buy_case.buyer = buyer
    if request.POST.get("lianzuo") is not None:
        buy_case.lianzuo = request.POST.get("lianzuo")
    buy_case.ticket_num = request.POST.get("ticket_num")
    buy_case.save()

    if len(goods) != 0:
        return render(request, "auction/decide_buy.html",
                      {"buy_case": buy_case, "goods": goods, "have_good": True})
    else:
        return render(request, "auction/decide_buy.html",
                      {"buy_case": buy_case, "have_good": False})


def preview_sell(request):
    pass


def decide_sell(request):
    showid = request.POST.get("show_id")
    print "showid%s" % showid
    show = Show.objects.filter(show_id=showid).all()[0]

    sell_case = SellCase()
    sell_case.sell_case_id = random.randint(0, 2000000)
    sell_case.ticket_num = request.POST.get("ticket_num")
    sell_case.online_price = request.POST.get("begin_price")
    sell_case.offline_price = request.POST.get("end_price")
    sell_case.description = request.POST.get("sell_notes")
    sell_case.separate_sell = request.POST.get("fenkaimai")
    sell_case.lianzuo = request.POST.get("lianzuo")
    sell_case.peisongfangshi = request.POST.get("pesongfangshi")
    sell_case.show =show

    # TODO
    category = Category.objects.all()[0]
    sell_case.category = category
    sell_case.online_time = datetime.datetime.now()

    # TODO user
    user = Action_User.objects.filter(user_id="seller")[0]
    sell_case.seller = user
    sell_case.save()

    good = Goods()
    good.goods_id = random.randint(0, 2000000)
    # TODO request.POST.get("play_time")
    good.offline_time = datetime.datetime.now()
    good.status = "ONSALE"
    good.org_price = request.POST.get("org_price")
    good.sit_num = request.POST.get("sit_num")
    good.online_price = request.POST.get("begin_price")
    good.offline_price = request.POST.get("end_price")
    good.sell_case = sell_case
    good.show_id = showid
    good.save()

    return render(request, "auction/decide_sell.html",
                  {"show": show, "sell_case": sell_case, "good": good})


def deal(request):
    good_id = request.POST.get("goods_id")
    good = Goods.objects.filter(goods_id=good_id).all()[0]
    buy_case_id = request.POST.get("buy_case_id")
    buy_case = BuyCase.objects.filter(buy_case_id=buy_case_id).all()[0]

    new_deal = Deal()
    new_deal.deal_id = random.randint(0, 2000000)
    new_deal.buy_case = buy_case
    new_deal.deal_price = max(good.online_price, good.offline_price)
    new_deal.save()

    good.deal_case_id = "%s" % new_deal.deal_id
    good.save()

    buyer = Action_User.objects.filter(user_id="buyer").all()[0]
    buyer.wallet -= new_deal.deal_price
    buyer.save()

    seller = Action_User.objects.filter(user_id="seller").all()[0]
    seller.wallet += new_deal.deal_price
    seller.save()

    return render(request, "auction/deal.html")


