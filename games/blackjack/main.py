# Go easy on me, this code was produced at the beginning of my python journey. Next time, I'll use classes

logo = """
.------.            _     _            _    _            _
|A_  _ |.          | |   | |          | |  (_)          | |   
|( \/ ).-----.     | |__ | | __ _  ___| | ___  __ _  ___| | __
| \  /|K /\  |     | '_ \| |/ _` |/ __| |/ / |/ _` |/ __| |/ /
|  \/ | /  \ |     | |_) | | (_| | (__|   <| | (_| | (__|   < 
`-----| \  / |     |_.__/|_|\__,_|\___|_|\_\ |\__,_|\___|_|\_\\
      |  \/ K|                            _/ |                
      `------'                           |__/           
"""

import random
import os, platform
import asyncio
import sys

async def ainput(prompt: str = "") -> str:
    if prompt:
        print(prompt, end="")
        sys.stdout.flush()  # <-- critical: forces prompt to appear immediately
    s = await __js_ainput__()
    return "" if s is None else str(s)


def clear():
    # Browser (Pyodide): clear the HTML console
    try:
        import js
        js.globalThis.__clear_console__()
        return
    except Exception:
        pass

    # Local terminal fallback
    import os, platform
    os.system("cls" if platform.system() == "Windows" else "clear")

async def get_play():
    replies = {"yes", "no"}
    while True:
        reply = (await ainput('Would you like to play a game of blackjack? Type "yes" or "no"')).strip().lower()
        if reply in replies:
            print(f'> {reply}')
            return reply
        print('Not a valid response. Type "yes" or "no".')

async def get_balance(kind: str) -> int:
    # kind is "balance" or "bet"
    while True:
        raw = (await ainput(f'Enter your {kind} (whole number): ')).strip()
        try:
            num = int(raw)
        except ValueError:
            print("Must be a valid integer.")
            continue

        if num <= 0:
            print("Must be greater than 0.")
            continue

        return num

def create_deck():
    deck = []
    Special_Cards = ["J", "Q", "K", "A"]
    for suit in range(0,4):
        for card in range(2,11):
            deck.append(card)
        for special in Special_Cards:
            deck.append(special)
    return(deck)

async def get_continue():
    replies = {"yes", "no"}
    while True:
        reply = (await ainput('Continue with the current deck? Type "yes" or "no"> ')).strip().lower()
        if reply in replies:
            return reply
        print('Not a valid response. Type "yes" or "no".')

async def get_split():
    replies = {"yes", "no"}
    while True:
        reply = (await ainput('split? Type "yes" or "no"> ')).strip().lower()
        if reply in replies:
            return reply
        print('Not a valid response. Type "yes" or "no".')

async def choose_ace():
    reply = 0
    is_valid_num = False
    replies = [1, 11]
    while not is_valid_num:
        try:
            reply = int(await ainput('Choose your value for your Ace! "1" or "11":  '))
        except ValueError:
            print("Must be valid integer, no floats, letters, or special charaters")
        if reply not in replies:
            print('Not a valid response. Type: "1" or "11": ')
        else:
            is_valid_num = True
    return(reply)

def get_cards(current_deck, num_of_cards):
    card_count = 0
    cards = []
    while card_count <= (num_of_cards - 1):
        size = len(current_deck)
        card_pos = random.randint(0, size -1)
        cards.append(current_deck[card_pos])
        current_deck.remove(current_deck[card_pos])
        card_count += 1
    return(cards, current_deck)

async def get_action():
    replies = {"hit", "stand"}
    while True:
        reply = (await ainput('Hit or stand? ')).strip().lower()
        if reply in replies:
            print(f'> {reply}')
            return reply
        print('Not a valid response. Type "hit" or "stand".')


def evaluate_deal(Hand):
    display = Hand
    for cards in range(0,len(display)):
        if display[cards] == "A":
            display[cards] = 11
        elif type(display[cards]) is str:
            display[cards] = 10
    hand_value = sum(display)
    if hand_value > 21:
        for cards in range(0,len(display)):
            if display[cards] == 11:
                display[cards] = 1
            elif type(display[cards]) is str:
                display[cards] = 10
    hand_value = sum(display)
    return(hand_value)

async def splithand(current_hands, specific_hand, iterable, count, bet):
    if len(specific_hand) == 2:
        if specific_hand[0] == specific_hand[1]:
            split_decision = await get_split()
            if split_decision == "yes":
                if count < 3:
                    count += 1
                    bet.append(bet[iterable])
                    to_repeat = specific_hand[0]
                    current_hands[iterable].pop(0)
                    current_hands.append([to_repeat])
                else:
                    print("can't split anymore [max 3]!")

    return(current_hands, count, bet)


async def play_blackjack():
    clear()
    print(logo)
    play = await get_play()
    balance = await get_balance("balance")
    iteration = 0
    bet = []
    while play == "yes":

        if iteration > 0:
            clear()
            print(logo)
            print(f'Your current balance is {balance}')
        else:
            print(f'> {balance}')
        bet = []
        initial_bet = await get_balance("bet")
        print(f'> {initial_bet}')
        bet.append(initial_bet)
        iteration += 1
        if iteration == 1:
            deck = create_deck()

        original_cards = get_cards(deck, 2) #Get First Hand
        player_cards = [original_cards[0]]
        deck = original_cards[1]
        original_cards = get_cards(deck, 2)
        dealer_cards = original_cards[0]
        deck = original_cards[1]
        ####################################

        print(f"Your Hand: {player_cards}")
        print(f"Dealer's Hand: {[str(dealer_cards[0]), 'Covered']}")

        #array to hold the values of the players hand(s)
        hand_values = []
        hand_values.append(evaluate_deal(list(player_cards[0])))
        dealer_val = evaluate_deal(list(dealer_cards))

        if hand_values[0] == 21 and dealer_val == 21:
            print(f'You have 21, but the dealer also has 21: {dealer_cards}')
            print("Wow, two natural blackjacks!")
            print(f'This is a push, there are no winners')
            continue
        elif hand_values[0] == 21 and dealer_val != 21:
            print(f'You have 21! A natural blackjack! The dealer has {dealer_cards} You win!')
            balance = balance + bet[0]
            print(f"You win {bet[0]}")
            continue
        else:

            all_hands_played = False
            hands = 0
            splitcount = 0
            while not all_hands_played:
                is_hand_over = False
                while not is_hand_over:
                    split_result = await splithand(player_cards, player_cards[hands], hands, splitcount, bet)
                    bet = split_result[2]
                    player_cards = split_result[0]
                    splitcount = split_result[1]
                    print(f'Your current hand (No. {hands+1}) is {player_cards[hands]}')
                    action = await get_action()
                    if action == "hit":
                        player_cards[hands].append(get_cards(deck, 1)[0][0])
                        hand_val = evaluate_deal(list(player_cards[hands]))
                        print(player_cards[hands])
                        if hand_val == 21:
                            print(f"You have 21! {player_cards[hands]}!...moving on...")
                            is_hand_over = True
                        elif hand_val > 21:
                            print(f"You bust with: {player_cards[hands]}! This hand is over with a total of {hand_val}.")
                            is_hand_over = True
                        else:
                            print(f"You have: {player_cards[hands]} with a total of {hand_val}.")
                    if action == "stand":
                        hand_val = evaluate_deal(list(player_cards[hands]))
                        print(f"You have: {player_cards[hands]} with a total of {hand_val}")
                        is_hand_over = True
                hands += 1
                if hands > len(player_cards)-1:
                    all_hands_played = True

            have_all_busted = True
            for hands in range(0,len(player_cards)):
                if evaluate_deal(list(player_cards[hands])) <= 21:
                    have_all_busted = False
            total_loss = 0
            if have_all_busted:
                for buck in bet:
                    total_loss = total_loss + buck
                    balance = balance - buck
                    print(f"You have lost ${total_loss}! Your remaining balance is {balance}")
                continue_with_deck = await get_continue()
                if continue_with_deck == "no":
                    iteration = 0
                continue

            print("Now the dealer will reveal, and draw")
            print(f"The dealer's hand is: {dealer_cards}")

            while dealer_val < 17:
                new_card = get_cards(deck, 1)[0][0]
                dealer_cards.append(new_card)
                print(f"The dealer draws a card: {dealer_cards}")
                dealer_val = evaluate_deal(list(dealer_cards))
                print(f"The dealer's total is: {dealer_val}")

            print(f"The dealer's hand stops with a score of {dealer_val}")

            # evaluating winners of the hands
            for hands in range(0, len(player_cards)):
                hand_val = evaluate_deal(list(player_cards[hands]))
                if hand_val > dealer_val and hand_val < 21 :
                    print(f"Your hand (No. {hands+1}): {hand_val} with a score of {hand_val} beats the dealer's {dealer_val}!")
                    balance = balance + bet[hands]
                    print(f"You win {bet[hands]}")
                elif hand_val == dealer_val:
                    print(f"Your hand (No. {hands+1}): {hand_val} with a score of {hand_val} ties the dealer's {dealer_val}!")
                    print("No bet is awarded")
                elif dealer_val > 21:
                    print(f"The dealer is over the max with {dealer_val}, your hand: {player_cards[hands]} wins!")
                    print(f"You win ${bet[hands]}")
                    balance = balance + bet[hands]
                else:
                    print(f"Your Hand (No. {hands+1}): {hand_val} with a score of {hand_val} loses!")
                    print(f"You lose ${bet[hands]}")
                    balance = balance - bet[hands]
        print(f"Your balance is ${balance}")
        play = await get_play()				# replay mechanic
        length_of_deck = len(deck)
        if play == "yes" and length_of_deck <25:
            print("The length of the deck is currently halved, the deck will be restocked and reshuffled")
        elif play == "yes" and length_of_deck >25:
            continue_with_deck = await get_continue()
            if continue_with_deck == "no":
                iteration = 0
                continue
    print("Thanks for playing!")


if __name__ == "__main__":
    await play_blackjack()

