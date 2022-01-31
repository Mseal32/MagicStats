import dearpygui.dearpygui as dpg
import json
import random

dpg.create_context()
dpg.create_viewport(min_width=500, min_height=500)
dpg.setup_dearpygui()

stat_file = open('stats.json', 'r+')
stat_data = json.loads(open('stats.json').read())


def register(sender):
    values = dpg.get_values(items=['RegPlayer', 'Player List', 'RegDeck'])
    if values[0] != '':
        player_name = values[0]
        data = {
            player_name: {
                "Decks": {
                    values[2]: {
                        "Games Played": 1,
                        "Games Won": 0,
                        "Games Lost": 0
                    }
                }
            }
        }
        stat_data.update(data)
        json.dump(stat_data, open('stats.json', 'w'), indent=2)
    elif values[1] != '':
        player_name = values[1]
        stat_data[player_name]["Decks"].update({values[2]: {"Games Played": 1, "Games Won": 0, "Games Lost": 0}})
        json.dump(stat_data, open('stats.json', 'w'), indent=2)

    dpg.delete_item(dpg.get_item_parent(sender))


def test_list(sender):
    x = dpg.get_value(sender)
    if x == 'Games Played':
        print('Too many!')
    else:
        print('None!')


with dpg.viewport_menu_bar():
    with dpg.menu(label='Decks'):
        dpg.add_menu_item(label='Register Deck', callback=lambda: create_registry())
        dpg.add_menu_item(label='View/Edit Registered Decks', callback=lambda: generate_filter())

    with dpg.menu(label='Visualize Data'):
        dpg.add_menu_item(label='Compare', callback=lambda: generate_compare())

    with dpg.menu(label='Leaderboards'):
        dpg.add_menu_item(label='Best Decks', callback=lambda: dpg.show_item('BestDecks'))
        dpg.add_menu_item(label='Best Players', callback=lambda: dpg.show_item('BestPlayers'))

    with dpg.menu(label='Misc'):
        dpg.add_menu_item(label='Random Deck', callback=lambda: dpg.show_item('Random Deck'))

with dpg.window(label='Top Players', show=False, pos=[500, 200], tag='BestPlayers'):
    dpg.add_text('Top 3 Players:')
    games_played = {}
    games_won = {}
    player_winrate = {}
    game_play = 0
    game_won = 0
    for player in list(stat_data):
        for deck in list(stat_data[player]["Decks"]):
            game_play += stat_data[player]['Decks'][deck]['Games Played']
            game_won += stat_data[player]['Decks'][deck]['Games Won']
        player_winrate.update({player: (game_won / game_play) * 100})
        game_won = 0
        game_play = 0
    sorted_winrate = sorted(player_winrate.items(), key=lambda item: item[1], reverse=True)
    dpg.add_text('Best Player: ', color=[255, 215, 0])
    try:
        with dpg.group(horizontal=True):
            dpg.add_text(sorted_winrate[0][0] + ',')
            dpg.add_text('Winrate: ' + str(sorted_winrate[0][1]) + '%')
    except IndexError:
        dpg.add_text('No Player Found!')
    dpg.add_text('\n')
    dpg.add_text('Second Best: ', color=[196, 174, 173])
    try:
        with dpg.group(horizontal=True):
            dpg.add_text(sorted_winrate[1][0] + ',')
            dpg.add_text('Winrate: ' + str(sorted_winrate[1][1]) + '%')
    except IndexError:
        dpg.add_text('No Player Found!')
    dpg.add_text('\n')
    dpg.add_text('Third Best: ', color=[205, 127, 50])
    try:
        with dpg.group(horizontal=True):
            dpg.add_text(sorted_winrate[2][0] + ',')
            dpg.add_text('Winrate: ' + str(sorted_winrate[2][1]) + '%')
    except IndexError:
        dpg.add_text('No Player Found!')

with dpg.window(label='Best Decks', show=False, width=250, height=135, pos=[500, 200], tag='BestDecks'):
    dpg.add_text('Top 5 Decks:')
    decks = {}
    deck_players = {}
    for player in list(stat_data):
        for deck in list(stat_data[player]["Decks"]):
            try:
                deck_winrate = (stat_data[player]['Decks'][deck]['Games Won'] / stat_data[player]['Decks'][deck]['Games Played']) * 100
            except ZeroDivisionError:
                continue
            decks.update({deck: deck_winrate})
            deck_players.update({deck: player})
    sorted_decks = sorted(decks.items(), key=lambda item: item[1], reverse=True)
    dpg.add_text('Best Deck: ', color=[255, 215, 0])
    try:
        with dpg.group(horizontal=True):
            dpg.add_text(sorted_decks[0][0] + ',')
            with dpg.tooltip(dpg.last_item()):
                dpg.add_text(deck_players[sorted_decks[0][0]] + "'s Deck")
            dpg.add_text('Winrate: ' + str(sorted_decks[0][1]) + '%')
    except IndexError:
        dpg.add_text('No Deck Found!')
    dpg.add_text('\n')
    dpg.add_text('Second Best: ', color=[196, 174, 173])
    try:
        with dpg.group(horizontal=True):
            dpg.add_text(sorted_decks[1][0] + ',')
            with dpg.tooltip(dpg.last_item()):
                dpg.add_text(deck_players[sorted_decks[1][0]] + "'s Deck")
            dpg.add_text('Winrate: ' + str(sorted_decks[1][1]) + '%')
    except IndexError:
        dpg.add_text('No Deck Found!')
    dpg.add_text('\n')
    dpg.add_text('Third Best: ', color=[205, 127, 50])
    try:
        with dpg.group(horizontal=True):
            dpg.add_text(sorted_decks[2][0] + ',')
            with dpg.tooltip(dpg.last_item()):
                dpg.add_text(deck_players[sorted_decks[2][0]] + "'s Deck")
            dpg.add_text('Winrate: ' + str(sorted_decks[2][1]) + '%')
    except IndexError:
        dpg.add_text('No Deck Found!')
    dpg.add_text('\n')
    dpg.add_text('Fourth Best: ', color=[158, 152, 235])
    try:
        with dpg.group(horizontal=True):
            dpg.add_text(sorted_decks[3][0] + ',')
            with dpg.tooltip(dpg.last_item()):
                dpg.add_text(deck_players[sorted_decks[3][0]] + "'s Deck")
            dpg.add_text('Winrate: ' + str(sorted_decks[3][1]) + '%')
    except IndexError:
        dpg.add_text('No Deck Found!')
    dpg.add_text('\n')
    dpg.add_text('Fifth Best: ', color=[211, 211, 211])
    try:
        with dpg.group(horizontal=True):
            dpg.add_text(sorted_decks[4][0] + ',')
            with dpg.tooltip(dpg.last_item()):
                dpg.add_text(deck_players[sorted_decks[4][0]] + "'s Deck")
            dpg.add_text('Winrate: ' + str(sorted_decks[4][1]) + '%')
    except IndexError:
        dpg.add_text('No Deck Found!')

with dpg.window(label='Random Deck', width=250, pos=[300, 150], show=False, tag='Random Deck'):
    player_list = list(stat_data)
    try:
        random_player = random.randint(0, len(player_list) - 1)
        dpg.add_text(player_list[random_player] + "'s Deck:")
        deck_list = list(stat_data[player_list[random_player]]["Decks"])
        random_deck = random.randint(0, len(deck_list) - 1)
        dpg.add_text(deck_list[random_deck], color=[232, 125, 125])
        with dpg.group(horizontal=True):
            dpg.add_text('Deck Win Rate:')
            dpg.add_text(str((stat_data[player_list[random_player]]["Decks"][deck_list[random_deck]]["Games Won"] /
                              stat_data[player_list[random_player]]["Decks"][deck_list[random_deck]]["Games Played"] * 100)) + '%')
        with dpg.group(horizontal=True):
            dpg.add_text('Games Played:')
            dpg.add_text(str(stat_data[player_list[random_player]]["Decks"][deck_list[random_deck]]["Games Played"]))
        with dpg.group(horizontal=True):
            dpg.add_text('Games Won:')
            dpg.add_text(str(stat_data[player_list[random_player]]["Decks"][deck_list[random_deck]]["Games Won"]))
        with dpg.group(horizontal=True):
            dpg.add_text('Games Lost:')
            dpg.add_text(str(stat_data[player_list[random_player]]["Decks"][deck_list[random_deck]]["Games Lost"]))
    except ValueError:
        dpg.add_text('No Registered Deck/Player Found!', color=[232, 125, 125])


def generate_compare():
    win = dpg.add_window(label='Compare Players')
    player_list = list(stat_data)
    num_players = []
    for z in range(0, len(player_list)):
        num_players.append(str(z + 1))
    dpg.add_text('Number of Players:', parent=win)
    combo = dpg.add_combo(items=num_players, parent=win, callback=lambda: compare_num_players(combo, win))


def compare_num_players(sender, parent):
    num_players = int(dpg.get_value(sender))
    combos = []
    for z in range(0, num_players):
        dpg.add_combo(label='Player ' + str(z + 1), items=list(stat_data), parent=parent, tag='Player ' + str(z + 1))
        combos.append(dpg.last_item())
    button = dpg.add_button(label='Compare!', parent=parent, callback=lambda: compare_players(button, num_players, combos))


def compare_players(sender, num_players, combos):
    win = dpg.add_window(label='Comparing Players')
    with dpg.table(parent=win, resizable=True, policy=dpg.mvTable_SizingFixedFit, borders_innerH=True, borders_innerV=True, borders_outerV=True):
        dpg.add_table_column(label='Player Name')
        dpg.add_table_column(label='Overall Winrate')
        dpg.add_table_column(label='Games Played')
        dpg.add_table_column(label='Games Won')
        dpg.add_table_column(label='Games Lost')
        total_games = 0
        games_won = 0
        games_lost = 0

        for player in range(0, num_players):
            player_name = dpg.get_value(combos[player])
            for deck in stat_data[player_name]['Decks']:
                total_games += stat_data[player_name]['Decks'][deck]["Games Played"]
                games_won += stat_data[player_name]['Decks'][deck]["Games Won"]
                games_lost += stat_data[player_name]['Decks'][deck]["Games Lost"]
            with dpg.table_row():
                for column in range(0, 5):
                    if column == 0:
                        dpg.add_text(player_name)
                    if column == 1:
                        winrate = (games_won / total_games) * 100
                        dpg.add_text(str(winrate) + '%')
                        winrate = 0
                    if column == 2:
                        dpg.add_text(str(total_games))
                        total_games = 0
                    if column == 3:
                        dpg.add_text(games_won)
                        games_won = 0
                    if column == 4:
                        dpg.add_text(games_lost)
                        games_lost = 0


def view_stats(sender, value, window):
    global top_deck
    options = dpg.get_value(sender)
    player = stat_data[value]
    deck_list = list(player['Decks'])
    if options == 'View Player Stats':
        total_games = 0
        total_games_won = 0
        total_games_lost = 0
        win = dpg.add_window(label=value + "'s Stats", pos=[500, 300])
        wrap = dpg.get_item_width(win)
        top_deck = {"DeckName": 0}
        for deck in deck_list:
            for key in top_deck:
                name = key
            deck_winrate = player['Decks'][deck]['Games Won'] / player['Decks'][deck]['Games Played']
            if top_deck.keys().__contains__("DeckName"):
                top_deck = {deck: deck_winrate}
            elif deck_winrate > top_deck[key]:
                top_deck = ({deck: deck_winrate})
            else:
                continue
            total_games += player['Decks'][deck]['Games Played']
            total_games_won += player['Decks'][deck]['Games Won']
            total_games_lost += player['Decks'][deck]['Games Lost']
        with dpg.group(parent=win, horizontal=True):
            dpg.add_text('Total Games Played : ', color=[232, 125, 125])
            dpg.add_text(str(total_games))
        with dpg.group(parent=win, horizontal=True):
            dpg.add_text('Total Games Won: ', color=[232, 125, 125])
            dpg.add_text(str(total_games_won))
        with dpg.group(parent=win, horizontal=True):
            dpg.add_text('Total Games Lost: ', color=[232, 125, 125])
            dpg.add_text(str(total_games_lost))
        with dpg.group(parent=win, horizontal=True):
            dpg.add_text('Overall Win Rate: ', color=[232, 125, 125])
            dpg.add_text(str((total_games_won / total_games) * 100) + '%')
        with dpg.group(parent=win, horizontal=True):
            for key in top_deck:
                top_deck_name = key
            dpg.add_text(value + "'s Top Deck:", color=[232, 125, 125])
            dpg.add_text(top_deck_name)
        with dpg.group(parent=win, horizontal=True):
            dpg.add_text('Top Deck Win Rate:', color=[232, 125, 125])
            dpg.add_text(str(top_deck[top_deck_name] * 100) + '%')
    elif options == 'View Decks':
        win = dpg.add_window(label=value + "'s Decks", pos=[500, 300], width=200)
        with dpg.table(parent=win, resizable=True, policy=dpg.mvTable_SizingFixedFit, borders_innerH=True, borders_innerV=True, borders_outerV=True):
            dpg.add_table_column(label='Deck Name')
            dpg.add_table_column(label='Win Rate')
            dpg.add_table_column(label='Games Played')
            dpg.add_table_column(label='Games Won')
            dpg.add_table_column(label='Games Lost')
            for deck in deck_list:
                with dpg.table_row():
                    for column in range(0, 6):
                        deck_winrate = (player['Decks'][deck]['Games Won'] / player['Decks'][deck]['Games Played']) * 100
                        if column == 0:
                            dpg.add_text(deck)
                        if column == 1:
                            dpg.add_text(str(deck_winrate) + '%')
                        if column == 2:
                            dpg.add_text(str(player['Decks'][deck]['Games Played']))
                        if column == 3:
                            dpg.add_text(str(player['Decks'][deck]['Games Won']))
                        if column == 4:
                            dpg.add_text(str(player['Decks'][deck]['Games Won']))

    elif options == 'Edit Stats':
        win = dpg.add_window(label='Editing ' + value + "'s Stats", pos=[500, 300])
        dpg.add_text('Deck: ', parent=win, color=[232, 125, 125])
        current_deck = dpg.add_combo(items=deck_list, parent=win, callback=lambda: show_items(current_deck, value, win))


def delete_deck(sender, player_name, deck_name):
    stat_data[player_name]["Decks"].pop(deck_name)
    json.dump(stat_data, open('stats.json', 'w'), indent=2)
    dpg.delete_item(dpg.get_item_parent(dpg.get_item_parent(sender)))


def show_items(sender, player_name, parent):
    deck = dpg.get_value(sender)
    dpg.add_input_int(parent=parent, default_value=stat_data[player_name]['Decks'][deck]['Games Played'], label='Games Played', tag='Games Played')
    dpg.add_input_int(label='Games Won', default_value=stat_data[player_name]['Decks'][deck]['Games Won'], parent=parent, tag='Games Won')
    dpg.add_input_int(label='Games Lost', default_value=stat_data[player_name]['Decks'][deck]['Games Lost'], parent=parent, tag='Games Lost')
    with dpg.group(parent=parent):
        delete_button = dpg.add_button(label='Delete Deck', callback=lambda: delete_deck(delete_button, player_name, deck))
        button = dpg.add_button(label='Done!', callback=lambda: edit_stats(button, player_name, deck))
    dpg.add_text(deck, before=sender, parent=parent, color=[240, 36, 36])
    dpg.delete_item(sender)


def edit_stats(sender, player_name, deck):
    values = dpg.get_values(items=('Games Played', 'Games Won', 'Games Lost'))
    stat_data[player_name]["Decks"][deck].update({"Games Played": values[0], "Games Won": values[1], "Games Lost": values[2]})
    json.dump(stat_data, open('stats.json', 'w'), indent=2)
    dpg.delete_item(dpg.get_item_parent(sender))


def filter_config(sender, filter_id, filter_string):
    dpg.set_value(filter_id, filter_string)


def filter_handler(sender, appdata):
    player_name = appdata[1]
    win = dpg.add_window(show=True, no_title_bar=True, modal=True, pos=[500, 300], width=300)
    list_box = dpg.add_listbox(items=['View Player Stats', 'View Decks', 'Edit Stats/Delete Decks'], parent=dpg.last_item(), callback=lambda: view_stats(list_box, player_name, win))


with dpg.item_handler_registry() as handler:
    dpg.add_item_clicked_handler(callback=filter_handler)


def generate_filter():
    window = dpg.add_window(label='Registered Players', width=250, pos=[300, 200], on_close=dpg.delete_item)
    name_filter = dpg.add_input_text(parent=window, label='Filter by Name', width=150, callback=lambda: filter_config(name_filter, filter_set, dpg.get_value(name_filter)))
    with dpg.filter_set(parent=window) as filter_set:
        for name in stat_data:
            dpg.add_text(name, filter_key=name, tag=name)
            dpg.bind_item_handler_registry(name, handler)


def checkbox_vis(sender, item):
    if dpg.get_value(sender) is True:
        dpg.show_item(item)
    else:
        dpg.configure_item(item, show=False)


def create_registry():
    window = dpg.add_window(label='Deck Registry', width=300, height=135, pos=[150, 200])
    with dpg.group(horizontal=True, parent=window):
        box0 = dpg.add_checkbox(label='New Player', callback=lambda: checkbox_vis(box0, 'RegPlayer'))
        box1 = dpg.add_checkbox(label='Existing Player', callback=lambda: checkbox_vis(box1, 'Player List'))
    dpg.add_input_text(label='New Player', show=False, tag='RegPlayer', parent=window)
    dpg.add_combo(label='Player List', items=list(stat_data), show=False, tag='Player List', parent=window)
    dpg.add_input_text(label='Deck Name', tag='RegDeck', parent=window)
    dpg.add_button(label='Register!', callback=register, parent=window)


dpg.show_viewport()
dpg.start_dearpygui()
dpg.destroy_context()
