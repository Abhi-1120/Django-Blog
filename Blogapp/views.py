from django.shortcuts import render, HttpResponse, redirect
from Blogapp.models import Post, BlogComment
from django.contrib import messages


def blogHome(request):
    allposts = Post.objects.all().order_by('-timestamp')
    context = {'allposts': allposts}
    return render(request, "Blogapp/bloghome.html", context)


def blogPost(request, slug):
    photos = Post.objects.all()
    post=Post.objects.filter(slug=slug).first()
    comments= BlogComment.objects.filter(post=post, parent=None)
    replies= BlogComment.objects.filter(post=post).exclude(parent=None)
    replyDict={}
    for reply in replies:
        if reply.parent.sno not in replyDict.keys():
            replyDict[reply.parent.sno]=[reply]
        else:
            replyDict[reply.parent.sno].append(reply)

    context={'post':post, 'comments': comments, 'user': request.user, 'replyDict': replyDict, 'photo': photos}
    return render(request, "Blogapp/blogPost.html", context)


def postComment(request):
    if request.method == "POST":
        comment = request.POST.get('comment')
        user = request.user
        postSno = request.POST.get('postSno')
        post = Post.objects.get(sno=postSno)
        parentSno = request.POST.get('parentSno')
        if parentSno == "":
            comment = BlogComment(comment=comment, user=user, post=post)
            comment.save()
            messages.success(request, "Your comment has been posted successfully")
        else:
            parent = BlogComment.objects.get(sno=parentSno)
            comment = BlogComment(comment=comment, user=user, post=post, parent=parent)
            comment.save()
            messages.success(request, "Your reply has been posted successfully")

    return redirect(f"/blog/{post.slug}")

