import ant_game


if __name__ == "__main__":
    game = ant_game.AntGame(
        pixel_size=20,
        width=800,
        height=800,
        grid_line_color=0,
        background_color=0x262428,
        ant_color=0xc070ff,
        on_block_color=0xfdfbff
    )
    game.run()