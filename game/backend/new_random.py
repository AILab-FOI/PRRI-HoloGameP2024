import bge
import bpy
import os

def import_cube(cube_name):
    filepath = bpy.path.abspath("//") + cube_name + ".blend"
    with bpy.data.libraries.load(filepath, link=False) as (data_from, data_to):
        data_to.objects = [name for name in data_from.objects if name.startswith("Cube")]

    for obj in data_to.objects:
        if obj is not None:
            bpy.context.collection.objects.link(obj)

import_cube('kocka1')

def move_figure(game_board, figure_index=None):
    if figure_index:
        steps = game_board.roll_dice()
        game_board.movement.move_figure(game_board.players[game_board.current_player_index].color, steps, figure_index)
        if steps != 6:
            game_board.next_turn()
    else:
        game_board.play_turn()

def handle_keyboard_input():
    keyboard = bge.logic.keyboard
    scene = bge.logic.getCurrentScene()
    game_instance = scene.objects.get("Unutarnje")

    if game_instance and game_instance.get("game_instance", False):
        game_board_instance = game_instance.get("game_board_instance")
        if not game_board_instance:
            print("Game board instance not found.")
            return

        if game_instance.get('selecting_figure', False):
            available_figures = game_instance['available_figures']
            key_mapping = {
                bge.events.ONEKEY: 1,
                bge.events.TWOKEY: 2,
                bge.events.THREEKEY: 3,
                bge.events.FOURKEY: 4
            }
            for key, index in key_mapping.items():
                if keyboard.events[key] == bge.logic.KX_INPUT_JUST_ACTIVATED and index in available_figures:
                    figure_index = index
                    figure_color = game_instance['figure_color']
                    steps = game_instance['steps']
                    game_instance['selecting_figure'] = False
                    game_instance['figure_color'] = None
                    game_instance['steps'] = None
                    game_instance['available_figures'] = None
                    game_board_instance.movement.move_figure(figure_color, steps, figure_index)
                    if steps != 6:
                        game_board_instance.next_turn()
                    break
        else:
            if keyboard.events[bge.events.SPACEKEY] == bge.logic.KX_INPUT_JUST_ACTIVATED:
                game_board_instance.play_turn()

                # Spinning the cube
                cube = scene.objects.get("dice")
                if cube:
                    cube.applyRotation((0, 0, 0.1), True)
                else:
                    print("Cube  not found in the scene.")
    else:
        print("Game instance not found or 'game_instance' property is not set to True.")

handle_keyboard_input()
