import random
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

def valid_draw(winner, runner_up):
    return winner[0] != runner_up[0] and winner[1] != runner_up[1]

def simulate_draw(winners, runner_ups):
    draw = []
    shuffled_winners = list(winners.items())
    random.shuffle(shuffled_winners)
    for winner_team, winner_info in shuffled_winners:
        valid_runner_ups = [team for team, info in runner_ups.items() if valid_draw(winner_info, info)]

        if not valid_runner_ups:
            return None

        runner_up_team = random.choice(valid_runner_ups)
        draw.append((winner_team, runner_up_team))

        del runner_ups[runner_up_team]

    return draw

def probability_heatmap(simulation_results, winners, runner_ups):
    matchup_counts = pd.DataFrame(0, index=list(winners.keys()), columns=list(runner_ups.keys()))

    for draw in simulation_results:
        for winner, runner_up in draw:
            matchup_counts.at[winner, runner_up] += 1

    matchup_probabilities = matchup_counts / len(simulation_results)

    plt.figure(figsize=(10, 8))
    sns.heatmap(matchup_probabilities, annot=True, fmt=".2f", cmap="YlGnBu")
    plt.title(f"Champions League 23/24 Draw Probability Heatmap ({len(simulation_results)})")
    plt.ylabel("Winners")
    plt.xlabel("Runner-ups")
    plt.show()

def simulate_cl_draw_heatmap(winners, runner_ups, simulations):
    results = []
    counter = 0
    while counter < simulations:
        available_runner_ups = runner_ups.copy()
        draw_result = simulate_draw(winners, available_runner_ups)
        if draw_result:
            results.append(draw_result)
            counter += 1

    probability_heatmap(results, winners, runner_ups)
    return results


def main():
  winners = {
          'BAY': ['GER', 'A'],
          'ARS': ['ENG', 'B'],
          'RMA': ['SPA', 'C'],
          'RSO': ['SPA', 'D'],
          'ATM': ['SPA', 'E'],
          'DOR': ['GER', 'F'],
          'MCI': ['ENG', 'G'],
          'BAR': ['SPA', 'H'],
          }
  runner_ups = {
          'CPH': ['DEN', 'A'],
          'PSV': ['NED', 'B'],
          'NAP': ['ITA', 'C'],
          'INT': ['ITA', 'D'],
          'LAZ': ['ITA', 'E'],
          'PSG': ['FRA', 'F'],
          'RBL': ['GER', 'G'],
          'POR': ['POR', 'H'],
          }
  simulate_cl_draw_heatmap(winners, runner_ups, 100000)


if __name__ == "__main__":
  main()


