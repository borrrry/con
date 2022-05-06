from django.shortcuts import redirect, render
from .models import Board, Reply
from django.utils import timezone
from django.core.paginator import Paginator
from django.contrib import messages
# Create your views here.

def likeyc(req,bpk):
    b = Board.objects.get(id=bpk)
    b.likey.remove(req.user)
    return redirect("board:detail", bpk)

def likey(req,bpk):
    b = Board.objects.get(id=bpk)
    b.likey.add(req.user)
    return redirect("board:detail", bpk)

def index(req):
    pg = req.GET.get("page", 1)
    kw = req.GET.get("kw", "")
    cate = req.GET.get("cate", "")

    if kw:
        if cate =="sub":
            b = Board.objects.filter(subject__startswith=kw)
        elif cate =="wri":
            try:
                from acc.models import User
                u = User.objects.get(username=kw)
                b = Board.objects.filter(writer=u)
            except:
                b = Board.objects.none() # 속이 빈 레코드 설정
        elif cate == "con":
            b = Board.objects.filter(content__contains=kw)
        else:
            b = Board.objects.all()
    else:
        b = Board.objects.all()

    b = b.order_by('-pubdate') # 최신글이 제일 위로

    pag = Paginator(b, 5)
    obj = pag.get_page(pg)
    context={
        "bset":obj,
        "kw": kw,
        "cate":cate,
    }
    return render(req, "board/index.html", context)

def dreply(req,bpk, rpk):
    r = Reply.objects.get(id=rpk)
    if req.user == r.replyer:
        r.delete()
    else:
        messages.warning(req, "삭제할 수 없는 댓글입니다")
    return redirect("board:detail", bpk)

def creply(req,bpk):
    b = Board.objects.get(id=bpk)
    c = req.POST.get("com")
    Reply(board=b, replyer=req.user, comment=c).save()
    return redirect("board:detail", bpk)

def update(req,bpk):
    b = Board.objects.get(id=bpk)
    if b.writer != req.user:
        return redirect("board:index")
    elif req.method == "POST":
        s = req.POST.get("sub")
        c = req.POST.get("con")
        b.subject=s
        b.content=c
        b.save()
        return redirect("board:detail", bpk)
    context={
        "b":b
    }
    return render(req, "board/update.html", context)

def create(req):
    if req.method == "POST":
        ss = req.POST.get("ssub")
        sc = req.POST.get("scon")
        Board(subject=ss, writer=req.user, content=sc, pubdate=timezone.now()).save()
        return redirect("board:index")
    return render(req, "board/create.html")

def delete(req,bpk):
    b = Board.objects.get(id=bpk)
    if b.writer == req.user:
        b.delete()
    else: # hacking
        messages.warning(req, "삭제할 수 없는 게시글입니다")
    return redirect("board:index")

def detail(req, bpk):
    b = Board.objects.get(id=bpk)
    r = b.reply_set.all()
    context={
        "b":b,
        "rset":r
    }
    return render(req, "board/detail.html",context)
