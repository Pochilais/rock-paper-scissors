# RPS.py

import random
from collections import Counter

def player(prev_play, opponent_history=[], memory={}):
    # Reiniciar memoria en nueva partida
    if not opponent_history:
        memory.clear()
        memory['moves'] = ['R', 'P', 'S']
        memory['freq'] = {'R': 0, 'P': 0, 'S': 0}
        memory['last_move'] = ''
        memory['counter'] = {'R': 'P', 'P': 'S', 'S': 'R'}
        memory['pattern_len'] = 3
        memory['play_order'] = {}
        memory['game_count'] = 0

    opponent_history.append(prev_play)
    memory['game_count'] += 1

    # Actualizar frecuencias
    if prev_play:
        memory['freq'][prev_play] += 1

    # --- Predicción basada en patrones ---
    def predict_pattern(history, pattern_len=3):
        play_order = memory.get('play_order', {})
        if len(history) < pattern_len + 1:
            return random.choice(memory['moves'])

        last_pattern = ''.join(history[-pattern_len:])
        play_order[last_pattern] = play_order.get(last_pattern, 0) + 1
        memory['play_order'] = play_order

        potential_plays = [k for k in play_order if k.startswith(last_pattern[1:])]

        if potential_plays:
            next_move = max(potential_plays, key=lambda x: play_order[x])[-1]
            return memory['counter'][next_move]
        return random.choice(memory['moves'])

    # --- Jugada principal ---
    if memory['game_count'] < 5:
        guess = random.choice(memory['moves'])  # Aleatorio al inicio
    else:
        freq_move = max(memory['freq'], key=memory['freq'].get)
        guess = memory['counter'][freq_move]  # Contra movida más común
        pattern_guess = predict_pattern(opponent_history)
        guess = pattern_guess  # Usamos predicción de patrones

    memory['last_move'] = guess
    return guess
    