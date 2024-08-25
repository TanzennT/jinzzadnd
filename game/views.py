from django.shortcuts import render, redirect
from .models import Game, Character, Log
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from regulation.creation import *
from gemini.functions import *
import json
from django.template.defaulttags import register

@register.filter(name='max')
def max(vigor): 
    vigor = int(vigor)
    return vigor * 2 + 10


@register.filter(name='tidy')
def tidy(value):
    index = value.find("-&-&-")
    value = value[(index+5):]
    index = value.find("-&-&-")
    value = value[:(index)]
    return value
# Create your views here.

@login_required
def create_character(request, game_id):
    game = Game.objects.get(id=game_id)
    user_character_cnt = Character.objects.filter(game=game, is_user=True).count()
    if user_character_cnt >= 1:
        return redirect('game:detail', game_id=game_id)
    if request.method == "POST":
        # Save Character
        character = Character()
        character.origin = request.POST.get('origin')
        character.game = game
        character.name = request.POST.get('name')
        character.is_user = True
        character.stat = ORIGINS[character.origin]['stats']
        character.level = ORIGINS[character.origin]['level']
        character.hp = character.stat[2] * 2 + 10
        character.inventory = ORIGINS[character.origin]['items']
        character.equipped = ['', '', ''] # Left, Right, Armor
        character.save()

        # Save Game
        game.name = f"{character.name}'s game"
        intro = generate_intro(game_id)
        game.last_response = intro
        game.save()


        return redirect('game:detail', game_id=game_id)
    return render(request, 'game/create_character.html', {'origins': ORIGINS, 'traits': TRAITS, 'gifts': GIFTS})

@login_required
def create_game(request):
    if request.method == "POST":
        if Game.objects.filter(user=request.user).count() >= 3:
            return JsonResponse({"message": "User already has 3 games."}, status=202)
        game = Game.objects.create(
            name = "Default_Game_Name",
            setting = "Default_Setting",
            user = request.user
        )
        return JsonResponse({"message": "Game Successfully Created.", "gameID": game.id}, status=200)
    else:
        return JsonResponse({"message": "Invalid request method"}, status=400)
    
@login_required
def list(request):
    currentUser = request.user
    saved_games = Game.objects.filter(user=currentUser)
    return render(request, 'game/list.html', {'games': saved_games})

@login_required
def detail(request, game_id):
    game = Game.objects.get(id=game_id)
    try:
        user_character = Character.objects.get(game=game)
        if game.user != request.user:
            return render(request, 'invalid.html')
        return render(request, 'game/detail.html', {'game': game, 'character': user_character})
    except Character.DoesNotExist:
            return redirect('game:create_character', game_id=game_id)


@login_required
def play(request, game_id):
    game = Game.objects.get(id=game_id)
    print(game.log_set.all())
    character = Character.objects.get(game=game)
    if game.user != request.user:
        return render(request, 'invalid.html')
    return render(request, 'game/play.html', {'game': game, 'inventory': character.inventory, 'character': character})


@login_required
def send_message(request):
    if request.method == "POST":
        data = json.loads(request.body)
        game = Game.objects.get(id=data['game_id'])
        print(data)
        response = generate_response(data['message'], data['game_id'])
        character = Character.objects.get(game=game)
        print(response)
        print(character)
        context = {}
        context["ai_response"] = response["response"]
        status = response["user_status"]
        if status.get("inventory") is not None or status.get("equipped") is not None:  
            character.inventory = status.get("inventory", character.inventory)
            character.save()
            context["inventory"] = character.inventory
            character.equipped = status.get("equipped", character.equipped)
            context["equipped"] = character.equipped
        if status.get("hp") is not None:
            character.hp = status["hp"]
        if status.get("stat") is not None:
            character.stat = status['stat']
        return JsonResponse(context, status=200)
    else:
        return JsonResponse({'success': False, 'error': 'Invalid request method.'}, status=400)