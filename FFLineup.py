
"""
FFLineup.py - Compares your fantasy football roster
against Boris Chen's weekly tiered fantasy football
model and prints out your optimal lineup.
"""

import requests
import warnings

def fetch_tier_data(url):
    """Fetches and parses tier data from a given URL."""
    response = requests.get(url)
    lines = response.text.splitlines()
    tier_dict = {}
    for line in lines:
        if ': ' in line:
            tier_name, players = line.split(': ')
            players_list = players.split(', ')
            tier_dict[tier_name] = players_list
    return tier_dict
    
def recommend_best_player(position_tiers, roster, used_players):
    for player in roster:
        if player not in [p for tier_players in position_tiers.values() for p in tier_players]:
            warnings.warn(f"Player {player} not found in real-time data.")
    
    for tier, players in position_tiers.items():
        for player in players:
            if player in roster and player not in used_players:
                used_players.add(player)
                return player

def recommend_lineup(tier_data, roster, select_flex_first=False):
    recommended_lineup = {}
    used_players = set()
    
    lineup_positions = ['QB', 'WR1', 'WR2', 'RB1', 'RB2', 'TE', 'FLEX', 'K', 'DEF']
    
    if select_flex_first:
        lineup_positions.remove('FLEX')
        lineup_positions.insert(0, 'FLEX')
    
    for pos in lineup_positions:
        core_pos = pos[:-1] if pos[-1].isdigit() else pos
        candidates = []
        
        if core_pos == 'FLEX':
            for flex_pos in ['WR', 'RB', 'TE']:
                for tier in tier_data.get(flex_pos, {}).values():
                    candidates.extend(tier)
            
            candidates = [player for player in candidates if player not in used_players]
            
            # Check if any player in the roster is in the flex rankings
            flex_roster = [player for pos in ['WR', 'RB', 'TE'] for player in roster.get(pos, [])]
            flex_in_tiers = any(player in candidates for player in flex_roster)
            
            if not flex_in_tiers:
                print("Warning: Nobody in your roster is in the flex rankings.")
            
            # Pick from the wide receivers, then running backs, then tight ends until a flex player is found
            for flex_pos in ['WR', 'RB', 'TE']:
                flex_candidate = recommend_best_player(tier_data.get(flex_pos, {}), roster.get(flex_pos, []), used_players)
                if flex_candidate:
                    recommended_lineup['FLEX'] = flex_candidate
                    used_players.add(flex_candidate)
                    break
            
            continue  # Skip the rest of the loop to move on to the next position
        
        else:
            for tier in tier_data.get(core_pos, {}).values():
                candidates.extend(tier)
        
        recommended_player = recommend_best_player({core_pos: candidates}, roster.get(core_pos, []), used_players)
        if recommended_player:
            recommended_lineup[pos] = recommended_player
    
    return recommended_lineup

# Your roster data
roster_dict = {
    'QB': ['Joe Burrow', 'Jordan Love'],
    'WR': ['Garrett Wilson', 'Jaylen Waddle', 'Chris Godwin', 'Christian Watson'],
    'RB': ['Christian McCaffrey', 'Derrick Henry', 'Khalil Herbert', 'AJ Dillon', 'Samaje Perine'],
    'TE': ['T.J. Hockenson', 'Chigoziem Okonkwo'],
    'K': ['Tyler Bass'],
    'DEF': ['Dallas Cowboys']
}

# URLs for tier data
url_dict = {
    'QB': 'https://s3-us-west-1.amazonaws.com/fftiers/out/text_QB.txt',
    'RB': 'https://s3-us-west-1.amazonaws.com/fftiers/out/text_RB.txt',
    'WR': 'https://s3-us-west-1.amazonaws.com/fftiers/out/text_WR.txt',
    'TE': 'https://s3-us-west-1.amazonaws.com/fftiers/out/text_TE.txt',
    'Flex': 'https://s3-us-west-1.amazonaws.com/fftiers/out/text_FLX.txt',
    'K': 'https://s3-us-west-1.amazonaws.com/fftiers/out/text_K.txt',
    'DEF': 'https://s3-us-west-1.amazonaws.com/fftiers/out/text_DST.txt'
}

# Fetch and parse tier data from URLs
tier_data = {}
for position, url in url_dict.items():
    tier_data[position] = fetch_tier_data(url)

# Recommend a lineup based on the fetched tier data and your roster
recommended_lineup = recommend_lineup(tier_data, roster_dict, select_flex_first=False)
print()
print("RECOMMENDED LINEUP")
print("------------------")
for k,v in recommended_lineup.items():
    if len(k)==1:
        print(f'{k}:    {v}')
    elif len(k)==2:
        print(f'{k}:   {v}')
    elif len(k)==3:
        print(f'{k}:  {v}')
    else:
        print(f'{k}: {v}')
