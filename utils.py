def blit_text_center(win, font, text):
    # render text to screen
    render = font.render(text, 1, (200, 200, 200))
    win.blit(render, (win.get_width() / 2 - render.get_width() /
                      2, win.get_height() / 2 - render.get_height() / 2))