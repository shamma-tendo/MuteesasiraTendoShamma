# Assignment 3: Real-World Application of Loop Control Statements
# Program: FIFA World Cup 2026 - National Team Manager Simulation

# MUTEESASIRA TENDO SHAMMA 2400707480 


import random
import time

# TEAM DATA: Using real countries competing at FIFA World Cup 2026
# The tournament expands to 48 teams across USA, Canada & Mexico

WORLD_CUP_TEAMS = [
    "Brazil", "Argentina", "Colombia", "Ecuador", "Paraguay", "Uruguay",
    "England", "France", "Germany", "Spain", "Portugal", "Netherlands",
    "Belgium", "Croatia", "Austria", "Switzerland", "Sweden", "Scotland",
    "Norway", "Bosnia and Herzegovina", "Czechia", "Turkey",
    "USA", "Mexico", "Canada", "Panama", "Curaçao", "Haiti",
    "Japan", "South Korea", "Australia", "Iran", "Saudi Arabia", "Qatar",
    "Jordan", "Iraq", "Uzbekistan",
    "Egypt", "Morocco", "Senegal", "Ghana", "Algeria", "Ivory Coast",
    "Tunisia", "Cape Verde", "South Africa", "DR Congo",
    "New Zealand"
]

# Map teams to FIFA Confederations
TEAMS_BY_CONFEDERATION = {
    "CONMEBOL": ["Brazil", "Argentina", "Colombia", "Ecuador", "Paraguay", "Uruguay"],
    "UEFA": ["England", "France", "Germany", "Spain", "Portugal", "Netherlands", "Belgium", "Croatia", "Austria", "Switzerland", "Sweden", "Scotland", "Norway", "Bosnia and Herzegovina", "Czechia", "Turkey"],
    "CONCACAF": ["USA", "Mexico", "Canada", "Panama", "Curaçao", "Haiti"],
    "AFC": ["Japan", "South Korea", "Australia", "Iran", "Saudi Arabia", "Qatar", "Jordan", "Iraq", "Uzbekistan"],
    "CAF": ["Egypt", "Morocco", "Senegal", "Ghana", "Algeria", "Ivory Coast", "Tunisia", "Cape Verde", "South Africa", "DR Congo"],
    "OFC": ["New Zealand"]
}

KNOCKOUT_ROUNDS = [
    "Round of 16",
    "Quarter-Final",
    "Semi-Final",
    "Final"
]


# HELPER FUNCTIONS


def print_divider(char="=", length=60):
    print(char * length)

def print_stats(morale, strength, injuries):
    print(f"\n  📊 Team Stats  |  Morale: {morale}/10  |  "
          f"Strength: {strength}/10  |  Injuries: {injuries}")

def get_choice(prompt, valid_options):
    """Keep asking until the user gives a valid choice."""
    while True:                                         # <-- while loop
        choice = input(prompt).strip().lower()
        if choice in valid_options:
            return choice
        print(f"  ⚠  Invalid input. Choose from: {valid_options}")

def display_teams_by_confederation():
    """Display all World Cup 2026 teams organized by confederation in table format."""
    print("\n🏆 2026 FIFA WORLD CUP - 48 QUALIFIED NATIONS 🏆")
    print("Organized by FIFA Confederation:\n")
    
    # Get max teams in any confederation for table alignment
    max_teams = max(len(teams) for teams in TEAMS_BY_CONFEDERATION.values())
    
    # Create headers
    headers = list(TEAMS_BY_CONFEDERATION.keys())
    header_line = "  " + " | ".join(f"{h:^20}" for h in headers)
    divider = "  " + "-" * (len(header_line) - 2)
    
    print(header_line)
    print(divider)
    
    # Get teams for each confederation and organize them
    confederation_teams = {}
    for conf, teams in TEAMS_BY_CONFEDERATION.items():
        confederation_teams[conf] = sorted(teams)
    
    # Print teams row by row
    for row_idx in range(max_teams):
        row_data = []
        for conf in headers:
            teams = confederation_teams[conf]
            if row_idx < len(teams):
                row_data.append(f"{teams[row_idx]:^20}")
            else:
                row_data.append(f"{'':^20}")
        print("  " + " | ".join(row_data))
    
    print(divider)
    print()

def get_player_country():
    """Let the user enter their country name from the World Cup 2026 table."""
    while True:
        country_input = input("\n  Enter your country name: ").strip()
        
        # Check if country exists (case-insensitive match)
        for country in WORLD_CUP_TEAMS:
            if country.lower() == country_input.lower():
                return country
        
        print(f"  ⚠  '{country_input}' is not in the World Cup 2026. Please check the table above and try again.")

def get_opponent_confederation(player_country):
    """Get the confederation of the player's country."""
    for confederation, teams in TEAMS_BY_CONFEDERATION.items():
        if player_country in teams:
            return confederation
    return None

def get_valid_opponents(player_country, already_selected):
    """Get list of valid opponents (different confederation from player's country and not already selected)."""
    player_confederation = get_opponent_confederation(player_country)
    valid_opponents = []
    
    for confederation, teams in TEAMS_BY_CONFEDERATION.items():
        if confederation != player_confederation:
            for team in teams:
                if team not in already_selected and team != player_country:
                    valid_opponents.append(team)
    
    return valid_opponents

def get_valid_opponents_different_confederation(player_country, already_selected):
    """Get list of valid opponents from confederations not yet selected (for group/knockout stages)."""
    player_confederation = get_opponent_confederation(player_country)
    
    # Get confederations already used by selected opponents
    selected_confederations = set()
    for opponent in already_selected:
        conf = get_opponent_confederation(opponent)
        if conf:
            selected_confederations.add(conf)
    
    valid_opponents = []
    
    for confederation, teams in TEAMS_BY_CONFEDERATION.items():
        # Skip player's own confederation and confederations already used
        if confederation != player_confederation and confederation not in selected_confederations:
            for team in teams:
                if team not in already_selected and team != player_country:
                    valid_opponents.append(team)
    
    return valid_opponents

def select_opponents(player_country, num_opponents):
    """Let the user select specific opponents from different confederations."""
    player_confederation = get_opponent_confederation(player_country)
    
    print(f"\n  Your country: {player_country} ({player_confederation})")
    print(f"  You must choose opponents from DIFFERENT confederations.\n")
    
    selected_opponents = []
    
    for i in range(num_opponents):
        print(f"\n  Selecting Opponent {i + 1} of {num_opponents}:")
        print("  Available opponents (from unused confederations):")
        
        valid_opponents = get_valid_opponents_different_confederation(player_country, selected_opponents)
        
        if not valid_opponents:
            print(f"  ⚠  No more opponents available from different confederations!")
            print(f"  Cannot select {num_opponents} opponents with this constraint.")
            break
        
        for j, opponent in enumerate(valid_opponents, 1):
            confederation = get_opponent_confederation(opponent)
            print(f"    {j:2d}. {opponent} ({confederation})")
        
        while True:
            try:
                choice = int(input(f"  Enter the number of opponent {i + 1}: ").strip())
                if 1 <= choice <= len(valid_opponents):
                    selected_opponent = valid_opponents[choice - 1]
                    selected_opponent_confederation = get_opponent_confederation(selected_opponent)
                    
                    # Double-check: cannot pick from same confederation
                    if selected_opponent_confederation == player_confederation:
                        print(f"  ⚠  {selected_opponent} is from the same confederation ({selected_opponent_confederation})!")
                        print(f"  ⚠  You cannot compete against teams from your own confederation.")
                        continue
                    
                    # Check if confederation already used by another opponent
                    used_confederations = {get_opponent_confederation(opp) for opp in selected_opponents}
                    if selected_opponent_confederation in used_confederations:
                        print(f"  ⚠  {selected_opponent} is from {selected_opponent_confederation}!")
                        print(f"  ⚠  You already have an opponent from {selected_opponent_confederation}.")
                        print(f"  ⚠  Each opponent must be from a different confederation.")
                        continue
                    
                    # Check if already selected
                    if selected_opponent in selected_opponents:
                        print(f"  ⚠  {selected_opponent} has already been selected!")
                        print(f"  ⚠  Cannot compete again. Choose from a different confederation.")
                        continue
                    
                    selected_opponents.append(selected_opponent)
                    print(f"  ✓ {selected_opponent} selected!")
                    break
                else:
                    print(f"  ⚠  Invalid selection. Please enter a number between 1 and {len(valid_opponents)}.")
            except ValueError:
                print("  ⚠  Invalid input. Please enter a number.")
    
    return selected_opponents

def get_random_host():
    """Randomly assign match to one of the three host cities."""
    hosts = ["USA", "Canada", "Mexico"]
    return random.choice(hosts)

def simulate_match(opponent, strength, morale, host):
    """
    Simulate a match result.
    Higher strength + morale = higher win chance.
    Match is played at a randomly assigned host (USA, Canada, or Mexico).
    Returns: 'win', 'draw', or 'loss'
    """
    score = strength + morale + random.randint(1, 5)
    opponent_score = random.randint(8, 18)
    
    # All matches are neutral venues, no advantage/disadvantage
    # (played at host countries USA, Canada, or Mexico)

    if score > opponent_score:
        return "win"
    elif score == opponent_score:
        return "draw"
    else:
        return "loss"



# STAGE 1 — PRE-TOURNAMENT PREPARATION
# Uses: while loop, continue, pass


def pre_tournament_preparation():
    print_divider()
    print("  STAGE 1: PRE-TOURNAMENT PREPARATION")
    print_divider()
    print("\nYou have 3 preparation sessions before the group stage.")
    print("Each choice shapes your team's morale, strength, and injury risk.\n")

    morale   = 6
    strength = 6
    injuries = 0

    session = 1
    while session <= 3:                                 # -- WHILE LOOP --
        print(f"\n  Preparation Session {session} of 3")
        print_stats(morale, strength, injuries)

        print("\n  What will you do?")
        print("  [t] Intense Training    -> +2 Strength, risk of injury")
        print("  [f] Play a Friendly     -> +1 Morale, +1 Strength")
        print("  [r] Rest & Recovery     -> +2 Morale, -1 Injury (if any)")
        print("  [s] Scout Opponents     -> (Future feature - placeholder)")

        choice = get_choice("\n  Your choice: ", ["t", "f", "r", "s"])

        # -- CONTINUE: skip to next session if player scouts (nothing to do yet) --
        if choice == "s":
            print("\n  Scouts dispatched! No immediate effect this session.")
            print("  Skipping to next session...")
            session += 1
            continue                                    # -- CONTINUE --

        # -- PASS: placeholder for a future "press conference" feature --
        if choice == "p":
            pass                                        # -- PASS (placeholder) --

        if choice == "t":
            strength = min(strength + 2, 10)
            injury_roll = random.randint(1, 5)
            if injury_roll == 1:
                injuries += 1
                morale = max(morale - 1, 1)
                print(f"\n  Intense training pays off! Strength up.")
                print(f"  But a player picked up an injury! Injuries: {injuries}")
            else:
                print(f"\n  Intense training pays off! Strength up. No injuries.")

        elif choice == "f":
            morale   = min(morale + 1, 10)
            strength = min(strength + 1, 10)
            print(f"\n  Great friendly match! Morale and Strength both up.")

        elif choice == "r":
            morale = min(morale + 2, 10)
            if injuries > 0:
                injuries -= 1
                print(f"\n  Rest session. Morale up, one player recovered!")
            else:
                print(f"\n  Rest session. Morale up. Squad is fresh.")

        # -- CHECK: if injuries mount, warn the manager --
        if injuries >= 3:
            print("\n  WARNING: Too many injuries! Consider resting the squad.")

        session += 1                                    # advance loop counter

    # Apply injury penalty to strength before tournament
    strength = max(strength - injuries, 1)
    print("\n")
    print_divider()
    print(f"  Preparation complete! Final pre-tournament stats:")
    print_stats(morale, strength, injuries)
    print_divider()

    return morale, strength, injuries



# STAGE 2 — GROUP STAGE (3 matches)
# Uses: while loop, break, continue


def group_stage(player_country, group_opponents, morale, strength, injuries):
    print("\n")
    print_divider()
    print("  STAGE 2: GROUP STAGE")
    print_divider()
    print(f"\nYour country: {player_country}")
    print(f"Your group opponents: {', '.join(group_opponents)}")
    print("You need at least 4 points to qualify.\n")

    points    = 0
    match_num = 0
    eliminated = False

    while match_num < len(group_opponents):       # -- WHILE LOOP --
        opponent = group_opponents[match_num]
        print_divider("-")
        print(f"  Group Match {match_num + 1}: {player_country} vs {opponent}")
        print_stats(morale, strength, injuries)

        print("\n  Pre-match decision:")
        print("  [a] Attack -- high risk, high reward (+1 Strength for this match)")
        print("  [d] Defend -- low risk, safer outcome  (+1 Morale for this match)")
        print("  [n] Normal setup -- balanced approach")

        tactic = get_choice("\n  Choose your tactic: ", ["a", "d", "n"])

        match_strength = strength
        match_morale   = morale

        if tactic == "a":
            match_strength += 1
            print("\n  Attacking formation selected!")
        elif tactic == "d":
            match_morale += 1
            print("\n  Defensive formation selected!")
        else:
            print("\n  Balanced formation selected.")

        host = get_random_host()

        result = simulate_match(opponent, match_strength, match_morale, host)

        if result == "win":
            points += 3
            morale  = min(morale + 2, 10)
            print(f"\n  RESULT: {player_country} WINS vs {opponent}! +3 points")
            print(f"  Host City: {host}")

        elif result == "draw":
            points += 1
            morale  = min(morale + 1, 10)
            print(f"\n  RESULT: Draw vs {opponent}. +1 point")
            print(f"  Host City: {host}")

        else:
            morale = max(morale - 1, 1)
            print(f"\n  RESULT: {player_country} LOSES vs {opponent}. 0 points")
            print(f"  Host City: {host}")

        print(f"  Points so far: {points}")

        # -- BREAK: early elimination if mathematically out before last match --
        if match_num == 1 and points == 0:
            print("\n  With 0 points after 2 matches, qualification is impossible.")
            print(f"  {player_country} is ELIMINATED from the group stage.")
            eliminated = True
            break                                       # -- BREAK --

        # -- CONTINUE: skip morale boost if team is already at peak morale --
        if morale == 10:
            print("  Morale is already at peak -- skipping morale boost.")
            match_num += 1
            continue                                    # -- CONTINUE --

        match_num += 1

    if not eliminated:
        qualify_threshold = 4
        if points >= qualify_threshold:
            print("\n")
            print_divider()
            print(f"  {player_country} QUALIFIES for the Knockout Stage with {points} points!")
            print_divider()
            return morale, strength, injuries, True
        else:
            print("\n")
            print_divider()
            print(f"  {player_country} exits the tournament with only {points} points.")


# STAGE 3 — KNOCKOUT STAGE
# Uses: while loop, break, continue, pass


def knockout_stage(player_country, knockout_opponents, morale, strength, injuries):
    print("\n")
    print_divider()
    print("  STAGE 3: KNOCKOUT ROUNDS")
    print_divider()

    round_index = 0
    champion    = False

    while round_index < len(KNOCKOUT_ROUNDS):           # -- WHILE LOOP --
        round_name = KNOCKOUT_ROUNDS[round_index]
        opponent   = knockout_opponents[round_index]

        print(f"\n  {round_name.upper()}: {player_country} vs {opponent}")
        print_stats(morale, strength, injuries)

        # -- PASS: placeholder for fan support / stadium atmosphere feature --
        # Future: fan chants affect morale dynamically based on host city
        pass                                            # -- PASS (placeholder) --

        print("\n  Manage your squad before kick-off:")
        print("  [p] Push key players  -> +2 Strength, but risk injury")
        print("  [r] Rotate squad      -> -1 Strength, but safer")
        print("  [k] Keep current plan -> no change")

        decision = get_choice("\n  Your decision: ", ["p", "r", "k"])

        if decision == "p":
            strength = min(strength + 2, 10)
            if random.randint(1, 4) == 1:
                injuries += 1
                print(f"\n  Pushed hard! Strength up -- but a player got hurt. "
                      f"Injuries: {injuries}")
            else:
                print("\n  Players responding well! Strength boosted.")

        elif decision == "r":
            strength = max(strength - 1, 1)
            morale   = min(morale + 1, 10)
            print("\n  Squad rotated. Freshness maintained.")

        else:
            print("\n  Sticking to the current plan.")

        host = get_random_host()

        result = simulate_match(opponent, strength, morale, host)

        if result == "win":
            morale = min(morale + 2, 10)
            print(f"\n  {player_country} BEATS {opponent}! Advancing to the next round!")
            print(f"  Host City: {host}")
            if round_name == "Final":
                champion = True
                break                                   # -- BREAK: won the cup! --

        elif result == "draw":
            # Knockout stage: draws go to penalties
            print(f"\n  Draw after 90 minutes! Going to PENALTIES...")
            print(f"  Host City: {host}")
            penalty_result = random.choice(["win", "loss"])
            if penalty_result == "win":
                morale = min(morale + 1, 10)
                print(f"  {player_country} WINS on penalties! Advancing!")
            else:
                morale = max(morale - 2, 1)
                print(f"  {player_country} LOSES on penalties. Tournament over.")
                break                                   # -- BREAK: eliminated --

        else:
            morale = max(morale - 2, 1)
            print(f"\n  {player_country} LOSES to {opponent}. Knocked out in {round_name}.")
            print(f"  Host City: {host}")
            break                                       # -- BREAK: eliminated --

        # -- CONTINUE: if morale is critical, skip press conference (future feature)
        #    and go straight to preparing for the next match --
        if morale <= 2:
            print("\n  Morale critically low -- skipping press conference.")
            print("  Moving straight to next round preparation...")
            round_index += 1
            continue                                    # -- CONTINUE --

        round_index += 1

    return champion



# MAIN PROGRAM


def main():
    print_divider("=", 60)
    print("  FIFA WORLD CUP 2026 -- MANAGER SIMULATION")
    print("  Tournament hosts: USA / Canada / Mexico")
    print_divider("=", 60)

    # Display teams organized by confederation in table format
    display_teams_by_confederation()

    # Let player select their country
    player_country = get_player_country()
    
    # Let player select group stage opponents
    print_divider()
    print("  GROUP STAGE OPPONENT SELECTION")
    print_divider()
    group_opponents = select_opponents(player_country, 3)
    
    # Let player select knockout stage opponents
    print_divider()
    print("  KNOCKOUT STAGE OPPONENT SELECTION")
    print_divider()
    knockout_opponents = select_opponents(player_country, 4)

    print("\n")
    input("  Press ENTER to begin your World Cup journey...")

    # Stage 1: Preparation
    morale, strength, injuries = pre_tournament_preparation()

    # Stage 2: Group Stage
    morale, strength, injuries, qualified = group_stage(player_country, group_opponents, morale, strength, injuries)

    if not qualified:
        print(f"\n  {player_country} heads home after the group stage.")
        print("  Better luck at World Cup 2030!\n")
        return

    # Stage 3: Knockout Stage
    champion = knockout_stage(player_country, knockout_opponents, morale, strength, injuries)

    # Final Result
    print("\n")
    print_divider("=", 60)
    if champion:
        print(f"  *** {player_country.upper()} ARE WORLD CHAMPIONS! ***")
        print(f"  You led {player_country} to glory at FIFA World Cup 2026!")
    else:
        print(f"  A valiant effort by {player_country}!")
        print("  The team gave everything. Build for the future.")
    print_divider("=", 60)
    print("\n  Thanks for playing. End of simulation.\n")


# Entry point
if __name__ == "__main__":
    main()
