import numpy as np
import matplotlib.pyplot as plt


def play_roulette(bet, win_probability=0.5):
    '''
    Place a bet and either gain an amount equal to that bet or lose it
    
    Args:
        bet: Number of dollars to bet
        win_probability: Probability that you will win
        
    Returns:
        winnings: plus or minus your bet.
    '''
    outcome = 1 if np.random.random()<win_probability else -1
    winnings = bet*outcome
    return winnings


def play_martingale(bankroll, min_bet=5, max_bet=500, win_probability=0.5,verbose=True):
    '''
    Use the Martingale betting system on the roulette game.
    The goal is to win an amount equal to the min_bet, 
    by walking away if you win, or doubling your bet every time you lose.  
    Prints the outcome of your game. 

    Args:
        bankroll: The amount of money you have available to play with
        min_bet: The minimum bet allowed at the table
        max_bet: The maximum bet allowed at the table
        win_probability: Chances of winning a single spin.
        verbose: Whether to print out the outcome of a single spin

    Returns:
        bankroll_log: a list showing how much money you had initially, and after every spin.

    '''
    bankroll_log = [bankroll]
    bet = min_bet
    winnings = 0
    while bankroll>=bet and bet<=max_bet and winnings <= 0:
        winnings = play_roulette(bet,win_probability)
        bankroll = bankroll + winnings
        bankroll_log.append(bankroll)
        bet = bet*2 #double your bet until you win
        if verbose:
            if bet>max_bet:
                outcome = "To make your money back you'd need to bet $%r, which exceeds maximum bet ($%r).  You end up with $%r." %(bet,max_bet,bankroll)
            if bankroll<bet:
                outcome = "You're down to $%r, wich is not enough to make the required bet of $%r." %(bankroll,bet)
            if winnings>0:
                print "Congratulations!  You won $%r!" %winnings
    return bankroll_log


def iterate_martingale(bankroll, target, min_bet=5, max_bet=500, win_probability=0.5, verbose = True):
    '''
    Use the Martingale betting system on the roulette game.
    This time, you don't walk away until you have reached your target amount of winnings.
    Still double your bet every time you lose, but if you win, reset your bet to the min_bet.

    Args:
        bankroll: The amount of money you have available to play with
        target: How much money you want to win
        min_bet: The minimum bet allowed at the table
        max_bet: The maximum bet allowed at the table
        win_probability: Chances of winning a single spin.
        verbose: Whether to print out the outcome of a single spin
    Returns:
        bankroll_log: a list showing how much money you had initially, and after every spin.
    '''

    bankroll_log = [bankroll]
    bet = min_bet
    winnings = 0
    gain = 0
    while bankroll>=bet and bet<=max_bet and gain<target:
        winnings = play_roulette(bet,win_probability)
        bankroll = bankroll + winnings
        bankroll_log.append(bankroll)
        gain = bankroll_log[-1] - bankroll_log[0]

        #double your bet until you win, then reset
        if winnings<0:
            bet = bet*2
        else:
            bet = min_bet
        
        if bet>max_bet:
            outcome = "To make your money back you'd need to bet $%r, which exceeds maximum bet ($%r).  You end up with $%r." %(bet,max_bet,bankroll)
        if bankroll<bet:
            outcome = "You're down to $%r, wich is not enough to make the required bet of $%r." %(bankroll,bet)
        if gain >= target:
            outcome = "Congratulations!  You won $%r!" % gain
            reached_target = 1
        else: reached_target = 0
        
    if verbose:  
        print outcome
        plt.plot(bankroll_log)
        plt.xlabel('Roulette Spins')
        plt.ylabel('Bankroll')
        plt.title('Repeated Martingale, Goal=$%r' % target)
        
    return reached_target


def simulate_martingales(bankroll, target, min_bet=5, max_bet=500, win_probability=0.5):
    '''
    Run 1000 simulations of a given Martingale scenario
    Args:
        bankroll: The amount of money you have available to play with
        target: How much money you want to win
        min_bet: The minimum bet allowed at the table
        max_bet: The maximum bet allowed at the table
        win_probability: Chances of winning a single spin

    Returns:
        win_pct: The percent of the time that you reach your target winnings (rather than losing horribly)
    '''
    wins = 0
    for i in range(1000):
        wins = wins + iterate_martingale(bankroll,target,min_bet,max_bet,win_probability, verbose=False)
    
    win_pct = wins*1.0/1000
    return win_pct


def test_targets(target_list,bankroll, min_bet=5, max_bet=500, win_probability=0.5):
    '''
    Run simulations for a variety of different targets to see how likely you are to hit each target.

    Args:
        target_list: List of target winnings to shoot for
        bankroll: The amount of money you have available to play with
        min_bet: The minimum bet allowed at the table
        max_bet: The maximum bet allowed at the table
        win_probability: Chances of winning a single spin

    Returns: 
        win_pct_list: List of the percent of times you will reach each target
    '''
    win_pct_list = []
    for target in target_list:
        win_pct = simulate_martingales(bankroll, target, min_bet, max_bet, win_probability)
        win_pct_list.append(win_pct)
        
    return win_pct_list
