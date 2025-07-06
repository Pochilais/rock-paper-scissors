# RPS.py

import random
from collections import Counter

def player(prev_play, opponent_history=[], memory={
    "patterns": {},
    "last_move": "",
    "counter_moves": {"R": "P", "P": "S", "S": "R"},
    "freq": {"R": 0, "P": 0, "S": 0},
    "game_count": 0,
    "pattern_len": 3
}):
    
    # Reiniciar memoria al inicio de una nueva partida
    if not prev_play:
        memory["patterns"] = {}
        memory["freq"] = {"R": 0, "P": 0, "S": 0}
        memory["game_count"] = 0
        memory["last_move"] = ""
    
    opponent_history.append(prev_play)
    memory["game_count"] += 1

    # Actualizar frecuencia de jugadas del oponente
    if prev_play:
        memory["freq"][prev_play] += 1

    # Predicción basada en patrones (Markov-like)
    def predict_next(history, pattern_len=memory["pattern_len"]):
        if len(history) < pattern_len + 1:
            return random.choice(["R", "P", "S"])
        
        last_pattern = "".join(history[-pattern_len:])
        next_plays = [history[i+pattern_len] for i in range(len(history)-pattern_len) if "".join(history[i:i+pattern_len]) == last_pattern]

        if next_plays:
            most_common = Counter(next_plays).most_common(1)[0][0]
            return memory["counter_moves"][most_common]
        return random.choice(["R", "P", "S"])

    # --- Estrategia inicial aleatoria ---
    if memory["game_count"] < 5:
        guess = random.choice(["R", "P", "S"])
    else:
        freq_move = max(memory["freq"], key=memory["freq"].get)
        pattern_guess = predict_next(opponent_history)
        guess = pattern_guess
    
    memory["last_move"] = guess
    return guess