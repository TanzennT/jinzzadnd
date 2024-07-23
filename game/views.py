from django.shortcuts import render, redirect
from .models import Game, Character
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from regulation.creation import *
from gemini.functions import *
import json

# Create your views here.

@login_required
def create_character(request, game_id):
    game = Game.objects.get(id=game_id)
    user_character_cnt = Character.objects.filter(game=game, is_user=True).count()
    if user_character_cnt >= 1:
        return redirect('game:detail', game_id=game_id)
    if request.method == "POST":
        # print(request.POST.get('origin'))
        character = Character()
        character.origin = request.POST.get('origin')
        character.game = game
        character.name = request.POST.get('name')
        character.is_user = True
        character.stat = ORIGINS[character.origin]['stats']
        character.hp = character.stat[2] * 2 + 10
        character.save()
        game.name = f"{character.name}'s game"
        game.last_response = generate_intro(game_id)
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
    if game.user != request.user:
        return render(request, 'invalid.html')
    return render(request, 'game/play.html', {'game': game})


@login_required
def send_message(request):
    if request.method == "POST":
        data = json.loads(request.body)
        game = Game.objects.get(id=data['game_id'])
        print(data)
        response = generate_response(data['message'], data['game_id'])
        print(response)
        game.last_response = response
        game.save()
        
        return JsonResponse({"ai_response": response}, status=200)
    else:
        return JsonResponse({'success': False, 'error': 'Invalid request method.'}, status=400)