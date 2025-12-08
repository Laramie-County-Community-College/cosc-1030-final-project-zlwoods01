import random

P_THREE_MAKE = 0.35
P_TWO_MAKE = 0.55
P_FT_MAKE = 0.75
P_OFF_REB_FT = 0.10
P_OT_WIN = 0.50

def attempt_shot(prob):
    return random.random() < prob

def attempt_free_throw():
    return random.random() < P_FT_MAKE

def offensive_rebound():
    return random.random() < P_OFF_REB_FT

def simulate_strategy_three():
    made_three = attempt_shot(P_THREE_MAKE)
    if made_three:
        return random.random() < P_OT_WIN
    return False

def simulate_strategy_two():
    made_two = attempt_shot(P_TWO_MAKE)
    if not made_two:
        return False

    ft1 = attempt_free_throw()
    ft2 = attempt_free_throw()
    opponent_points = ft1 + ft2

    if opponent_points == 2:
        return False

    if opponent_points == 1:
        return attempt_shot(P_THREE_MAKE)

    if not offensive_rebound():
        return attempt_shot(P_THREE_MAKE) or attempt_shot(P_TWO_MAKE)

    return False

def run_simulation(n=10000):
    three_wins = 0
    two_wins = 0

    for _ in range(n):
        if simulate_strategy_three():
            three_wins += 1
        if simulate_strategy_two():
            two_wins += 1

    print(f"Total Simulations: {n}")
    print("-----------------------------------")
    print(f"Strategy: Take 3 Immediately → Win Rate: {three_wins/n:.3f}")
    print(f"Strategy: Quick 2 + Foul → Win Rate:  {two_wins/n:.3f}")

if __name__ == "__main__":
    run_simulation(10000)
import random

THREE_PT_PCT = 0.35
TWO_PT_PCT = 0.55
OPP_FT_PCT = 0.60
OFF_REB_PCT = 0.20
OT_WIN_PROB = 0.50

SIMULATIONS = 50000

def attempt_shot(percentage):
    return random.random() < percentage

def shoot_free_throws(ft_pct, shots=2):
    points = 0
    for _ in range(shots):
        if attempt_shot(ft_pct):
            points += 1
    return points

def simulate_take_three():
    score = 0
    if attempt_shot(THREE_PT_PCT):
        score += 3
        return random.random() < OT_WIN_PROB, score
    if random.random() < OFF_REB_PCT:
        if attempt_shot(TWO_PT_PCT):
            score += 2
            return random.random() < OT_WIN_PROB, score
    return False, score

def simulate_foul_strategy():
    score = 0
    if attempt_shot(TWO_PT_PCT):
        score += 2
    else:
        if random.random() < OFF_REB_PCT and attempt_shot(TWO_PT_PCT):
            score += 2
    if score < 2:
        return False, score
    opp_points = shoot_free_throws(OPP_FT_PCT, 2)
    if attempt_shot(THREE_PT_PCT):
        return random.random() < OT_WIN_PROB, score + 3
    else:
        if random.random() < OFF_REB_PCT and attempt_shot(THREE_PT_PCT):
            return random.random() < OT_WIN_PROB, score + 3
    return False, score

three_wins = 0
three_points = 0
foul_wins = 0
foul_points = 0

for _ in range(SIMULATIONS):
    w, pts = simulate_take_three()
    if w: three_wins += 1
    three_points += pts

    w2, pts2 = simulate_foul_strategy()
    if w2: foul_wins += 1
    foul_points += pts2

print("TAKE THE 3")
print("Win %:", round(three_wins / SIMULATIONS * 100, 2))
print("Avg Points:", round(three_points / SIMULATIONS, 2))

print("\nTAKE THE 2 + FOUL")
print("Win %:", round(foul_wins / SIMULATIONS * 100, 2))
print("Avg Points:", round(foul_points / SIMULATIONS, 2))
