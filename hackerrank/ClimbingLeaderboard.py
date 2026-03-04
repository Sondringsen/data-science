"""
All solutions time out except the last one. Need to start from behind to get O(m+n) not O(m*n).
"""


def climbingLeaderboard(ranked, player):
    # Write your code here
    ranks = {}
    old_score = 0
    rank_counter = 1
    for score in ranked:
        if score == old_score: continue
        ranks[score] = rank_counter
        rank_counter += 1
        old_score = score
        
    player_ranks = []
    for player_score in player:
        added = False
        for ranked_score in ranked:
            if player_score >= ranked_score:
                added = True
                player_ranks.append(ranks[ranked_score])
                break
        if not added:
            player_ranks.append(rank_counter)
    
    return player_ranks
        

def climbingLeaderboard(ranked, player):
    # Write your code here
    player_ranks = []
    for player_score in player:
        rank = 1
        added = False
        for i in range(len(ranked)):
            ranked_score = ranked[i]
            if player_score >= ranked_score:
                player_ranks.append(rank)
                added = True
                break
            elif player_score < ranked_score and i == len(ranked) - 1:
                rank += 1
            elif player_score < ranked_score and ranked_score != ranked[i+1]:
                rank += 1
        if not added:
            player_ranks.append(rank)
            
    return player_ranks
    

def climbingLeaderboard(ranked, player):
    # Write your code here
    unique_ranked = []
    for ranked_score in ranked:
        if ranked_score not in unique_ranked: 
            unique_ranked.append(ranked_score)
            
    player_ranks = []
    for player_score in player:
        for rank, ranked_score in enumerate(unique_ranked):
            if player_score >= ranked_score:
                player_ranks.append(rank + 1)
                break
            elif player_score < ranked_score and rank == len(unique_ranked) - 1:
                player_ranks.append(rank + 2)
                
    return player_ranks


def climbingLeaderboard(ranked, player):
    # Write your code here
    ranked = sorted(set(ranked), reverse=True)
    
    result = []
    i = len(ranked) - 1  # Start from lowest rank
    
    for score in player:
        while i >= 0 and score >= ranked[i]:
            i -= 1
        result.append(i + 2)