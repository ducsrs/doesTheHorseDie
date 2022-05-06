import chess, chess.pgn
import io

horse_logo = (r'''
        ,....,
      ,::::::<
     ,::/^\"``.
    ,::/, `   e`.
   ,::; |        '.
   ,::|  \___,-.  c)
   ;::|     \   '-'
   ;::|      \
   ;::|   _.=`\
   `;:|.=` _.=`\
     '|_.=`   __\
     `\_..==`` /
      .'.___.-'.
     /          \
jgs ('--......--')
    /'--......--'\
    `"--......--"`''')
kasparov_pgn = ('[Event "Match"]\n'
                '[Site "Philadelphia, PA USA"]\n'
                '[Date "1996.02.10"]\n'
                '[Round "1"]\n'
                '[White "Deep Blue (Computer)"]\n'
                '[Black "Garry Kasparov"]\n'
                '[Result "1-0"]\n'
                '[ECO "B22"]\n'
                '[PlyCount "73"]\n'
                '[EventDate "1996.??.??"]\n'
                '[WhiteElo ""]\n'
                '[BlackElo ""]\n'
                '\n'
                '1. e4 c5 {Garry chooses his favorite move against 1.e4 which served him\n'
                'throughout his career.} 2. c3 {The computer avoids the main-line and plays the\n'
                'Alapin(c3) Sicilian.} 2... d5 3. exd5 Qxd5 4. d4 Nf6 5. Nf3 Bg4 6. Be2 e6 7. h3\n'
                'Bh5 8. O-O Nc6 9. Be3 cxd4 10. cxd4 Bb4 {A somewhat rare move.} (10... Be7 {This\n'
                'is the most popular move in this position.} 11. Nc3 Qd6) 11. a3 Ba5 12. Nc3 Qd6\n'
                '13. Nb5 Qe7 14. Ne5 Bxe2 15. Qxe2 O-O 16. Rac1 Rac8 {Both sides have completed\n'
                'development and have activated their pieces. White has an isolated pawn and will\n'
                'have to play actively to justify this slight weakness.} 17. Bg5 Bb6 18. Bxf6\n'
                'gxf6 19. Nc4 Rfd8 20. Nxb6 axb6 21. Rfd1 f5 22. Qe3 {White activates the queen\n'
                'and threatens to invade on the kingside.} 22... Qf6 23. d5 Rxd5 24. Rxd5 exd5\n'
                '25. b3 Kh8 26. Qxb6 Rg8 {In order to compensate for the damaged king\'s position\n'
                'Black works on organizing an attack.} 27. Qc5 d4? (27... f4 {This move keeps the\n'
                'positon balanced.}) 28. Nd6! f4 29. Nxb7 Ne5 30. Qd5 f3 31. g3 Nd3 32. Rc7\n'
                '{White\'s pieces are working together and starting to penetrate into Black\'s\n'
                'position.} 32... Re8?? {The fatal mistake by the world champion.} 33. Nd6 Re1+\n'
                '34. Kh2 Nxf2 35. Nxf7+ Kg7 36. Ng5+ Kh6 37. Rxh7+ {This is the first time a\n'
                'chess computer defeated a current world champion in classical time controls. A\n'
                'huge moment in chess history!} 1-0')
morphy_pgn = ('[Event "Paul Morphy - Duke Karl Count Isouard (1858.??.??)"]\n'
              '[Site "Paris (France)"]\n'
              '[Date "1858.??.??"]\n'
              '[Round "?"]\n'
              '[White "Paul Morphy"]\n'
              '[Black "Duke of Brunswick and Count Isouard"]\n'
              '[Result "1-0"]\n'
              '\n'
              '1. e4 e5 2. Nf3 d6 3. d4 Bg4 4. dxe5 Bxf3 5. Qxf3 dxe5 6. Bc4 Nf6 7. Qb3 Qe7 8.\n'
              'Nc3 c6 9. Bg5 b5 10. Nxb5 cxb5 11. Bxb5+ Nbd7 12. O-O-O Rd8 13. Rxd7 Rxd7 14.\n'
              'Rd1 Qe6 15. Bxd7+ Nxd7 16. Qb8+ Nxb8 17. Rd8# 1-0')

# TODO: Scrape https://www.chess.com/article/view/the-best-chess-games-of-all-time to fill in 10 gallery games
# TODO: Split gallery into its own file
gallery = [
    {
        'name': "Kasparov v. Deep Blue (1996)",
        'pgn': kasparov_pgn
    },
    {
        'name': "Morphy v. Allies (1858)",
        'pgn': morphy_pgn
    },
    {
        'name': "Scholar's Mate",
        'pgn': '1.e4 e5 2.Bc4 Nc6 3.Qh5 Nf6?? 4.Qxf7#'
    }
]
piece_names = [0, 'a pawn', 'another horse', 'a bishop',
               'a rook', 'the queen', 'the king']

def show_gallery():
    n = 1
    for game_dict in gallery:
        print(f"{n}. {game_dict['name']}")
        n += 1

def captured_knight(board, move):
    try:
        # print(board.piece_at(move.to_square).piece_type)
        if board.piece_at(move.to_square).piece_type == chess.KNIGHT:
            # print(board)
            return board.piece_at(move.to_square).color
        return None
    except AttributeError:
        return None


# game = chess.pgn.read_game(
#     io.StringIO(kasparov_pgn))
def report(game: chess.pgn.Game):

    board = game.board()
    deaths = [
        # {
        #     'color': 'white',
        #     'on_turn': 0,
        #     'taken_by': 1,
        # }
    ]
    move_count = 1
    # even counts are black moves, odd are white
    moves = [node for node in game.mainline_moves()]
    # print(moves)
    board.push(moves[0])

    for move in moves[1:]:
        move_count += 1
        knight_color = captured_knight(board, move)
        # print(knight_color == 0)
        if board.is_capture(move) and knight_color is not None:
            deaths.append({
                'color': 'white' if knight_color else 'black',
                'on_turn': move_count,
                'taken_by': piece_names[board.piece_at(move.from_square).piece_type],
            })
            # print(deaths)
        board.push(move)

    # print(deaths)
    if not deaths:
        print("NO")
        print("No horses are captured in this game.")
    else:
        print("YES")
        for death in deaths:
            print(f"On turn {(death['on_turn'] + 1) // 2}, a {death['color']} horse is captured by {death['taken_by']}.")


print(horse_logo)
print("Does the horse die? v1.0")
request = input("Enter pgn or view [g]allery:\n")
if request.lower() == 'g':
    show_gallery()
    pgn = gallery[int(input('')) - 1]['pgn']
else:
    pgn = request
report(chess.pgn.read_game(
    io.StringIO(pgn)
))

