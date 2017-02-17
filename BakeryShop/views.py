# -*- coding: UTF-8 -*-

from django.shortcuts import render
from django.contrib import auth
from django.http import HttpResponseRedirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.core.files.storage import FileSystemStorage
import datetime
from models import Invoice, Shop, Product, SendToShop, ProductToShop, BarCode, Revision, RevisionHasBarCode
from forms import ShopForm, ProductForm
from django.contrib.auth.models import User, Permission
from django.db.models import Q

from django import template

register = template.Library()


def home(request):
    args = {}
    args['user'] = auth.get_user(request)
    args['sendToShop'] = getSendsToShops(request)

    return render(request, 'home.html', args)

def invoices(request):
    args = {}
    args['user'] = auth.get_user(request)

    if request.method == 'POST' and request.FILES['myfile']:
        myfile = request.FILES['myfile']
        fs = FileSystemStorage()
        filename = fs.save(myfile.name, myfile)
        uploaded_file_url = fs.url(filename)

        invoice = Invoice(Photo=uploaded_file_url, DateTime = datetime.datetime.now(), User =  auth.get_user(request))
        invoice.save()

        args['uploaded_file_url'] = uploaded_file_url

    invoices_list = Invoice.objects.all()
    paginator = Paginator(invoices_list, 9)  # Show 25 contacts per page

    page = request.GET.get('page')
    try:
        invoices = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        invoices = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        invoices = paginator.page(paginator.num_pages)

    args['invoices'] = invoices

    return render(request, 'invoices.html', args)

def shops(request):

    if request.method == "POST":
        form = ShopForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.save()

    args = {}
    args['user'] = auth.get_user(request)
    args['form'] = ShopForm()
    args['shops'] = Shop.objects.all()

    return render(request, 'shops.html', args)

def editShop(request, pk):

    edit = False

    if request.method == "POST":
        form = ShopForm(request.POST)
        if form.is_valid():
            model_instance = form.save(commit=False)
            model_instance.id = pk
            model_instance.save()
            edit = True

    args = {}
    args['user'] = auth.get_user(request)
    args['form'] = ShopForm(instance = Shop.objects.get(id = pk))
    args['whatEdit'] = 'Редагування магазину'

    if not edit:
        return render(request, 'edit.html', args)
    else:
        args['shops'] = Shop.objects.all()
        return render(request, 'shops.html', args)

def products(request):

    if request.method == "POST" and request.FILES['Photo']:
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            product = form.save(commit=False)

            photo = request.FILES['Photo']
            fs = FileSystemStorage()
            filename = fs.save(photo.name, photo)
            uploaded_file_url = fs.url(filename)

            product.Photo = uploaded_file_url
            product.save()

    args = {}
    args['user'] = auth.get_user(request)
    args['form'] = ProductForm()
    args['products'] = Product.objects.all()

    return render(request, 'products.html', args)

def editProduct(request, pk):
    edit = False

    if request.method == "POST":
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            product = form.save(commit=False)

            photo = request.FILES['Photo']
            fs = FileSystemStorage()
            filename = fs.save(photo.name, photo)
            uploaded_file_url = fs.url(filename)

            product.Photo = uploaded_file_url
            product.id = pk
            product.save()
            edit = True
        else:
            product = Product.objects.get(id=pk)
            product.Title = form.data['Title']
            product.Description = form.data['Description']
            product.Price = form.data['Price']
            product.save()
            edit = True

    args = {}
    args['user'] = auth.get_user(request)
    args['form'] = ProductForm(instance=Product.objects.get(id=pk))
    args['whatEdit'] = 'Редагування продукції'

    if not edit:
        return render(request, 'edit.html', args)
    else:
        args['products'] = Product.objects.all()
        return render(request, 'products.html', args)

def vendors(request):
    args = {}
    args['user'] = auth.get_user(request)

    # perm = Permission.objects.get(codename='Продавці')
    # users = User.objects.filter(Q(groups__permissions=perm) | Q(user_permissions=perm)).distinct()

    args['users'] = User.objects.filter(groups__name='Продавці')
    return render(request, 'vendors.html', args)

def view_send_to_shop(request, pk):
    args = {}
    args['user'] = auth.get_user(request)
    sendToShop = SendToShop.objects.get(id = pk)
    args['sendToShop'] = sendToShop
    args['productToShop'] = ProductToShop.objects.filter(SendToShop_id = sendToShop)

    dictonary = {}

    for pts in args['productToShop']:
        dictonary[pts] = len(BarCode.objects.filter(ProductToShop_id = pts))

    args['productToShop'] = dictonary
    return render(request, 'showSendToShop.html', args)

def getSendsToShops(request):
    sts_list = SendToShop.objects.all().order_by('-DateTime')
    paginator = Paginator(sts_list, 10)  # Show 25 contacts per page

    page = request.GET.get('page')
    try:
        sendsToShops = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        sendsToShops = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        sendsToShops = paginator.page(paginator.num_pages)

    return sendsToShops

def getRevisions(request):
    revisions_list = Revision.objects.all().order_by('-DateTime')
    paginator = Paginator(revisions_list, 10)  # Show 25 contacts per page

    page = request.GET.get('page')
    try:
        revisions = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        revisions = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        revisions = paginator.page(paginator.num_pages)

    return revisions

@register.simple_tag()
def multiply(qty, unit_price, *args, **kwargs):
    # you would need to do any localization of the result here
    return qty * unit_price

def create_new_send(request):
    args = {}
    args['user'] = auth.get_user(request)

    if request.method != "POST":
        args['shops'] = Shop.objects.all()
        args['products'] = Product.objects.all()
        return render(request, 'createNewSend.html', args)
    else:
        shop_id = request.POST.get("shop_ch")

        sendToShop = SendToShop(User_id=args['user'], Shop_id = Shop.objects.get(id = shop_id), DateTime = datetime.datetime.now())
        sendToShop.save()

        # Get list of product and him count
        for prod in Product.objects.all():
            # By count we need to generate BarCode
            count = int(request.POST.get("count_" + str(prod.id)))

            if count == 0:
                continue

            productToShop = ProductToShop(Product_id = prod, SendToShop_id = sendToShop)
            productToShop.save()

            i = 0
            while i<count:
                # Generate BarCode here
                barCode = BarCode(ProductToShop_id = productToShop)
                barCode.save()
                i = i + 1


        args['sendToShop'] = getSendsToShops(request)
        return render(request, 'home.html', args)

def revisions(request):
    args = {}
    args['user'] = auth.get_user(request)
    args['revisions'] = getRevisions(request)

    return render(request, 'revisions.html', args)

def view_shop(request, pk):
    args = {}
    args['user'] = auth.get_user(request)

    args['shop'] = Shop.objects.get(id = pk)

    sendToShop = SendToShop.objects.filter(Shop_id=args['shop'])   # We have list of all SendToShop
    productToShop = ProductToShop.objects.filter(SendToShop_id__in = sendToShop)
    dictonary = {}

    for pst in productToShop:
        if not pst.Product_id in dictonary:
            dictonary[pst.Product_id] = 0
        dictonary[pst.Product_id] = dictonary[pst.Product_id] + len(BarCode.objects.filter(ProductToShop_id=pst, SoldOut=False))

    args['products'] = dictonary

    return render(request, 'showShopStorage.html', args)

def view_revision_info(request, pk):
    args = {}
    args['user'] = auth.get_user(request)
    args['revision'] = Revision.objects.get(id = pk)

    revHasBarOK = RevisionHasBarCode.objects.filter(Revision_id = args['revision']).filter(OK=True)
    revHasBar_OK = RevisionHasBarCode.objects.filter(Revision_id = args['revision']).filter(OK=False)

    prod = {}

    for bar in revHasBarOK:
        if not bar.BarCode.ProductToShop_id.Product_id in prod:
            prod[bar.BarCode.ProductToShop_id.Product_id] = [0, 0, []]
        prod[bar.BarCode.ProductToShop_id.Product_id][0] = prod[bar.BarCode.ProductToShop_id.Product_id][0] + 1
        prod[bar.BarCode.ProductToShop_id.Product_id][2].append(bar)

    for bar in revHasBar_OK:
        if not bar.BarCode.ProductToShop_id.Product_id in prod:
            prod[bar.BarCode.ProductToShop_id.Product_id] = [0, 0, []]
        prod[bar.BarCode.ProductToShop_id.Product_id][1] = prod[bar.BarCode.ProductToShop_id.Product_id][1] + 1
        prod[bar.BarCode.ProductToShop_id.Product_id][2].append(bar)

    args['productToShop'] = prod

    if len(revHasBarOK)>0:
        rhbc = revHasBarOK[0]
    elif len(revHasBar_OK)>0:
        rhbc = revHasBarOK[0]

    args['shop'] = rhbc.BarCode.ProductToShop_id.SendToShop_id.Shop_id

    '''
    args['productToShop'] = ProductToShop.objects.filter(SendToShop_id=sendToShop)

    dictonary = {}

    for pts in args['productToShop']:
        dictonary[pts] = len(BarCode.objects.filter(ProductToShop_id=pts))

    args['productToShop'] = dictonary
    '''
    return render(request, 'showRevision.html', args)



# Method commit revision
def commitRevision():
    # Get list all production in magazine, not SoldOut
    # Get List from magazine
    # All not SoldOut and FromMagazine OK
    # other not OK

    user_id = 1
    id_shop = 4
    bc_from_revision = [7895, 7896, 7897, 7898, 7899, 7900, 7901, 7902, 7903,
                        7904, 7905, 7906, 7907, 7908, 7909, 7910, 7911, 7912,
                        7913, 7914, 7915, 7916, 7917, 7918, 7919, 7920, 7921,
                        7922, 7923, 7924, 7925, 7926, 7927, 7928, 7929, 7930,
                        7931, 7932, 7933, 7934, 7935, 8516, 8517, 8518, 8519,
                        8520, 8521, 8522, 8523, 8524, 8525, 8526, 8527, 8528,
                        8529, 8530, 8531, 8532, 8533, 8534, 8535, 8536, 8537,
                        8538, 8539, 8540, 8541, 8542, 8543, 8544, 8545, 8546,
                        8547, 8548, 8549, 8550, 8551, 8552, 8553, 8554, 8555,
                        8556, 8557]

    send_to_shops = SendToShop.objects.filter(Shop_id = Shop.objects.get(id = id_shop))
    productToShop = ProductToShop.objects.filter(SendToShop_id__in=send_to_shops)
    bar_codes = BarCode.objects.filter(ProductToShop_id__in=productToShop, SoldOut=False)

    revision = Revision(DateTime = datetime.datetime.now(),User_id = User.objects.get(id = user_id))
    revision.save()

    for bar_code in bar_codes:
        if bar_code.id in bc_from_revision:
            revisionHasBarCode = RevisionHasBarCode(Revision_id=revision, BarCode=bar_code, OK=True)
        else:
            revisionHasBarCode = RevisionHasBarCode(Revision_id=revision, BarCode=bar_code, OK=False)

        revisionHasBarCode.save()

ok = False
if ok:
    commitRevision()