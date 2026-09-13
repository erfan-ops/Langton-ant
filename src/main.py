import ant_game

if __name__ == "__main__":
    game = ant_game.Game(
        pixel_size=20,
        width=1600,
        height=900,
        grid_line_color=0,
        ant_color=0xc070ff,
        mode="RLLLLLLRRLRR",
        colors=[0x1e1e2e, 0xf5e0dc, 0xf2cdcd, 0xf5c2e7, 0xcba6f7, 0xf38ba8, 0xeba0ac, 0xfab387, 0xf9e2af, 0xa6e3a1, 0x94e2d5, 0x89dceb, 0x74c7ec, 0x89b4fa, 0xb4befe],
        step_interval=0.02
    )
    game.run()
