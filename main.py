import ant_game


if __name__ == "__main__":
    game = ant_game.AntGame(
        pixel_size=20,
        width=800,
        height=800,
        grid_line_color=0,
        ant_color=0xc070ff,
        mode="LRRRRRLLR",
        colors=[0x14012a, 0x542809, 0xffe999],
        step_interval=1
    )
    game.run()