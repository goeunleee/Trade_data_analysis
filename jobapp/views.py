from django.shortcuts import render
from .models import Job
from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from django.core.paginator import Paginator
# Create your views here.

def job(request):
    job_all = Job.objects.all().order_by("-id") # 쿼리셋, 객체목록 가져오기
    # blog_all = blog.all()
    paginator =Paginator(job_all, 3) #3개씩 쪼개서 페이지에 보여준다.
    # 8000/detail/?page='3' 이런식으로 넘어간다. 그래서 현재 페이지가 몇번인지 알아야한다
    page=request.GET.get('page') #페이지는 항상 GET방식으로 받는다 이러면 현재 페이지가 몇번인지 알수있다
    posts= paginator.get_page(page) #가지고 온 페이지를 posts에 저장한다
    return render(request, "job.html", {"job": posts}) #page에 관련된 객체 넘겨줌


def detail(request, job_id):
    job_all = Job.objects.all().order_by("-id")
    count = Job.objects.count()
    job = get_object_or_404(Job, page_number=job_id)
    return render(request, "detail.html", {"job_detail": job, "row_count": count})

def next(request, job_id):
    count = Job.objects.count()

    if job_id + 1 > count:
        return redirect("/jobapp/detail/1")
    else:
        return redirect("/jobapp/detail/" + str(job_id + 1))

def before(request, job_id):
    count = Job.objects.count()
    if job_id - 1 == 0:
        return redirect("/jobapp/detail/" + str(count))
    else:
        return redirect("/jobapp/detail/" + str(job_id - 1))

def write(request):
    if request.method == "POST":
        job = Job()
        job.author = request.user
        job.title = request.POST["title"]
        try:
            job.image = request.FILES["image"]
        except:
            pass
        job.body = request.POST["body"]
        job.pub_date = timezone.datetime.now()
        job.page_number = Job.objects.count() + 1
        job.save()
        return redirect("/jobapp/detail/" + str(job.page_number))
    else:
        return render(request, "write.html")

def rewrite(request, job_id):
    if request.method == "POST":
        job = get_object_or_404(Job, page_number=job_id)
        job.title = request.POST["title"]
        job.body = request.POST["body"]
        job.pub_date = timezone.datetime.now()
        job.save()
        return redirect("/jobapp/detail/" + str(job_id))
    else:
        job = get_object_or_404(Job, page_number=job_id)
        return render(request, "rewrite.html", {"job": job})

def remove(request, job_id):
    job = get_object_or_404(Job, page_number=job_id)
    job.delete()

    object_all = Job.objects.all()
    for item in object_all:
        if item.page_number > job_id:
            item.page_number = item.page_number - 1
            item.save()
        else:
            pass

    return redirect("/jobapp/job")

def search(request):
    jobs = Job.objects.all().order_by('-id')
    q = request.POST.get('q', "")

    if q:
        jobs = jobs.filter(title__icontains=q)
        return render(request, 'search.html', {'jobs': jobs, 'q' : q})
    else:
        return render(request, 'search.html')