from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.shortcuts import get_object_or_404, render
from django.db.models import F
from django.urls import reverse
from django.views import generic

from .ml import get_question_answer, get_similarity_score

from .models import Question, Choice, Category, Info

import random
import json

class IndexView(generic.ListView):
    template_name = "kgraph/index.html"
    context_object_name = "latest_question_list"
    
    def get_queryset(self):
        return Question.objects.order_by("-pub_date")[:5]
    

class DetailView(generic.DetailView):
    model = Question
    template_name = "kgraph/detail.html"


class ResultsView(generic.DetailView):
    model = Question
    template_name = "kgraph/results.html"

def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST["choice"])
    except (KeyError, Choice.DoesNotExist):
        return render(
                    request, 
                    "kgraph/detail.html",
                    {
                        "question" : question,
                        "error_message" : "You didn't select a choice.",
                    },
                ) 
    else:
        selected_choice.votes = F("votes") + 1
        selected_choice.save()
        return HttpResponseRedirect(reverse("kgraph:results", args=(question.id,)))

################
'''
Helper functions
'''

def get_colour(category: Category) -> str:
    norm = max(0, min(category.timestamp / 100, 1))     # Normalize to [0,1]
    inv = 1 - norm                             # So 0 → 1.0 (light), 100 → 0.0 (dark)

    gray = int(50 + inv * (230 - 50))          # Map to [50, 230]
    r = int(10 + inv * (200 - 10))   # From 200 (light) to 10 (dark)
    g = int(50 + inv * (170 - 50))   # From 220 (light) to 50 (dark)
    b = int(150 + inv * (105))       # From 255 (light) to 150 (dark)
    return f"rgb({r},{g},{b})"

def get_edge_length(category: Category) -> int:
    return max(20, int((10 - category.neighbour_node_weight) * 100))

def get_node_width(category: Category) -> float:
    return max(1, category.neighbour_node_weight)


################


def CategoryView(request):
    categories = Category.objects.all()
    
    nodes = []
    edges = []
    seen_edges = set()
    topic_to_id = {category.topic: category.id for category in categories}

    for category in categories:
        nodes.append({
            "id" : category.id,
            "label" : category.topic,
            "color": {
                "background": get_colour(category),
                "border": "#333",     # Optional: dark border
            }
        })

        # edge case - single node
        if category.neighbour_node == "":
            continue
    
        # subtract from timestamp (for now)
        if category.timestamp > 0:
            category.timestamp -= 1
        category.save()

        
        edge_key = tuple(sorted((category.topic, category.neighbour_node)))
        if edge_key not in seen_edges:
            edges.append({
                "from" : category.id,
                "to" : topic_to_id[category.neighbour_node],
                "label" : str(category.neighbour_node_weight),
                "width" : get_node_width(category),
                "length": get_edge_length(category)
            })
            seen_edges.add(edge_key)
    
    return render(request, "kgraph/categories.html", {
        "nodes" : json.dumps(nodes),
        "edges" : json.dumps(edges),
        "topic_to_id" : json.dumps(topic_to_id),
    })


class InfoView(generic.DetailView):
    model = Category
    template_name = "kgraph/info.html"


def CreateCategoryView(request):
    return render(request, "kgraph/create_category.html")


def create_new_category(request):
    input_topic = request.POST["topic"]
    
    neighbour_node = ""
    neighbour_node_weight = 0
    categories = list(Category.objects.all())
    for c in categories:
        tmp_weight = get_similarity_score(input_topic, c.topic)

        if tmp_weight > c.neighbour_node_weight:
            c.neighbour_node = input_topic
            c.neighbour_node_weight = tmp_weight
            c.save()

        if tmp_weight > neighbour_node_weight:

            neighbour_node_weight = tmp_weight
            neighbour_node = c.topic


    category_obj = Category(topic=input_topic, neighbour_node=neighbour_node, neighbour_node_weight=neighbour_node_weight)
    category_obj.save()
    return HttpResponseRedirect(reverse("kgraph:categories"))


def delete_category(request, category_id):
    selected_category = Category.objects.get(id=category_id)

    categories = list(Category.objects.all())
    
    # optimization: typically a node has few neighbours, so we narrow down the
    # search space to only those that have the deleted category as a neighbour
    to_update = []
    for c in categories:
        if c.neighbour_node == selected_category.topic:
            to_update.append(c)

    selected_category.delete()

    for node in to_update:
        node.neighbour_node = ""
        node.neighbour_node_weight = 0

        for nei in categories:
            if node != nei and nei != selected_category.topic:
                tmp_weight = get_similarity_score(node.topic, nei.topic)

                if tmp_weight > node.neighbour_node_weight:
                    
                    node.neighbour_node = nei.topic
                    node.neighbour_node_weight = tmp_weight
        
        node.save()
                

    return HttpResponseRedirect(reverse("kgraph:categories"))


def CreateInfoView(request, category_id):
    return render(request, "kgraph/create_info.html", {
        "category_id": category_id,
    })


def create_new_info(request, category_id):
    input_info = request.POST["info"]
    parent_category = Category.objects.get(id=category_id)
    info_obj = Info(category=parent_category, info=input_info)
    info_obj.save()
    return HttpResponseRedirect(reverse("kgraph:info", args=(category_id,)))


def delete_info(request, category_id, info_id):
    selected_info = Info.objects.get(id=info_id)
    selected_info.delete()

    return HttpResponseRedirect(reverse("kgraph:info", args=(category_id,)))


def quiz_me(request, category_id):
        
    def get_random_info(category_id):
        infos = list(Info.objects.filter(category=category_id))
        return infos[random.randint(0, len(infos) - 1)]

    random_category = Category.objects.get(pk=category_id)
    random_info = get_random_info(random_category.id)
    qa = get_question_answer(random_category.topic, random_info.info)
    print("website link", qa.website_link)
    return render(request, "kgraph/quiz_me.html", {
        "category_id" : random_category.id,
        "question" : qa.question,
        "correct_answer" : qa.correct_answer,
        "wrong_answer_1" : qa.wrong_answer_1,
        "wrong_answer_2" : qa.wrong_answer_2,
        "website_link" : qa.website_link,
    })


def increment_category(request, category_id):
    ans = request.POST.get("choice")

    if ans == "correct_answer":
        category = Category.objects.get(pk=category_id)
        category.timestamp = 100
        category.save()

    return HttpResponseRedirect(reverse("kgraph:categories"))