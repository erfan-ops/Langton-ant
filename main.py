import ant_game


if __name__ == "__main__":
    game = ant_game.AntGame(pixel_size=30, grid_line_color=0, background_color=0x262428, ant_color=0xfdfbff)
    game.run()