# -*- coding: utf-8 -*-
# КОСМИЧЕСКОЕ ПРИКЛЮЧЕНИЕ – с перехватом main_menu

init python:
    # Настройки экрана
    config.screen_width = 1920
    config.screen_height = 1080
    config.window_title = "Космическое Приключение"

    config.has_autosave = False
    config.autosave_on_quit = False

    import random
    import time
    import pygame

    # ========== КЛАСС МЕТЕОРИТОВ ==========
    class FireballCollector:
        def __init__(self):
            self.fireballs = []
            self.collected = 0
            self.total = 10
            self.time_limit = 30
            self.start_time = None
            self.game_active = True

        def start_game(self, level):
            self.fireballs = []
            self.collected = 0
            self.game_active = True
            self.start_time = time.monotonic()

            if level == 1:
                self.total = 10
                self.time_limit = 30
            elif level == 2:
                self.total = 14
                self.time_limit = 25
            elif level == 3:
                self.total = 18
                self.time_limit = 20
            elif level == 4:
                self.total = 22
                self.time_limit = 15
            else:
                self.total = 26
                self.time_limit = 10

            for i in range(self.total):
                x = random.randint(200, 1720)
                y = random.randint(200, 800)
                self.fireballs.append({
                    'x': x,
                    'y': y,
                    'active': True,
                    'id': i,
                    'scale': 0.15 + random.uniform(-0.02, 0.02)
                })

        def get_remaining_time(self):
            if self.start_time is None:
                return self.time_limit
            elapsed = time.monotonic() - self.start_time
            remaining = max(0, self.time_limit - elapsed)
            if remaining <= 0 and self.game_active:
                self.game_active = False
            return remaining

        def on_mouse_up(self):
            if not self.game_active:
                return
            x, y = renpy.get_mouse_pos()
            for ball in self.fireballs:
                if not ball['active']:
                    continue
                distance = ((ball['x'] - x) ** 2 + (ball['y'] - y) ** 2) ** 0.5
                if distance < 70:
                    ball['active'] = False
                    self.collected += 1
                    if persistent.sfx_on:
                        renpy.play("audio/fireball_collect.wav", channel="sound")
                    if self.collected >= self.total:
                        self.game_active = False
                    renpy.restart_interaction()
                    break

    def fireball_rotate_function(trans, st, at):
        trans.rotate = (trans.rotate or 0) + 2
        if trans.rotate >= 360:
            trans.rotate = 0
        return 0.016

    def pause_key_handler():
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE]:
            if not renpy.get_screen("pause_menu"):
                renpy.call_screen("pause_menu")
            return True
        return False

    config.overlay_functions.append(pause_key_handler)
    config.autosave_slots = 1
    config.autosave_frequency = 300

# === ПЕРСОНАЖИ ===
define narrator = Character(None, what_color="#FFFFFF", what_size=28, what_outlines=[(1, "#000000", 0, 0)])
define v = Character("Ветрячок", color="#FF6B6B", what_color="#FFFFFF")
define k = Character("Кула", color="#4ECDC4", what_color="#FFFFFF")
define l = Character("Лизун", color="#45B7D1", what_color="#FFFFFF")
define p = Character("Пружинка", color="#FFBE0B", what_color="#FFFFFF")

# === ИЗОБРАЖЕНИЯ ===
image bg космос:
    "images/космос.png"
    zoom 5.0
    xalign 0.5
    yalign 0.5
image bg станция:
    "images/станция.png"
    zoom 5.0
    xalign 0.5
    yalign 0.5
image bg черный = "#000000"

image planet луна:
    "images/луна.png"
    zoom 3.0
    xalign 0.5
    yalign 0.5
image planet марс:
    "images/марс.png"
    zoom 3.0
    xalign 0.5
    yalign 0.5
image planet юпитер:
    "images/Юпитер.png"
    zoom 3.0
    xalign 0.5
    yalign 0.5
image planet сатурн:
    "images/Сатурн.png"
    zoom 3.0
    xalign 0.5
    yalign 0.5
image planet меркурий:
    "images/Меркурий.png"
    zoom 3.0
    xalign 0.5
    yalign 0.5

image ракета:
    "images/ветрячок братья.png"
    zoom 0.1
    xalign 0.5
    yalign 0.5

image crystal red:
    "images/crystal_red.png"
    zoom 0.5
image crystal blue:
    "images/crystal_blue.png"
    zoom 0.5
image crystal green:
    "images/crystal_green.png"
    zoom 0.5
image fireball:
    "images/fireball.png"
    zoom 0.15

image персонаж1:
    "images/ветрячок братья.png"
    zoom 0.25
image персонаж2:
    "images/Кула.png"
    zoom 0.25
image персонаж3:
    "images/Лизун.png"
    zoom 0.25
image персонаж4:
    "images/Пружинка.png"
    zoom 0.25

image heart_full = "images/heart.png"
image heart_empty:
    "images/heart.png"
    matrixcolor InvertMatrix(0.5)*SaturationMatrix(0.0)

# === ТРАНСФОРМЫ ===
transform char_left:
    xalign 0.15
    yalign 0.85
    zoom 0.25
transform char_right:
    xalign 0.85
    yalign 0.85
    zoom 0.25
transform char_center:
    xalign 0.5
    yalign 0.85
    zoom 0.25
transform char_left2:
    xalign 0.25
    yalign 0.85
    zoom 0.25
transform char_right2:
    xalign 0.75
    yalign 0.85
    zoom 0.25
transform planet_top:
    xalign 0.5
    yalign 0.2
    zoom 0.8

transform hop:
    linear 0.1 yoffset -20
    linear 0.1 yoffset 0
transform shake:
    linear 0.05 xoffset -10
    linear 0.05 xoffset 10
    linear 0.05 xoffset 0
transform fireball_rotate:
    rotate 0
    linear 2.0 rotate 360
    repeat

# === АУДИО ===
define audio.space_theme = "audio/space_theme.mp3"
define audio.mystery = "audio/mystery.mp3"
define audio.adventure = "audio/adventure.mp3"
define audio.epic = "audio/epic.mp3"

define audio.click = "audio/click.wav"
define audio.crystal_collect = "audio/crystal_collect.wav"
define audio.map_found = "audio/map_found.wav"
define audio.energy = "audio/energy_recharge.wav"
define audio.success = "audio/success.wav"
define audio.failure = "audio/failure.wav"
define audio.fireball_collect = "audio/energy.wav"

# === ПЕРЕМЕННЫЕ ИГРЫ ===
default lives = 3
default max_lives = 3
default crystals = 0
default level = 1
default energy = 100
default moon_complete = False
default mars_complete = False
default jupiter_complete = False
default saturn_complete = False
default mercury_complete = False
default game_completed = False
default total_score = 0
default fireball_game = None
default fireball_power = False

default persistent.music_on = True
default persistent.sfx_on = True

# === ЭКРАНЫ ИНТЕРФЕЙСА ===
screen game_ui():
    vbox:
        xalign 0.02
        yalign 0.02
        spacing 10
        hbox:
            spacing 5
            for i in range(max_lives):
                if i < lives:
                    add "heart_full":
                        size (60, 60)
                else:
                    add "heart_empty":
                        size (60, 60)
    vbox:
        xalign 0.98
        yalign 0.02
        spacing 5
        text "Кристаллы: [crystals]" size 36 color "#FFFFFF" outlines [(2, "#000000", 0, 0)] xalign 1.0
        text "Уровень: [level]" size 30 color "#FFFFFF" outlines [(2, "#000000", 0, 0)] xalign 1.0
        text "Энергия: [energy]%" size 30:
            if energy > 50:
                color "#00FF00"
            elif energy > 20:
                color "#FFFF00"
            else:
                color "#FF0000"
            outlines [(2, "#000000", 0, 0)] xalign 1.0
    vbox:
        xalign 0.02
        yalign 0.15
        spacing 5
        if persistent.music_on:
            textbutton "Музыка: Вкл" action [SetVariable("persistent.music_on", False), SetMute("music", True)]
        else:
            textbutton "Музыка: Выкл" action [SetVariable("persistent.music_on", True), SetMute("music", False)]
        if persistent.sfx_on:
            textbutton "Звуки: Вкл" action [SetVariable("persistent.sfx_on", False), SetMute("sound", True)]
        else:
            textbutton "Звуки: Выкл" action [SetVariable("persistent.sfx_on", True), SetMute("sound", False)]

screen pause_menu():
    modal True
    frame:
        xalign 0.5
        yalign 0.5
        xpadding 50
        ypadding 50
        background "#000000AA"
        vbox:
            spacing 20
            xalign 0.5
            yalign 0.5
            text "ПАУЗА" size 50 color "#FFFFFF" xalign 0.5
            null height 20
            text "Громкость музыки:" size 30 color "#FFFFFF" xalign 0.5
            bar value Preference("music volume") xalign 0.5 xmaximum 300
            text "Громкость звуков:" size 30 color "#FFFFFF" xalign 0.5
            bar value Preference("sound volume") xalign 0.5 xmaximum 300
            null height 20
            textbutton "Продолжить" action [Play("sound", "audio/click.wav"), Return()] xalign 0.5
            textbutton "Главное меню" action [Play("sound", "audio/click.wav"), MainMenu()] xalign 0.5
            textbutton "Выйти" action [Play("sound", "audio/click.wav"), Quit()] xalign 0.5

# === ЭКРАН ИГРЫ МЕТЕОРИТОВ ===
screen fireball_collector_screen(game, level):
    modal True
    key "dismiss" action [Function(game.on_mouse_up), RenpyRestartInteraction()]
    timer 0.05 repeat True action RenpyRestartInteraction()
    if game.collected >= game.total:
        timer 0.01 action Return("success")
    elif game.get_remaining_time() <= 0:
        timer 0.01 action Return("timeout")
    for ball in game.fireballs:
        if ball['active']:
            imagebutton:
                idle "fireball"
                hover "fireball"
                anchor (0.5, 0.5)
                pos (ball['x'], ball['y'])
                at fireball_rotate
                action [Function(game.on_mouse_up), RenpyRestartInteraction()]
    vbox:
        xalign 0.5
        yalign 0.05
        spacing 10
        text "{color=#FF9900}{size=50}ПОЯС МЕТЕОРИТОВ!{/size}{/color}" outlines [(4, "#000000", 0, 0)] xalign 0.5
        text "{size=36}Разбито: [game.collected]/[game.total]{/size}" color "#FF5500" outlines [(2, "#000000", 0, 0)] xalign 0.5
        text "{size=32}Зона опасности [level] / 5{/size}" color "#FFFF00" outlines [(2, "#000000", 0, 0)] xalign 0.5
        $ time_left = int(game.get_remaining_time())
        text "{size=32}Время до столкновения: [time_left] сек{/size}":
            if time_left > 10:
                color "#00FF00"
            elif time_left > 5:
                color "#FFFF00"
            else:
                color "#FF0000"
            outlines [(2, "#000000", 0, 0)] xalign 0.5
    vbox:
        xalign 0.5
        yalign 0.95
        text "{size=24}Быстро взрывайте метеориты кликами мыши!{/size}" color "#FFFFFF" outlines [(2, "#000000", 0, 0)] xalign 0.5
    textbutton "Отступить":
        xalign 0.02
        yalign 0.98
        action [Play("sound", "audio/click.wav"), Return("exit")]

# === НАЧАЛЬНАЯ ЗАСТАВКА ===
screen start_splash():
    modal True
    add "#000000"
    vbox:
        xalign 0.5
        yalign 0.5
        spacing 30
        text "{size=100}КОСМИЧЕСКОЕ{/size}" color "#FFFFFF" xalign 0.5
        text "{size=80}ПРИКЛЮЧЕНИЕ{/size}" color "#4ECDC4" xalign 0.5
        null height 50
        text "{size=30}Авторский проект Ren'Py{/size}" color "#FFFFFF" xalign 0.5
    textbutton "НАЧАТЬ ИГРУ":
        xalign 0.5
        yalign 0.85
        # Кнопка закрывает экран – управление вернётся в label main_menu
        action [Play("sound", "audio/click.wav"), Return()]

# === ЭКРАН НАСТРОЙКИ ЗВУКА ===
screen sound_settings():
    modal True
    frame:
        xalign 0.5
        yalign 0.5
        xpadding 50
        ypadding 50
        background "#000000AA"
        vbox:
            spacing 20
            xalign 0.5
            yalign 0.5
            text "НАСТРОЙКИ ЗВУКА" size 40 color "#FFFFFF" xalign 0.5
            null height 20
            text "Музыка:" size 30 color "#FFFFFF" xalign 0.5
            bar value Preference("music volume") xalign 0.5 xmaximum 400
            text "Звуки:" size 30 color "#FFFFFF" xalign 0.5
            bar value Preference("sound volume") xalign 0.5 xmaximum 400
            null height 20
            textbutton "Тест музыки" action Play("music", "audio/space_theme.mp3") xalign 0.5
            textbutton "Тест звуков" action Play("sound", "audio/click.wav") xalign 0.5
            null height 20
            textbutton "Сохранить" action Return() xalign 0.5

# === ПЕРЕХВАТ ГЛАВНОГО МЕНЮ – ЗАСТАВКА ВМЕСТО СТАНДАРТНОГО МЕНЮ ===
label main_menu:
    # Скрываем интерфейс (по желанию)
    $ quick_menu = False
    # Показываем заставку
    call screen start_splash
    # После закрытия экрана включаем интерфейс и переходим в игру
    $ quick_menu = True
    jump start

# === НАСТРОЙКИ ЗВУКА ПРИ СТАРТЕ ===
label before_main_menu:
    python:
        if not hasattr(persistent, 'music_on'):
            persistent.music_on = True
        if not hasattr(persistent, 'sfx_on'):
            persistent.sfx_on = True
        if not persistent.music_on:
            renpy.music.set_volume(0.0, channel='music')
        if not persistent.sfx_on:
            renpy.sound.set_volume(0.0, channel='sound')
    return

# === НАЧАЛО ИГРЫ (ЗАСТАВКА УЖЕ ПОКАЗАНА, НАЧИНАЕМ С ДИАЛОГОВ) ===
label start:
    $ lives = 3
    $ max_lives = 3
    $ crystals = 0
    $ level = 1
    $ energy = 100
    $ moon_complete = False
    $ mars_complete = False
    $ jupiter_complete = False
    $ saturn_complete = False
    $ mercury_complete = False
    $ game_completed = False
    $ total_score = 0
    $ fireball_power = False

    python:
        if not hasattr(persistent, 'music_on'):
            persistent.music_on = True
        if not hasattr(persistent, 'sfx_on'):
            persistent.sfx_on = True
        if persistent.music_on:
            renpy.music.set_volume(0.8, channel='music')
        else:
            renpy.music.set_volume(0.0, channel='music')
        if persistent.sfx_on:
            renpy.sound.set_volume(0.7, channel='sound')
        else:
            renpy.sound.set_volume(0.0, channel='sound')

    if persistent.music_on:
        play music "audio/space_theme.mp3" fadein 2.0 loop

    scene bg космос
    with fade
    show персонаж1 at char_left
    show персонаж2 at char_right
    with dissolve
    play sound "audio/click.wav"

    v "Привет! Я Ветрячок!"
    k "А я Кула! Мы рады видеть тебя на борту нашего корабля!"

    show персонаж3 at char_left2
    show персонаж4 at char_right2
    with dissolve

    l "Приветствую! Я Лизун."
    p "А я Пружинка! Мы отправимся в удивительное космическое путешествие!"

    v "Наша миссия - исследовать планеты и собирать кристаллы."
    k "У тебя есть [lives] жизни. Береги их!"
    l "Собирай кристаллы, проходи уровни и становись космическим героем!"
    p "Нажми ПРОБЕЛ для паузы. Удачи!"

    show screen game_ui
    jump level_select

# === МЕНЮ ВЫБОРА ПЛАНЕТ (ПЕРЕИМЕНОВАНО В level_select) ===
label level_select:
    scene bg космос
    show screen game_ui
    show персонаж1 at char_center
    v "Куда отправимся?"

    $ moon_text = "Луна (Пояс метеоритов)" + (" [✔]" if moon_complete else "")
    $ mars_text = "Марс (Космические загадки)" + (" [✔]" if mars_complete else "")
    $ jupiter_text = "Юпитер (Лабиринт энергии)" + (" [✔]" if jupiter_complete else "")
    $ saturn_text = "Сатурн" + (" [✔]" if saturn_complete else "")
    $ mercury_text = "Меркурий" + (" [✔]" if mercury_complete else "")

    menu:
        "[moon_text]":
            play sound "audio/click.wav"
            jump moon_mission
        "[mars_text]" if moon_complete:
            play sound "audio/click.wav"
            jump mars_mission
        "[jupiter_text]" if mars_complete:
            play sound "audio/click.wav"
            jump jupiter_mission
        "[saturn_text]" if jupiter_complete:
            play sound "audio/click.wav"
            jump saturn_mission
        "[mercury_text]" if saturn_complete:
            play sound "audio/click.wav"
            jump mercury_mission
        "Космическая станция":
            play sound "audio/click.wav"
            jump space_station
        "Показать статистику":
            play sound "audio/click.wav"
            call show_stats
        "Выход":
            play sound "audio/click.wav"
            jump end_game

# ---------- МИССИЯ ЛУНА ----------
label moon_mission:
    if persistent.music_on:
        stop music fadeout 1.0
        play music "audio/mystery.mp3" fadein 1.0 loop
    scene bg космос
    show planet луна at planet_top
    show персонаж3 at char_center
    l "Впереди опасный пояс метеоритов! ☄"
    l "Нам нужно расчистить путь и перелететь через это поле, иначе мы не пройдем дальше!"
    l "Быстро разбивай метеориты кликами. Впереди 5 сложных зон!"
    $ level = 1
    jump moon_loop

label moon_loop:
    call play_fireball_collector
    $ mission_result = _return
    if mission_result == "win_all":
        $ moon_complete = True
        play sound "audio/success.wav"
        show text "{size=60}{color=#00FF00}✔ ПОЛЕ МЕТЕОРИТОВ ПРЕОДОЛЕНО!{/color}{/size}" at truecenter with dissolve
        pause 2.5
        hide text with dissolve
        "Ура! Мы успешно прорвались сквозь огненные метеориты и можем лететь на Марс!"
        jump moon_end
    elif mission_result == "continue":
        "Зона очищена! Летим глубже в метеоритное поле!"
        jump moon_loop
    elif mission_result == "retry":
        if lives > 0:
            "Попробуем стабилизировать корабль и повторить попытку!"
            jump moon_loop
        else:
            "Корабль слишком поврежден метеоритами! Зайдем сюда позже."
            jump moon_end
    elif mission_result == "exit":
        "Вы вышли из миссии."
        jump moon_end
    elif mission_result == "game_over":
        "Миссия провалена! У вас закончились жизни."
        jump moon_end
    else:
        "Вы проиграли."
        jump moon_end

label moon_end:
    if persistent.music_on:
        stop music fadeout 1.0
        play music "audio/space_theme.mp3" fadein 1.0 loop
    jump level_select

# ---------- КОНТРОЛЛЕР МИНИ-ИГРЫ ----------
label play_fireball_collector:
    python:
        fireball_game = FireballCollector()
        fireball_game.start_game(level)
    call screen fireball_collector_screen(fireball_game, level)
    $ result = _return
    if result == "success":
        if persistent.sfx_on:
            play sound "audio/success.wav"
        $ fireball_bonus = fireball_game.collected * 20
        $ crystals += fireball_bonus
        $ level += 1
        $ total_score += fireball_bonus
        if fireball_game.collected == fireball_game.total:
            $ perfect_bonus = 100
            $ crystals += perfect_bonus
            $ total_score += perfect_bonus
            show text "{size=60}{color=#FFD700}ИДЕАЛЬНО!{/color}{/size}\n{size=40}Все метеориты уничтожены!{/size}" at truecenter with dissolve
            pause 1.5
            hide text with dissolve
        "Поздравляем! Вы очистили зону! Уничтожено: [fireball_game.collected] метеоритов."
        "Получено [fireball_bonus] кристаллов!"
        if level > 5:
            return "win_all"
        else:
            return "continue"
    elif result == "timeout":
        if persistent.sfx_on:
            play sound "audio/failure.wav"
        $ lives -= 1
        $ energy = max(0, energy - 20)
        "Метеорит врезался в корабль! Время вышло."
        if fireball_game.collected >= fireball_game.total * 0.7:
            "Время вышло, но вы расчистили больше 70% пути!"
            if lives <= 0:
                return "game_over"
            else:
                "Осталось жизней: [lives]. Попробуем еще раз!"
                return "retry"
        else:
            "Время вышло! Вы пропустили слишком много метеоритов."
            if lives <= 0:
                return "game_over"
            else:
                "Осталось жизней: [lives]. Попробуйте еще раз!"
                return "retry"
    elif result == "exit":
        return "exit"
    return "exit"

# ---------- МАРС ----------
label play_puzzle_game:
    $ puzzle_score = 0
    scene bg космос
    show planet марс at planet_top
    show персонаж2 at char_left
    show персонаж3 at char_right
    if energy < 10:
        k "Недостаточно энергии для этой миссии! Восстановите энергию на станции."
        return False
    $ energy -= 10
    k "Привет! Я подготовил для тебя космические загадки!"
    l "Ответь правильно на 3 из 5 вопросов, чтобы получить награду!"
    "Вопрос 1: Какая планета известна своими кольцами?"
    menu:
        "Марс":
            "Неправильно! У Марса нет таких колец."
            play sound "audio/failure.wav"
        "Сатурн":
            "Правильно! Сатурн имеет самые красивые кольца."
            play sound "audio/success.wav"
            $ puzzle_score += 1
        "Юпитер":
            "Юпитер тоже имеет кольца, но они не так заметны."
            play sound "audio/failure.wav"
    "Вопрос 2: Как называется natürlicher спутник Земли?"
    menu:
        "Марс":
            "Марс - это другая планета!"
            play sound "audio/failure.wav"
        "Солнце":
            "Солнце - это звезда!"
            play sound "audio/failure.wav"
        "Луна":
            "Верно! Луна - спутник Земли."
            play sound "audio/success.wav"
            $ puzzle_score += 1
    "Вопрос 3: Какая планета самая большая в Солнечной системе?"
    menu:
        "Земля":
            "Земля не самая большая."
            play sound "audio/failure.wav"
        "Юпитер":
            "Правильно! Юпитер - гигант!"
            play sound "audio/success.wav"
            $ puzzle_score += 1
        "Сатурн":
            "Сатурн большой, но не самый."
            play sound "audio/failure.wav"
    "Вопрос 4: Как называется красная планета?"
    menu:
        "Марс":
            "Да! Марс называют красной планетой."
            play sound "audio/success.wav"
            $ puzzle_score += 1
        "Венера":
            "Венера - утренняя звезда."
            play sound "audio/failure.wav"
        "Юпитер":
            "Юпитер - газовый гигант."
            play sound "audio/failure.wav"
    "Вопрос 5: Что такое астероид?"
    menu:
        "Маленькая звезда":
            "Не совсем."
            play sound "audio/failure.wav"
        "Каменный объект в космосе":
            "Правильно! Астероид - это каменное тело."
            play sound "audio/success.wav"
            $ puzzle_score += 1
        "Облако газа":
            "Это туманность."
            play sound "audio/failure.wav"
    if puzzle_score >= 3:
        play sound "audio/success.wav"
        $ crystals += 100
        $ level += 1
        $ mars_complete = True
        $ total_score += 100
        "Отлично! Вы ответили правильно на [puzzle_score] из 5 вопросов!"
        "Получено 100 кристаллов!"
        "Уровень повышен до [level]!"
        return True
    else:
        play sound "audio/failure.wav"
        $ lives -= 1
        $ energy = max(0, energy - 10)
        "К сожалению, только [puzzle_score] правильных ответов."
        if lives <= 0:
            "Игра окончена!"
            return False
        else:
            "Осталось жизней: [lives]"
            return False

label mars_mission:
    if persistent.music_on:
        stop music fadeout 1.0
        play music "audio/adventure.mp3" fadein 1.0 loop
    scene bg космос
    show planet марс at planet_top
    show персонаж2 at char_center
    k "Добро пожаловать на Марс!"
    k "Проверим твои знания о космосе."
    k "Ответь на вопросы правильно!"
    call play_puzzle_game
    if _return:
        "Марсианская миссия завершена!"
    else:
        "В следующий раз повезет больше!"
    if persistent.music_on:
        stop music fadeout 1.0
        play music "audio/space_theme.mp3" fadein 1.0 loop
    if lives <= 0:
        jump end_game
    else:
        jump level_select

# ---------- ЮПИТЕР ----------
label play_energy_game:
    $ energy_collected = 0
    scene bg космос
    show planet юпитер at planet_top
    show персонаж1 at char_left
    show персонаж4 at char_right
    if energy < 15:
        v "Недостаточно энергии для этой миссии! Восстановите энергию на станции."
        return False
    $ energy -= 15
    v "Добро пожаловать на Юпитер!"
    p "Соберите энергию, пройдя через электрический лабиринт!"
    "Инструкция: Выбирайте правильные пути, чтобы собрать энергию."
    "Осторожно! Неправильный выбор отнимет энергию."
    "Перед вами три пути. Куда пойти?"
    menu:
        "Налево (синяя дверь)":
            play sound "audio/energy.wav"
            $ energy_collected += 25
            $ energy = min(100, energy + 10)
            "Вы нашли энергетический кристалл! +25 энергии"
        "Прямо (зеленая дверь)":
            play sound "audio/failure.wav"
            $ energy_collected -= 10
            $ energy = max(0, energy - 10)
            "Ловушка! -10 энергии"
        "Направо (красная дверь)":
            "Пустая комната. Ничего не происходит."
    "Второй коридор. Что делать?"
    menu:
        "Взлететь вверх":
            play sound "audio/energy.wav"
            $ energy_collected += 30
            $ energy = min(100, energy + 15)
            "Вы нашли зарядную станцию! +30 энергии"
        "Проползти под лазерами":
            play sound "audio/failure.wav"
            $ energy_collected -= 15
            $ energy = max(0, energy - 15)
            "Вас ударило током! -15 энергии"
        "Вернуться назад":
            "Вы вернулись к началу."
    "Финальная комната. Выберите действие:"
    menu:
        "Активировать генератор (нужно 40 энергии)" if energy_collected >= 40:
            play sound "audio/success.wav"
            $ energy_collected += 50
            $ energy = min(100, energy + 30)
            "Генератор активирован! +50 энергии"
            $ jupiter_complete = True
        "Собрать оставшуюся энергию":
            play sound "audio/energy.wav"
            $ energy_collected += 20
            $ energy = min(100, energy + 10)
            "Вы собрали немного энергии. +20"
        "Быстро выйти":
            "Вы сбежали из лабиринта."
    if energy_collected > 0:
        $ crystals += energy_collected
        $ level += 1
        $ total_score += energy_collected
        play sound "audio/success.wav"
        "Вы собрали [energy_collected] единиц энергии!"
        "Получено [energy_collected] кристаллов!"
        "Уровень повышен до [level]!"
        if jupiter_complete:
            "Юпитерский лабиринт пройден!"
            return True
        else:
            return True
    else:
        play sound "audio/failure.wav"
        $ lives -= 1
        "Вы не собрали энергию."
        if lives <= 0:
            "Игра окончена!"
            return False
        else:
            return False

label jupiter_mission:
    if persistent.music_on:
        stop music fadeout 1.0
        play music "audio/epic.mp3" fadein 1.0 loop
    scene bg космос
    show planet юпитер at planet_top
    show персонаж4 at char_center
    p "Добро пожаловать на Юпитер!"
    p "Этот газовый гигант полон энергии."
    p "Собери как можно больше в энергетическом лабиринте!"
    call play_energy_game
    if _return:
        "Юпитерианская миссия завершена!"
    else:
        "Энергия закончилась!"
    if persistent.music_on:
        stop music fadeout 1.0
        play music "audio/space_theme.mp3" fadein 1.0 loop
    if lives <= 0:
        jump end_game
    else:
        jump level_select

# ---------- САТУРН ----------
label saturn_mission:
    if persistent.music_on:
        stop music fadeout 1.0
        play music "audio/mystery.mp3" fadein 1.0 loop
    scene bg космос
    show planet сатурн at planet_top
    show персонаж1 at char_center
    v "Добро пожаловать на Сатурн!"
    v "Эта планета защищена ледяным кольцом."
    v "Чтобы пройти, ответь на один сложный вопрос!"
    if energy < 20:
        v "Недостаточно энергии для этой миссии! Восстановите энергию на станции."
        jump level_select
    $ energy -= 20
    "Вопрос: Сколько основных колец у Сатурна?"
    menu:
        "3 кольца":
            "Неправильно!"
            play sound "audio/failure.wav"
            $ lives -= 1
            $ energy = max(0, energy - 10)
        "7 колец":
            "Правильно! У Сатурна 7 основных колец."
            play sound "audio/success.wav"
            $ saturn_complete = True
            $ crystals += 200
            $ level += 1
            $ total_score += 200
            "Получено 200 кристаллов!"
            "Уровень повышен до [level]!"
        "10 колец":
            "Слишком много!"
            play sound "audio/failure.wav"
            $ lives -= 1
            $ energy = max(0, energy - 10)
    if persistent.music_on:
        stop music fadeout 1.0
        play music "audio/space_theme.mp3" fadein 1.0 loop
    if lives <= 0:
        jump end_game
    else:
        jump level_select

# ---------- МЕРКУРИЙ ----------
label mercury_mission:
    if persistent.music_on:
        stop music fadeout 1.0
        play music "audio/epic.mp3" fadein 1.0 loop
    scene bg космос
    show planet меркурий at planet_top
    show персонаж3 at char_center
    l "Добро пожаловать на Меркурий!"
    l "Это последняя планета в нашем путешествии."
    l "Собери последние кристаллы!"
    if energy < 30:
        l "Недостаточно энергии для финальной миссии!"
        jump level_select
    $ energy -= 30
    "Вы находите сундук с сокровищами! Что будете делать?"
    menu:
        "Открыть сундук":
            play sound "audio/success.wav"
            $ mercury_complete = True
            $ crystals += 500
            $ level += 2
            $ total_score += 500
            $ game_completed = True
            "Вы нашли 500 кристаллов! Это финальная награда!"
            "Уровень повышен до [level]!"
            "Поздравляем! Вы завершили все миссии!"
        "Оставить сундук":
            "Вы решили не рисковать."
            $ crystals += 100
            $ total_score += 100
    if persistent.music_on:
        stop music fadeout 1.0
        play music "audio/space_theme.mp3" fadein 1.0 loop
    jump level_select

# ---------- КОСМИЧЕСКАЯ СТАНЦИЯ ----------
label space_station:
    scene bg станция
    show персонаж1 at char_left
    show персонаж2 at char_right
    v "Добро пожаловать на космическую станцию!"
    k "Здесь ты можешь восстановить силы и купить улучшения."
    menu:
        "Восстановить жизни (50 кристаллов)" if crystals >= 50 and lives < max_lives:
            play sound "audio/energy.wav"
            $ crystals -= 50
            $ lives = max_lives
            "Жизни восстановлены!"
        "Купить дополнительную жизнь (100 кристаллов)" if crystals >= 100:
            play sound "audio/energy.wav"
            $ crystals -= 100
            $ max_lives += 1
            $ lives += 1
            "Максимальное количество жизней увеличено!"
        "Восстановить энергию (бесплатно)":
            play sound "audio/energy.wav"
            $ energy = 100
            "Энергия восстановлена!"
        "Купить огненный шар (200 кристаллов)" if crystals >= 200:
            play sound "audio/success.wav"
            $ crystals -= 200
            $ fireball_power = True
            "Вы купили силу огненного шара! Он поможет в будущих миссиях!"
        "Настроить звук":
            call screen sound_settings
        "Вернуться":
            pass
    jump level_select

# === СТАТИСТИКА ===
label show_stats:
    scene bg космос
    show персонаж3 at char_center
    l "Твоя космическая статистика:"
    "════════════════════════════════════════"
    "  Жизни: [lives]/[max_lives]"
    "  Кристаллы: [crystals]"
    "  Уровень: [level]"
    "  Энергия: [energy]%"
    "  Общий счет: [total_score]"
    "════════════════════════════════════════"
    ""
    "╔══════════════════════════════════════╗"
    "            ПРОГРЕСС МИССИЙ"
    "╚══════════════════════════════════════╝"
    if moon_complete:
        "  🌙 Луна: {color=#00FF00}Завершено{/color}"
    else:
        "  🌙 Луна: {color=#FF0000}Не завершено{/color}"
    if mars_complete:
        "  🪐 Марс: {color=#00FF00}Завершено{/color}"
    else:
        "  🪐 Марс: {color=#FF0000}Не завершено{/color}"
    if jupiter_complete:
        "  ♃ Юпитер: {color=#00FF00}Завершено{/color}"
    else:
        "  ♃ Юпитер: {color=#FF0000}Не завершено{/color}"
    if saturn_complete:
        "  🪐 Сатурн: {color=#00FF00}Завершено{/color}"
    else:
        "  🪐 Сатурн: {color=#FF0000}Не завершено{/color}"
    if mercury_complete:
        "  ☿ Меркурий: {color=#00FF00}Завершено{/color}"
    else:
        "  ☿ Меркурий: {color=#FF0000}Не завершено{/color}"
    ""
    if game_completed:
        "🎉 Ты настоящий космический герой! Все миссии завершены! 🎉"
    elif total_score > 1000:
        "🚀 Отличный результат! Продолжай в том же духе! 🚀"
    elif total_score > 500:
        "⭐ Хорошая работа! Еще немного! ⭐"
    else:
        "✨ Продолжай исследовать космос! ✨"
    pause
    jump level_select

# === ФИНАЛ ===
label end_game:
    stop music fadeout 2.0
    scene bg черный
    with fade
    if total_score >= 1000:
        $ rank = "КОСМИЧЕСКИЙ ЛЕГЕНДА"
        $ rank_color = "#FFD700"
    elif total_score >= 500:
        $ rank = "ГЕРОЙ ГАЛАКТИКИ"
        $ rank_color = "#C0C0C0"
    elif total_score >= 200:
        $ rank = "ОПЫТНЫЙ ИССЛЕДОВАТЕЛЬ"
        $ rank_color = "#CD7F32"
    else:
        $ rank = "НАЧИНАЮЩИЙ КОСМОНАВТ"
        $ rank_color = "#FFFFFF"
    $ completed_missions = 0
    if moon_complete:
        $ completed_missions += 1
    if mars_complete:
        $ completed_missions += 1
    if jupiter_complete:
        $ completed_missions += 1
    if saturn_complete:
        $ completed_missions += 1
    if mercury_complete:
        $ completed_missions += 1
    show text "{size=60}МИССИЯ ЗАВЕРШЕНА{/size}\n\n{size=40}Звание: [rank]{/size}\n{size=40}Кристаллов: [crystals]{/size}\n{size=40}Общий счет: [total_score]{/size}\n{size=40}Уровень: [level]{/size}\n{size=40}Миссий завершено: [completed_missions]/5{/size}" at truecenter
    with dissolve
    pause 3.0
    if game_completed:
        show text "{size=50}Поздравляем!{/size}\n{size=30}Вы завершили все космические миссии!{/size}" at truecenter
        with dissolve
    else:
        show text "{size=50}Спасибо за игру!{/size}\n{size=30}До новых космических встреч!{/size}" at truecenter
        with dissolve
    pause 3.0
    return