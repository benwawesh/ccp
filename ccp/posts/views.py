import json
from django.db.models import Q
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from posts.models import Post, Voter
from django.http import HttpResponse
from django.db.models import F
from accounts.models import WebUser
import datetime






# Create your views here.

@login_required(login_url='accounts:login_page')
def create_post_index(request):
    template = 'posts/create_post.html'
    if request.method != 'POST':
        context = {
        }
        return render(request, template, context)
    else:
        post_content = request.POST.get('message')

        try:
            author = User.objects.get(id=request.user.id)
            post = Post.objects.create(
                content= post_content,
                owner = author,
                date_created = datetime.datetime.now()
            )
            return HttpResponse(json.dumps({'status': 1, 'message': 'Post created successfully'}))
        except Exception as e:
            print(e)
            return HttpResponse(json.dumps({'status': 0, 'message': 'Post not created!'}))


@login_required(login_url='accounts:login_page')
def get_posts(request):
    post_data = Post.objects.all().order_by('-date_created')
    template = 'posts/post_results.html'

    context = {"posts": post_data}
    return render(request, template, context)




@login_required(login_url='accounts:login_page')
def up_vote(request):
    content_id = request.POST.get('content_id')
    voter_id = request.POST.get('voter_id')
    print("post id {}".format(content_id))
    print("voter id {}".format(voter_id))
    post = Post.objects.get(id=content_id)
    web_user = WebUser.objects.get(user__id=voter_id)

    try:
        Voter.objects.get(Q(post=post) & Q(post_voter=web_user))
        print("Voter already voted on this post")
        return HttpResponse(json.dumps({'status': 0, 'message': 'Cannot record vote, You already voted on this post'}))

    except Exception as e:
        print(e)
        print("voter yet to vote")
        up_votes= post.up_vote
        post.up_vote_count = F('up_vote_count') + 1
        #post.post_votes.add("POS")
        post.save()
        new_voter = Voter()
        new_voter.post=post
        new_voter.post_voter=web_user
        new_voter.save()
        print("added voter {}".format(new_voter))
        posty = Post()
        print(posty)
        print(post)
        post.refresh_from_db()
        print(type(post.up_vote_count))
        total_votes = (post.up_vote_count + post.down_vote_count)
        print("Up vote count {}".format(post.up_vote_count))

        return HttpResponse(json.dumps({'status': '1', 'message': 'Vote recorded successfully', 'up_vote_count': post.up_vote_count, 'total_vote_count':total_votes}))


@login_required(login_url='accounts:login_page')
def down_vote(request):
    content_id = request.POST.get('content_id')
    voter_id = request.POST.get('voter_id')
    print("post id {}".format(content_id))
    print("voter id {}".format(voter_id))
    post = Post.objects.get(id=content_id)
    web_user = WebUser.objects.get(user__id=voter_id)

    try:
        Voter.objects.get(Q(post=post) & Q(post_voter=web_user))
        print("Voter already voted on this post")
        return HttpResponse(json.dumps({'status': 0, 'message': 'Cannot record vote, You already voted on this post'}))

    except Exception as e:
        print(e)
        print("voter yet to vote")
        up_votes= post.down_vote
        post.down_vote_count = F('down_vote_count') + 1
        #post.post_votes.add("NEG")
        post.save()
        new_voter = Voter()
        new_voter.post=post
        new_voter.post_voter=web_user
        new_voter.save()
        print("added voter {}".format(new_voter))
        posty = Post()
        print(posty)
        print(post)
        post.refresh_from_db()
        print(type(post.down_vote_count))
        total_votes = (post.down_vote_count + post.up_vote_count)
        print("Up vote count {}".format(post.down_vote_count))

        return HttpResponse(json.dumps({'status': '1', 'message': 'Vote recorded successfully', 'down_vote_count': post.down_vote_count, 'total_vote_count':total_votes}))



















