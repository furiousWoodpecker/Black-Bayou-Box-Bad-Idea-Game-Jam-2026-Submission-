import os
import sys
import random
import time

import pygame
from pygame import mixer
from pygame.locals import *

# @KennyYipCoding tutorial on how to convert python files to exe files.
def resource_path(path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, path)

mixer.init()

mixer.Channel(0).set_volume(1)
mixer.Channel(1).set_volume(0.5)
mixer.Channel(2).set_volume(0.25)

pygame.font.init()
pygame.font.get_init()

screen_width = 1280
screen_height = 720
screen = pygame.display.set_mode((screen_width, screen_height))

clock = pygame.time.Clock()
    
cell = pygame.image.load(resource_path('prison_cell.png'))
cell = pygame.transform.scale(cell, (1280, 480))

keys = pygame.key.get_pressed()

font1 = pygame.font.SysFont('courier new', 25)  # Most text
font2 = pygame.font.SysFont('courier new', 15)  # Small text
font3 = pygame.font.SysFont('courier new', 50)  # Title

use_item = font1.render("Press Z to use item:", True, (255, 255, 255))
take_item = font1.render("Press X to take item:", True, (255, 255, 255))

go_back = font1.render("Press 0 to go back:", True, (255, 255, 255))
go_back_rect = go_back.get_rect()
go_back_rect.bottomleft = (25, screen_height)

shift_text = font1.render("Press SHIFT to continue:", True, (255, 255, 255))
shift_rect = shift_text.get_rect()
shift_rect.bottomleft = (5, screen_height)

class Prison_item:
    def __init__(self, item_name, item_type, item_description):
        self.name = item_name
        self.category = item_type
        self.desc = item_description

class Prison_dish:
    def __init__(self, who_the_dish_goes_to):
        self.diner = who_the_dish_goes_to

empty_space = Prison_item("-----", "None", "Empty space.")

prisoner_jumpsuit = Prison_item("PRISONER JUMPSUIT", "laundry", "This bright uniform has been worn by many prisoners.")
officers_coat = Prison_item("OFFICER'S COAT", "laundry", "If only you had a matching hat to go with it.")
officers_hat = Prison_item("OFFICER'S HAT", "laundry", "If only you had a matching coat to go with it.")
bedsheet = Prison_item("BEDSHEET", "laundry", "Combine two of them for a more graceful rooftop escape.")
pillowcase = Prison_item("PILLOWCASE", "laundry", "Combine three of them for a graceful rooftop escape.")

butter_knife = Prison_item("BUTTER KNIFE", "Cutlery", "Typically for eating food, but there's always self-defense.")
cake_fork = Prison_item("CAKE FORK", "Cutlery", "Typically for eating food, but there's always self-defense.")

lumber = Prison_item("LUMBER", "wood to be shipped", "Combine two of them to make one large beam.")
box_of_goods = Prison_item("BOX OF GOODS", "boxes to be shipped", "Full of minerals from mining.")

screwdriver = Prison_item("SCREWDRIVER", "tools", "I found that screwdriver lyin' about in the warehouse.")
doorknob = Prison_item("DOORKNOB", "doorknob", "Ah, the good ol' doorknob. Dunno why they're so popular.")
torch = Prison_item("TORCH", "torch", "Stealin' torches from the guards ain't easy I tell ya!")

lumber_beam = Prison_item("LUMBER BEAM", "craft", "Here's your big plank, I guess.")
pillowcase_parachute = Prison_item("PILLOWCASE PARACHUTE", "craft", "One handmade pillowcase parachute.")
bedsheet_parachute = Prison_item("BEDSHEET PARACHUTE", "craft", "There's your big parachute.")

prisoner_dish = Prison_dish("prisoner")
officer_dish = Prison_dish("officer")

days_in_prison = 1
escape_attempts = 0
open_vent = False
vent_already_open = False
escaping = False

specific_parachute = None # This is to check if the player used the besheet parachute or pillow parachute to escape at the end.

text_emphasis = 2

def line_separating_text_and_images():
    pygame.draw.rect(screen, (255, 255, 255), pygame.Rect(0, 480, 1280, 4))

accessories = []
max_accessories = [officers_coat, officers_hat]
times_spotted_wearing_guard_uniform = 0
inventory = [empty_space, empty_space, empty_space, empty_space, empty_space]

def inspect_inventory(inventory):

    global times_spotted_wearing_guard_uniform
    global accessories
    
    spotted = mixer.Sound(resource_path("Spotted.wav"))
    spotted.set_volume(0.5)

    if officers_coat in inventory and officers_hat in inventory:
        guard = pygame.image.load(resource_path('walter with no coat or hat.png'))
        stunned = pygame.image.load(resource_path('stunned walter no coat or hat.png'))
    elif officers_coat in inventory and officers_hat not in inventory:
        guard = pygame.image.load(resource_path('walter with no coat.png'))
        stunned = pygame.image.load(resource_path('stunned walter no coat.png'))
    elif officers_coat not in inventory and officers_hat in inventory:
        guard = pygame.image.load(resource_path('walter with no hat.png'))
        stunned = pygame.image.load(resource_path('stunned walter no hat.png'))
    else:
        guard = pygame.image.load(resource_path('walter.png'))
        stunned = pygame.image.load(resource_path('stunned walter.png'))
        
    guard = pygame.transform.scale(guard, (1280, 480))
    guard_rect = guard.get_rect()
    guard_rect.topleft = (0, 0)
    stunned = pygame.transform.scale(stunned, (1280, 480))
    stunned_rect = guard.get_rect()
    stunned_rect.topleft = (0, 0)
    
    num_of_empty_spaces = 0
    for i in range(len(inventory)):
        if inventory[i] == empty_space:
            num_of_empty_spaces += 1

    # Calculate chances of getting spotted (closer to 100 = higher chances). Chances are much greater on week 1 so the player is more likely to be introduced to the guards before getting items such as the cutlery and guard uniform.
    if days_in_prison <= 7:
        if num_of_empty_spaces >= 4:
            chance_of_inspection = 0
        elif num_of_empty_spaces == 3:
            chance_of_inspection = 20
        elif num_of_empty_spaces == 2:
            chance_of_inspection = 40
        elif num_of_empty_spaces == 1:
            chance_of_inspection = 60
        elif num_of_empty_spaces == 0:
            chance_of_inspection = 80

    else:
        if num_of_empty_spaces >= 4:
            chance_of_inspection = 0
        elif num_of_empty_spaces == 3:
            chance_of_inspection = 15
        elif num_of_empty_spaces == 2:
            chance_of_inspection = 30
        elif num_of_empty_spaces == 1:
            chance_of_inspection = 45
        elif num_of_empty_spaces == 0:
            chance_of_inspection = 60

    self_defense = False

    if chance_of_inspection > 0 and random.randint(1, 100) <= chance_of_inspection:

        if butter_knife in inventory or cake_fork in inventory:        
            for i in range(len(inventory)):
                if inventory[i] == butter_knife or inventory[i] == cake_fork:
                    random_item = i
                    self_defense = True
                    break
        else:
            random_item = random.randint(0, len(inventory) - 1)
            while inventory[random_item] == empty_space:
                random_item = random.randint(0, len(inventory) - 1)
        
        count = 1

        if len(accessories) > 0:

            while count < 2:

                screen.fill('black')
                line_separating_text_and_images()

                if (times_spotted_wearing_guard_uniform < 1 and len(accessories) == 1) or (times_spotted_wearing_guard_uniform < 3 and len(accessories) == 2):
                    text1 = font1.render("You sneak past the guards in your totally legitimate uniform.", True, (255, 255, 255))
                elif (times_spotted_wearing_guard_uniform >= 1 and len(accessories) == 1) or (times_spotted_wearing_guard_uniform >= 3 and len(accessories) == 2):
                    if self_defense == False:
                        mixer.Channel(0).play(spotted)
                        screen.blit(guard, guard_rect)
                        text1 = font1.render("A guard sees through your disguise and confiscates your totally legitimate uniform!", True, (255, 255, 255))
                        times_spotted_wearing_guard_uniform = -1
                        accessories = []
                    else:
                        screen.blit(stunned, stunned_rect)
                        text1 = font1.render(f"You quickly stun a guard with your {inventory[random_item].name} before he could take your uniform!", True, (255, 255, 255))
                        inventory[random_item] = empty_space
                            

                text1_rect = text1.get_rect()
                text1_rect.topleft = (5, 485)
                shift_rect.bottomleft = (0, 720)

                for i in range(text_emphasis):
                    screen.blit(text1, text1_rect)
                    screen.blit(shift_text, shift_rect)

                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()
                    else:
                        if event.type == KEYDOWN:
                            if event.key == K_LSHIFT or event.key == K_RSHIFT:
                                count += 1
                                times_spotted_wearing_guard_uniform += 1
                    pygame.display.flip()

        else:

            mixer.Channel(0).play(spotted)
            item_confiscated = inventory[random_item].name
            inventory[random_item] = empty_space
            
            while count < 3:

                screen.fill('black')
                line_separating_text_and_images()
                
                if count == 1:
                    text1 = font1.render(f"A guard catches you carrying something you shouldn't have on you!", True, (255, 255, 255))
                else:
                    if self_defense == True:
                        text1 = font1.render(f"In a moment of panic, you stab him with the {item_confiscated}, leaving him stunned!", True, (255, 255, 255))
                    else:
                        text1 = font1.render(f"The {item_confiscated} has been confiscated!", True, (255, 255, 255))

                text2 = font1.render("you quickly flee back to your cell before anyone notices!", True, (255, 255, 255))

                text1_rect = text1.get_rect()
                text2_rect = text2.get_rect()
                text1_rect.topleft = (5, 485)
                text2_rect.topleft = (5, 515)
                shift_rect.bottomleft = (5, 720)

                screen.blit(guard, guard_rect)
                for i in range(text_emphasis):
                    screen.blit(text1, text1_rect)
                    if self_defense == True and count == 2:
                        screen.blit(stunned, stunned_rect)
                        screen.blit(text2, text2_rect)
                    screen.blit(shift_text, shift_rect)

                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()
                    else:
                        if event.type == KEYDOWN:
                            if event.key == K_LSHIFT or event.key == K_RSHIFT:
                                count += 1
                    pygame.display.flip()


def inspect_cell(mattress, pillow, hole):

    global vent
    global open_vent
    global vent_already_open

    open_vent = False
    vent_already_open = False

    cell_items = [mattress[0], pillow[0], hole[0]]
    area_checked = random.randint(0, 2)
    item_confiscated = cell_items[area_checked]
    count = 1

    cell = pygame.image.load(resource_path('prison_cell.png'))
    cell = pygame.transform.scale(cell, (1280, 480))

    while count < 3:
        
        if count == 1:
            text1 = font1.render("The guards have done their weekly cell inspection!", True, (255, 255, 255))
        else:
            if item_confiscated != empty_space:
                text1 = font1.render(f"The {item_confiscated.name} has been confiscated!", True, (255, 255, 255))
            else:
                text1 = font1.render("The guards couldn't find anything.", True, (255, 255, 255))
                
            cell_items[area_checked] = empty_space
            mattress[0] = cell_items[0]
            pillow[0] = cell_items[1]

        text1_rect = text1.get_rect()
        text1_rect.topleft = (5, 485)
        shift_rect.bottomleft = (0, 720)

        screen.fill('black')

        screen.blit(cell, (0, 0))
        for i in range(text_emphasis):
            screen.blit(text1, text1_rect)
            screen.blit(shift_text, shift_rect)
        line_separating_text_and_images()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            else:
                if event.type == KEYDOWN:
                    if event.key == K_LSHIFT or event.key == K_RSHIFT:
                        count += 1
            pygame.display.flip()







def show_inventory(inventory, inventory_name):

    pygame.draw.rect(screen, (255, 255, 255), pygame.Rect(970, 480, 4, 239))

    inventory_heading = font1.render(inventory_name, True, (255, 255, 255))
    slot1 = font2.render(inventory[0].name, True, (255, 255, 255))
    slot2 = font2.render(inventory[1].name, True, (255, 255, 255))
    slot3 = font2.render(inventory[2].name, True, (255, 255, 255))
    slot4 = font2.render(inventory[3].name, True, (255, 255, 255))
    slot5 = font2.render(inventory[4].name, True, (255, 255, 255))

    inventory_rect = inventory_heading.get_rect()
    inventory_rect.topleft = (980, 485)
    slot1_rect = slot1.get_rect()
    slot1_rect.topleft = (980, 515)
    slot2_rect = slot2.get_rect()
    slot2_rect.topleft = (980, 540)
    slot3_rect = slot3.get_rect()
    slot3_rect.topleft = (980, 565)
    slot4_rect = slot4.get_rect()
    slot4_rect.topleft = (980, 590)
    slot5_rect = slot5.get_rect()
    slot5_rect.topleft = (980, 615)

    screen.blit(inventory_heading, inventory_rect)
    screen.blit(slot1, slot1_rect)
    screen.blit(slot2, slot2_rect)
    screen.blit(slot3, slot3_rect)
    screen.blit(slot4, slot4_rect)
    screen.blit(slot5, slot5_rect)

def show_interactable_inventory(inventory, heading, custom_hint, go_back_text):
    
    inventory_heading = font1.render(heading, True, (255, 255, 255))
    inv_slot1 = font1.render("[1] " + inventory[0].name, True, (255, 255, 255))
    inv_slot2 = font1.render("[2] " + inventory[1].name, True, (255, 255, 255))
    inv_slot3 = font1.render("[3] " + inventory[2].name, True, (255, 255, 255))
    inv_slot4 = font1.render("[4] " + inventory[3].name, True, (255, 255, 255))
    inv_slot5 = font1.render("[5] " + inventory[4].name, True, (255, 255, 255))
    hint = font2.render(custom_hint, True, (255, 255, 255))

    inventory_rect = inventory_heading.get_rect()
    inventory_rect.topleft = (25, 485)
    inv_slot1_rect = inv_slot1.get_rect()
    inv_slot1_rect.topleft = (25, 516)
    inv_slot2_rect = inv_slot2.get_rect()
    inv_slot2_rect.topleft = (25, 542)
    inv_slot3_rect = inv_slot3.get_rect()
    inv_slot3_rect.topleft = (25, 568)
    inv_slot4_rect = inv_slot4.get_rect()
    inv_slot4_rect.topleft = (25, 594)
    inv_slot5_rect = inv_slot5.get_rect()
    inv_slot5_rect.topleft = (25, 620)
    hint_rect = hint.get_rect()
    hint_rect.topleft = (25, 660)

    for i in range(text_emphasis):
        screen.blit(inventory_heading, inventory_rect)
        screen.blit(inv_slot1, inv_slot1_rect)
        screen.blit(inv_slot2, inv_slot2_rect)
        screen.blit(inv_slot3, inv_slot3_rect)
        screen.blit(inv_slot4, inv_slot4_rect)
        screen.blit(inv_slot5, inv_slot5_rect)
        screen.blit(hint, hint_rect)
        if go_back_text == True:
            screen.blit(go_back, go_back_rect)


def day_blank(activity):
    
    global escape_attempts

    pygame.display.set_caption(f"Day {days_in_prison}")

    if escaping == True:
        escape_attempts += 1
        text = font3.render(f"ESCAPE ATTEMPT {escape_attempts}", True, (255, 255, 255))
    else:
        text = font3.render(f'DAY {days_in_prison} - {activity.upper()}', True, (255, 255, 255))
    text_rect = text.get_rect()
    text_rect.center = (screen_width // 2, screen_height // 2)

    shift_text = font1.render("Press SHIFT to continue:", True, (255, 255, 255))
    shift_rect = shift_text.get_rect()
    shift_rect.center = (screen_width // 2, (screen_height // 2)+50)
    
    while True:

        screen.fill('black')

        for i in range(text_emphasis):
            screen.blit(text, text_rect)
            screen.blit(shift_text, shift_rect)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            else:
                if event.type == KEYDOWN:
                    if event.key == K_LSHIFT or event.key == K_RSHIFT:
                        return None
            pygame.display.flip()





mattress = [empty_space]
pillow = [empty_space]
hole = [empty_space]

def inside_cell():

    global shift_text
    global shift_rect
    main_options = True
    use_item_options = False
    look_under_mattress = False
    look_inside_pillow = False
    look_inside_hole = False

    global item_used
    item_used = None

    global escaping
    global open_vent
    global vent_already_open

    usable_items = [screwdriver, butter_knife] # Exclude officer uniform (coat & hat)

    pygame.display.set_caption(f"Night {days_in_prison - 1} - In Your Cell")
    
    mixer.music.load(resource_path("In Your Cell.wav"))
    mixer.music.set_volume(1)
    mixer.music.play(-1)

    ventSFX = mixer.Sound(resource_path('SFX Vent Falling.wav'))

    text1 = font1.render("Press A to look under mattress:", True, (255, 255, 255))
    text2 = font1.render("Press S to look inside pillowcase:", True, (255, 255, 255))
    text3 = font1.render("Press D to look inside hole:", True, (255, 255, 255))
    text4 = use_item
    text5 = font1.render("Press C to begin escape:", True, (255, 255, 255))
    text1_rect = text1.get_rect()
    text2_rect = text2.get_rect()
    text3_rect = text3.get_rect()
    text4_rect = text3.get_rect()
    text5_rect = text4.get_rect()
    text1_rect.topleft = (5, 485)
    text2_rect.topleft = (5, 515)
    text3_rect.topleft = (5, 545)
    text4_rect.topleft = (5, 605)
    text5_rect.topleft = (5, 635)

    def move_items_under_mattress(inventory, mattress):

        screen.fill('black')
        screen.blit(cell, (0, 0))
        line_separating_text_and_images()
        pygame.draw.rect(screen, (255, 255, 255), pygame.Rect((screen_width // 2), 480, 2, 239))

        mattress_heading = font1.render("UNDER MATTRESS:", True, (255, 255, 255))
        mat_slot = font1.render(mattress[0].name, True, (255, 255, 255))

        mattress_rect = mattress_heading.get_rect()
        mattress_rect.topleft = ((screen_width // 2) + 25, 485)
        mat_slot_rect = mat_slot.get_rect()
        mat_slot_rect.topleft = ((screen_width // 2) + 25, 516)

        show_interactable_inventory(inventory, "Press a number to move an item:", "", True)
        
        for i in range(text_emphasis):
            screen.blit(mattress_heading, mattress_rect)
            screen.blit(mat_slot, mat_slot_rect)

    def move_items_inside_pillow(inventory, pillow):
        
        screen.fill('black')
        screen.blit(cell, (0, 0))
        line_separating_text_and_images()
        pygame.draw.rect(screen, (255, 255, 255), pygame.Rect((screen_width // 2), 480, 2, 239))

        pillow_heading = font1.render("INSIDE PILLOW:", True, (255, 255, 255))
        pil_slot = font1.render(pillow[0].name, True, (255, 255, 255))

        pillow_rect = pillow_heading.get_rect()
        pillow_rect.topleft = ((screen_width // 2) + 25, 485)
        pil_slot_rect = pil_slot.get_rect()
        pil_slot_rect.topleft = ((screen_width // 2) + 25, 516)

        show_interactable_inventory(inventory, "Press a number to move an item:", "", True)

        for i in range(text_emphasis):
            screen.blit(pillow_heading, pillow_rect)
            screen.blit(pil_slot, pil_slot_rect)

    def move_items_into_hole(inventory, hole):

        screen.fill('black')
        screen.blit(cell, (0, 0))
        line_separating_text_and_images()
        pygame.draw.rect(screen, (255, 255, 255), pygame.Rect((screen_width // 2), 480, 2, 239))

        hole_heading = font1.render("INSIDE HOLE IN FLOOR:", True, (255, 255, 255))
        hol_slot = font1.render(hole[0].name, True, (255, 255, 255))

        hole_rect = hole_heading.get_rect()
        hole_rect.topleft = ((screen_width // 2) + 25, 485)
        hol_slot_rect = hol_slot.get_rect()
        hol_slot_rect.topleft = ((screen_width // 2) + 25, 516)

        show_interactable_inventory(inventory, "Press a number to move an item:", "", True)
        
        for i in range(text_emphasis):
            screen.blit(hole_heading, hole_rect)
            screen.blit(hol_slot, hol_slot_rect)

    global heading
    heading = ""

    def use_items(inventory, hint):
        
        global item_used
        global open_vent
        global escaping

        screen.fill('black')
        screen.blit(cell, (0, 0))
        line_separating_text_and_images()

        if item_used == None:
            show_interactable_inventory(inventory, "Press the corresponding number to use item:", hint, True)
        elif item_used == empty_space:
            show_interactable_inventory(inventory, "Di- did you just try to use an empty slot as if it were an item?", hint, True)
        elif (item_used == screwdriver or item_used == butter_knife) and vent_already_open == False:
            open_vent = True
            if item_used == screwdriver:
                show_interactable_inventory(inventory, f"You used the {item_used.name} to unscrew the vent cover from the wall.", hint, True)
            elif item_used == butter_knife:
                show_interactable_inventory(inventory, f"You broke the {item_used.name} unscrewing the vent cover from the wall.", hint, True)
        elif (item_used == screwdriver or item_used == butter_knife) and vent_already_open == True:
            show_interactable_inventory(inventory, "The vent is already open.", hint, True)
        elif item_used == officers_coat:
            if officers_coat not in accessories:
                show_interactable_inventory(inventory, heading, hint, True)
            else:
                show_interactable_inventory(inventory, heading, hint, True)
        elif item_used == officers_hat:
            if officers_hat not in accessories:
                show_interactable_inventory(inventory, heading, hint, True)
            else:
                show_interactable_inventory(inventory, heading, hint, True)
        else:
            show_interactable_inventory(inventory, "That item cannot be used right now.", hint, True)
            
    while True:

        if open_vent == True:
            cell = pygame.image.load(resource_path('prison_cell_escape.png'))
        else:
            shift_text = font1.render("Press SHIFT to go to sleep:", True, (255, 255, 255))
            cell = pygame.image.load(resource_path('prison_cell.png'))
        cell = pygame.transform.scale(cell, (1280, 480))

        if main_options == True:
            screen.fill('black')
            screen.blit(cell, (0, 0))
            for i in range(text_emphasis):
                screen.blit(text1, text1_rect)
                screen.blit(text2, text2_rect)
                screen.blit(text3, text3_rect)
                screen.blit(text4, text4_rect)
                if open_vent == True:
                    screen.blit(text5, text5_rect)
                screen.blit(shift_text, shift_rect)
                show_inventory(inventory, "INVENTORY:")
            line_separating_text_and_images()
            
        if use_item_options == True and open_vent == False:
            use_items(inventory, "Perhaps you could unscrew that vent from the wall with something...")
        elif use_item_options == True and open_vent == True:
            use_items(inventory, "")
            
        if look_under_mattress == True:
            move_items_under_mattress(inventory, mattress)
            
        if look_inside_pillow == True:
            move_items_inside_pillow(inventory, pillow)

        if look_inside_hole == True:
            move_items_into_hole(inventory, hole)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            else:
                if event.type == KEYDOWN:
                    if event.key == K_LSHIFT or event.key == K_RSHIFT and main_options == True:
                        mixer.music.stop()
                        return None

                    ## Main options ##
                    if event.key == K_0 and main_options == False:
                        look_under_mattress = False
                        look_inside_pillow = False
                        look_inside_hole = False
                        use_item_options = False
                        item_used = None
                        main_options = True
                    if event.key == K_a and main_options == True:
                        look_under_mattress = True
                        main_options = False
                    if event.key == K_s and main_options == True:
                        look_inside_pillow = True
                        main_options = False
                    if event.key == K_d and main_options == True:
                        look_inside_hole = True
                        main_options = False
                    if event.key == K_z and main_options == True:
                        use_item_options = True
                        main_options = False
                    if event.key == K_c and main_options == True and open_vent == True:
                        main_options = False
                        escaping = True
                        mixer.music.stop()
                        return None
                        


                    ## Swap items between mattress/pillow/hole ##
                    if event.key == K_1 and look_under_mattress == True:
                        temp = mattress[0]
                        mattress[0] = inventory[0]
                        inventory[0] = temp
                    elif event.key == K_1 and look_inside_pillow == True:
                        temp = pillow[0]
                        pillow[0] = inventory[0]
                        inventory[0] = temp
                    elif event.key == K_1 and look_inside_hole == True:
                        temp = hole[0]
                        hole[0] = inventory[0]
                        inventory[0] = temp

                    if event.key == K_2 and look_under_mattress == True:
                        temp = mattress[0]
                        mattress[0] = inventory[1]
                        inventory[1] = temp
                    elif event.key == K_2 and look_inside_pillow == True:
                        temp = pillow[0]
                        pillow[0] = inventory[1]
                        inventory[1] = temp
                    elif event.key == K_2 and look_inside_hole == True:
                        temp = hole[0]
                        hole[0] = inventory[1]
                        inventory[1] = temp
                            
                    if event.key == K_3 and look_under_mattress == True:
                        temp = mattress[0]
                        mattress[0] = inventory[2]
                        inventory[2] = temp
                    elif event.key == K_3 and look_inside_pillow == True:
                        temp = pillow[0]
                        pillow[0] = inventory[2]
                        inventory[2] = temp
                    elif event.key == K_3 and look_inside_hole == True:
                        temp = hole[0]
                        hole[0] = inventory[2]
                        inventory[2] = temp

                    if event.key == K_4 and look_under_mattress == True:
                        temp = mattress[0]
                        mattress[0] = inventory[3]
                        inventory[3] = temp
                    elif event.key == K_4 and look_inside_pillow == True:
                        temp = pillow[0]
                        pillow[0] = inventory[3]
                        inventory[3] = temp
                    elif event.key == K_4 and look_inside_hole == True:
                        temp = hole[0]
                        hole[0] = inventory[3]
                        inventory[3] = temp

                    if event.key == K_5 and look_under_mattress == True:
                        temp = mattress[0]
                        mattress[0] = inventory[4]
                        inventory[4] = temp
                    elif event.key == K_5 and look_inside_pillow == True:
                        temp = pillow[0]
                        pillow[0] = inventory[4]
                        inventory[4] = temp
                    elif event.key == K_5 and look_inside_hole == True:
                        temp = hole[0]
                        hole[0] = inventory[4]
                        inventory[4] = temp


                    ## Use items ##
                    if event.key == K_1 and use_item_options == True:
                        item_used = inventory[0]
                        if len(usable_items) == 1:
                            vent_already_open = True
                        if inventory[0] in usable_items and len(usable_items) > 1:
                            if item_used == butter_knife:
                                inventory[0] = empty_space
                            usable_items.remove(item_used)
                            mixer.Channel(1).play(mixer.Sound(ventSFX))
                        elif inventory[0] == officers_coat:
                            if officers_coat not in accessories:
                                accessories.append(officers_coat)
                                heading = "You put on the officer's coat."
                                inventory[0] = empty_space
                            else:
                                heading = "You are already wearing an officer's coat."
                        elif inventory[0] == officers_hat:
                            if officers_hat not in accessories:
                                accessories.append(officers_hat)
                                heading = "You put on the officer's hat."
                                inventory[0] = empty_space
                            else:
                                heading = "You are already wearing an officer's hat."

                    if event.key == K_2 and use_item_options == True:
                        item_used = inventory[1]
                        if len(usable_items) == 1:
                            vent_already_open = True
                        if inventory[1] in usable_items and len(usable_items) > 1:
                            if item_used == butter_knife:
                                inventory[1] = empty_space
                            usable_items.remove(item_used)
                            mixer.Channel(1).play(mixer.Sound(ventSFX))
                        elif inventory[1] == officers_coat:
                            if officers_coat not in accessories:
                                accessories.append(officers_coat)
                                heading = "You put on the officer's coat."
                                inventory[1] = empty_space
                            else:
                                heading = "You are already wearing an officer's coat."
                        elif inventory[1] == officers_hat:
                            if officers_hat not in accessories:
                                accessories.append(officers_hat)
                                heading = "You put on the officer's hat."
                                inventory[1] = empty_space
                            else:
                                heading = "You are already wearing an officer's hat."
                        
                            
                    if event.key == K_3 and use_item_options == True:
                        item_used = inventory[2]
                        if len(usable_items) == 1:
                            vent_already_open = True
                        if inventory[2] in usable_items and len(usable_items) > 1:
                            if item_used == butter_knife:
                                inventory[2] = empty_space
                            usable_items.remove(item_used)
                            mixer.Channel(1).play(mixer.Sound(ventSFX))
                        elif inventory[2] == officers_coat:
                            if officers_coat not in accessories:
                                accessories.append(officers_coat)
                                heading = "You put on the officer's coat."
                                inventory[2] = empty_space
                            else:
                                heading = "You are already wearing an officer's coat."
                        elif inventory[2] == officers_hat:
                            if officers_hat not in accessories:
                                accessories.append(officers_hat)
                                heading = "You put on the officer's hat."
                                inventory[2] = empty_space
                            else:
                                heading = "You are already wearing an officer's hat."
                        

                    if event.key == K_4 and use_item_options == True:
                        item_used = inventory[3]
                        if len(usable_items) == 1:
                            vent_already_open = True
                        if inventory[3] in usable_items and len(usable_items) > 1:
                            if item_used == butter_knife:
                                inventory[3] = empty_space
                            usable_items.remove(item_used)
                            mixer.Channel(1).play(mixer.Sound(ventSFX))
                        elif inventory[3] == officers_coat:
                            if officers_coat not in accessories:
                                accessories.append(officers_coat)
                                heading = "You put on the officer's coat."
                                inventory[3] = empty_space
                            else:
                                heading = "You are already wearing an officer's coat."
                        elif inventory[3] == officers_hat:
                            if officers_hat not in accessories:
                                accessories.append(officers_hat)
                                heading = "You put on the officer's hat."
                                inventory[3] = empty_space
                            else:
                                heading = "You are already wearing an officer's hat."
                        

                    if event.key == K_5 and use_item_options == True:
                        item_used = inventory[4]
                        if len(usable_items) == 1:
                            vent_already_open = True
                        if inventory[4] in usable_items and len(usable_items) > 1:
                            if item_used == butter_knife:
                                inventory[4] = empty_space
                            usable_items.remove(item_used)
                            mixer.Channel(1).play(mixer.Sound(ventSFX))
                        elif inventory[4] == officers_coat:
                            if officers_coat not in accessories:
                                accessories.append(officers_coat)
                                heading = "You put on the officer's coat."
                                inventory[4] = empty_space
                            else:
                                heading = "You are already wearing an officer's coat."
                        elif inventory[4] == officers_hat:
                            if officers_hat not in accessories:
                                accessories.append(officers_hat)
                                heading = "You put on the officer's hat."
                                inventory[4] = empty_space
                            else:
                                heading = "You are already wearing an officer's hat."
                        
        pygame.display.flip()










def day1_Chopping():
    
    global days_in_prison
    
    chopping = True
    chop_input = 'Q'
    input_key_pressed_down = False
    pygame.display.set_caption(f"Day {days_in_prison} - Chopping")

    def chop_logs(logs_left, logs_chopped, input_key_pressed_down):

        global list_of_animations
        
        frame1 = pygame.image.load(resource_path('chop_animation_f1.png'))
        frame1 = pygame.transform.scale(frame1, (1280, 480))
        frame2 = pygame.image.load(resource_path('chop_animation_f2.png'))
        frame2 = pygame.transform.scale(frame2, (1280, 480))
        frame3 = pygame.image.load(resource_path('chop_animation_f3.png'))
        frame3 = pygame.transform.scale(frame3, (1280, 480))
        frame4 = pygame.image.load(resource_path('chop_animation_f4.png'))
        frame4 = pygame.transform.scale(frame4, (1280, 480))
        frame5 = pygame.image.load(resource_path('chop_animation_f5.png'))
        frame5 = pygame.transform.scale(frame5, (1280, 480))
        frame6 = pygame.image.load(resource_path('chop_animation_f6.png'))
        frame6 = pygame.transform.scale(frame6, (1280, 480))
        frame7 = pygame.image.load(resource_path('chop_animation_f7.png'))
        frame7 = pygame.transform.scale(frame7, (1280, 480))
        frame8 = pygame.image.load(resource_path('chop_animation_f8.png'))
        frame8 = pygame.transform.scale(frame8, (1280, 480))
        frame9 = pygame.image.load(resource_path('chop_animation_f9.png'))
        frame9 = pygame.transform.scale(frame9, (1280, 480))

        # Animation code made by following a tutorial made by 'Clear Code' on YT #
        class Chopping_Animation(pygame.sprite.Sprite):
            def __init__(self):
                super().__init__()
                self.frames = [frame1, frame2, frame3, frame4, frame5, frame6, frame7, frame8, frame9]
                self.is_animating = False
                self.current_frame = 0
                self.image = self.frames[self.current_frame]

                self.rect = self.image.get_rect()
                self.rect.topleft = (0, 0)

            def animate(self):
                self.is_animating = True

            def update(self):

                if self.is_animating == False and logs_left == 0:
                    pygame.draw.rect(screen, (0, 0, 0), pygame.Rect((screen_width)-1050, 0, 1051, 480))
                    
                if self.is_animating == True:
                    self.current_frame += 0.25

                    if self.current_frame >= 7 and logs_left == 0:
                        pygame.draw.rect(screen, (0, 0, 0), pygame.Rect((screen_width)-1050, 0, 1051, 480))

                    if self.current_frame >= len(self.frames):
                        self.current_frame = 0
                        self.is_animating = False

                    self.image = self.frames[int(self.current_frame)]

        list_of_animations = pygame.sprite.Group()
        chop_anim = Chopping_Animation()
        list_of_animations.add(chop_anim)  

        sfx1 = mixer.Sound(resource_path('SFX Chopping 1.wav'))
        sfx2 = mixer.Sound(resource_path('SFX Chopping 2.wav'))
        sfx3 = mixer.Sound(resource_path('SFX Chopping 3.wav'))

        # CHOP LOGS #
        while True:

            if chop_anim.is_animating == False and logs_left <= 0:
                pygame.draw.rect(screen, (0, 0, 0), pygame.Rect((screen_width)-1000, 0, 10001, 480))

            if logs_left <= 0:
                text1 = font1.render(f"You don't need to chop any more logs!",True, (255, 255, 255))
            elif logs_left == 1:
                text1 = font1.render(f"You must chop {logs_left} more log!", True, (255, 255, 255))
            else:
                text1 = font1.render(f"You must chop {logs_left} more logs!", True, (255, 255, 255))
            text2 = font1.render(f"Logs chopped: {logs_chopped}", True, (255, 255, 255))
            text3 = font1.render(f"Press {chop_input} to chop log:", True, (255, 255, 255))
            
            text1_rect = text1.get_rect()
            text2_rect = text2.get_rect()
            text3_rect = text3.get_rect()
            text1_rect.topleft = (5, 485)
            text2_rect.topleft = (5, 515)
            text3_rect.topleft = (5, 545)
                
            screen.fill('black')       
            line_separating_text_and_images()
            
            for i in range(text_emphasis):
                screen.blit(text1, text1_rect)
                screen.blit(text2, text2_rect)
                if logs_left > 0:
                    screen.blit(text3, text3_rect)
                elif logs_left <= 0:
                    screen.blit(shift_text, shift_rect)
                show_inventory(inventory, "INVENTORY:")

            for event in pygame.event.get():
                
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                        
                if event.type == KEYDOWN:
                    if event.key == K_q and chop_anim.is_animating == False and logs_left > 0:
                        chop_anim.animate()
                        logs_left -= 1
                        logs_chopped += 1
                        
                        random_sfx = random.randint(1, 3)
                        if random_sfx == 1:
                            mixer.Channel(1).play(sfx1)
                        elif random_sfx == 2:
                            mixer.Channel(1).play(sfx2)
                        elif random_sfx == 3:
                            mixer.Channel(1).play(sfx3)
                    elif (event.key == K_LSHIFT or event.key == K_RSHIFT) and logs_left <= 0:
                        return logs_chopped

            list_of_animations.draw(screen)
            list_of_animations.update()       
            pygame.display.flip()
            clock.tick(60)
    
            
    rng = random.randint(1, 4)
    if rng == 1:
        mixer.music.load(resource_path("Manual Labour 1.wav"))
    elif rng == 2:
        mixer.music.load(resource_path("Manual Labour 2.wav"))
    elif rng == 3:
        mixer.music.load(resource_path("Manual Labour 3.wav"))
    elif rng == 4:
        mixer.music.load(resource_path("Manual Labour 4.wav"))
    mixer.music.set_volume(1)
    mixer.music.play(-1)

    # THE ACTUAL PART OF THE FUNCTION
    while chopping:

        logs_chopped = 0
        logs_left = random.randint(2, 4) * 5

        logs_chopped = chop_logs(logs_left, logs_chopped, input_key_pressed_down)
        num_of_lumber = logs_chopped // 5
        days_in_prison += 1

        mixer.music.stop()
        time.sleep(0.2)

        return num_of_lumber













def day2_Mining():
    
    global days_in_prison
    mining = True
    mine_input = 'Q'
    pygame.display.set_caption(f"Day {days_in_prison} - Mining")

    def mine_minerals(minerals_mined, minerals_to_mine):

        count = 0

        frame1 = pygame.image.load(resource_path('mine_animation_f1.png'))
        frame1 = pygame.transform.scale(frame1, (1280, 480))
        frame2 = pygame.image.load(resource_path('mine_animation_f2.png'))
        frame2 = pygame.transform.scale(frame2, (1280, 480))
        frame3 = pygame.image.load(resource_path('mine_animation_f3.png'))
        frame3 = pygame.transform.scale(frame3, (1280, 480))
        frame4 = pygame.image.load(resource_path('mine_animation_f4.png'))
        frame4 = pygame.transform.scale(frame4, (1280, 480))
        frame5 = pygame.image.load(resource_path('mine_animation_f5.png'))
        frame5 = pygame.transform.scale(frame5, (1280, 480))
        frame6 = pygame.image.load(resource_path('mine_animation_f6.png'))
        frame6 = pygame.transform.scale(frame6, (1280, 480))
        frame7 = pygame.image.load(resource_path('mine_animation_f7.png'))
        frame7 = pygame.transform.scale(frame7, (1280, 480))
        frame8 = pygame.image.load(resource_path('mine_animation_f8.png'))
        frame8 = pygame.transform.scale(frame8, (1280, 480))
        frame9 = pygame.image.load(resource_path('mine_animation_f9.png'))
        frame9 = pygame.transform.scale(frame9, (1280, 480))
        frame10 = pygame.image.load(resource_path('mine_animation_f10.png'))
        frame10 = pygame.transform.scale(frame10, (1280, 480))
        frame11 = pygame.image.load(resource_path('mine_animation_f11.png'))
        frame11 = pygame.transform.scale(frame11, (1280, 480))
        frame12 = pygame.image.load(resource_path('mine_animation_f12.png'))
        frame12 = pygame.transform.scale(frame12, (1280, 480))
        frame13 = pygame.image.load(resource_path('mine_animation_f13.png'))
        frame13 = pygame.transform.scale(frame13, (1280, 480))
        frame14 = pygame.image.load(resource_path('mine_animation_f14.png'))
        frame14 = pygame.transform.scale(frame14, (1280, 480))
        frame15 = pygame.image.load(resource_path('mine_animation_f15.png'))
        frame15 = pygame.transform.scale(frame15, (1280, 480))

        class Mining_Animation(pygame.sprite.Sprite):
            def __init__(self):
                super().__init__()
                self.part1 = [frame1, frame2, frame3, frame4, frame5, frame6]
                self.part2 = [frame6, frame7, frame8, frame9, frame10, frame11]
                self.part3 = [frame11, frame12, frame13, frame14, frame15, frame1]
                self.is_animating = False
                self.current_frame = 0
                self.image = frame1

                self.rect = self.image.get_rect()
                self.rect.topleft = (0, 0)

            def animate(self):
                self.current_frame = 0
                self.is_animating = True

            def update(self):

                if self.is_animating == False and minerals_to_mine == 0:
                    pygame.draw.rect(screen, (0, 0, 0), pygame.Rect((screen_width)-1050, 0, 1051, 480))
                    
                if self.is_animating == True:
                    self.current_frame += 0.25

                    if self.current_frame >= 5:
                        self.current_frame = 5
                        self.is_animating = False

                    if count == 1:
                        self.image = self.part1[int(self.current_frame)]
                    elif count == 2:
                        self.image = self.part2[int(self.current_frame)]
                    elif count == 3:
                        self.image = self.part3[int(self.current_frame)]
                        if self.current_frame >= 2 and minerals_to_mine == 0:
                            pygame.draw.rect(screen, (0, 0, 0), pygame.Rect(1000, 0, 2001, 400))
                        if self.current_frame >= 3 and minerals_to_mine == 0:
                            pygame.draw.rect(screen, (0, 0, 0), pygame.Rect(800, 0, 3001, 400))
                        if self.current_frame >= 4 and minerals_to_mine == 0:
                            pygame.draw.rect(screen, (0, 0, 0), pygame.Rect(500, 0, 7001, 400))

        animations = pygame.sprite.Group()

        mine_anim = Mining_Animation()
        animations.add(mine_anim)

        sfx1 = mixer.Sound(resource_path('SFX Mining 1.wav'))
        sfx2 = mixer.Sound(resource_path('SFX Mining 2.wav'))
        sfx3 = mixer.Sound(resource_path('SFX Mining 3.wav'))

        sfx = [sfx1, sfx2]
        
        while True:

            screen.fill('black')

            if minerals_to_mine <= 0:
                text1 = font1.render(f"You don't need to mine any more minerals!", True, (255, 255, 255))
            elif minerals_to_mine == 1:
                text1 = font1.render(f"You must mine {minerals_to_mine} more mineral!", True, (255, 255, 255))
            else:
                text1 = font1.render(f"You must mine {minerals_to_mine} more minerals!", True, (255, 255, 255))
            text2 = font1.render(f"Minerals mined: {minerals_mined}", True, (255, 255, 255))
            text3 = font1.render(f"Press {mine_input} to mine mineral:", True, (255, 255, 255))
            
            text1_rect = text1.get_rect()
            text2_rect = text2.get_rect()
            text3_rect = text3.get_rect()
            text1_rect.topleft = (5, 485)
            text2_rect.topleft = (5, 515)
            text3_rect.topleft = (5, 545)

            line_separating_text_and_images()

            for i in range(text_emphasis):
                screen.blit(text1, text1_rect)
                screen.blit(text2, text2_rect)
                if minerals_to_mine > 0:
                    screen.blit(text3, text3_rect)
                if minerals_to_mine <= 0:
                    screen.blit(shift_text, shift_rect)
                show_inventory(inventory, "INVENTORY:")

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                else:
                    if event.type == KEYDOWN:
                        if event.key == K_q and mine_anim.is_animating == False and minerals_to_mine > 0:
                            count += 1
                            mine_anim.animate()
                            if count != 3:
                                mixer.Channel(0).play(sfx[random.randint(0, 1)])
                            if count == 3:
                                minerals_to_mine -= 1
                                minerals_mined += 1
                                mixer.Channel(1).play(sfx3)
                            if count == 4:
                                count = 1
                                
                        if (event.key == K_LSHIFT or event.key == K_RSHIFT) and minerals_to_mine <= 0:
                            return minerals_mined

            animations.draw(screen)
            animations.update()
            pygame.display.update()
            clock.tick(60)
                

    rng = random.randint(1, 4)
    if rng == 1:
        mixer.music.load(resource_path("Manual Labour 1.wav"))
    elif rng == 2:
        mixer.music.load(resource_path("Manual Labour 2.wav"))
    elif rng == 3:
        mixer.music.load(resource_path("Manual Labour 3.wav"))
    elif rng == 4:
        mixer.music.load(resource_path("Manual Labour 4.wav"))
    mixer.music.set_volume(1)
    mixer.music.play(-1)

    while mining:

        minerals_mined = 0
        minerals_to_mine = random.randint(1, 3) * 5

        minerals_mined = mine_minerals(minerals_mined, minerals_to_mine)
        num_of_boxes = minerals_mined // 5
        days_in_prison += 1

        mixer.music.stop()
        time.sleep(0.2)
        
        return num_of_boxes









def day3_Warehouse(num_of_lumber, num_of_boxes):
    
    global days_in_prison
    warehouse_ing = True
    next_item_input = 'Q'
    pygame.display.set_caption(f"Day {days_in_prison} - Warehouse")

    lumber_image = pygame.image.load(resource_path("warehouse - lumber.png"))
    lumber_image = pygame.transform.scale(lumber_image, (1280, 480))
    box_image = pygame.image.load(resource_path("warehouse - box of goods.png"))
    box_image = pygame.transform.scale(box_image, (1280, 480))

    def sort_items(items_left):
        
        current_item = empty_space # set default value to avoid crashing
        current_image = graphics[0]

        item_sorted = False
        finished_with_current_item = False

        while len(items_left) > 0 or finished_with_current_item == False:
            
            finished_with_current_item = False

            screen.fill('black')

            if item_sorted == False:
                if len(items_left) == 1:
                    text1 = font1.render(f"There is {len(items_left)} more item for you to sort!", True, (255, 255, 255))
                else:
                    text1 = font1.render(f"There are {len(items_left)} more items for you to sort!", True, (255, 255, 255))
            else:
                text1 = font1.render(f"Item you picked up: {current_item.name}!", True, (255, 255, 255))
                
            if item_sorted == False:
                text2 = font1.render(f"Press {next_item_input} to get next item:", True, (255, 255, 255))
                text2_rect = text2.get_rect()
                text2_rect.topleft = (5, 515)
            elif item_sorted == True and empty_space in inventory:
                text2 = take_item
                text2_rect = text2.get_rect()
                text2_rect.topleft = (5, 535)
            else:
                text2 = font1.render("FULL INVENTORY", True, (255, 255, 255))
                text2_rect = text2.get_rect()
                text2_rect.topleft = (5, 535)

            text3 = font1.render(f"Press W to put {current_item.name} with the other {current_item.category}:", True, (255, 255, 255))

            text1_rect = text1.get_rect()
            text3_rect = text3.get_rect()
            text1_rect.topleft = (5, 485)
            text3_rect.topleft = (5, 565)

            item_desc = font2.render(f"({current_item.desc})", True, (200, 200, 200))
            item_rect = item_desc.get_rect()
            item_rect.topleft = (5, 515)

            for i in range(text_emphasis):
                screen.blit(text1, text1_rect)
                screen.blit(text2, text2_rect)
                if item_sorted == True:
                    screen.blit(current_image, (0, 0))
                    screen.blit(text3, text3_rect)
                    screen.blit(item_desc, item_rect)
                show_inventory(inventory, "INVENTORY:")
            line_separating_text_and_images()
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                else:
                    if event.type == KEYDOWN:
                        if event.key == K_q and item_sorted == False:
                            current_item = (items_left.pop(0))
                            current_image = (graphics.pop(0))
                            item_name = current_item.name
                            item_desc = current_item.desc
                            item_sorted = True

                            random_sfx = random.randint(1, 2)
                            if current_item == lumber:
                                if random_sfx == 1:
                                    mixer.Channel(0).play(mixer.Sound(resource_path('SFX Warehouse Lumber 1.wav')))
                                elif random_sfx == 2:
                                    mixer.Channel(0).play(mixer.Sound(resource_path('SFX Warehouse Lumber 2.wav')))
                            elif current_item == box_of_goods:
                                if random_sfx == 1:
                                    mixer.Channel(0).play(mixer.Sound(resource_path('SFX Warehouse Box 1.wav')))
                                elif random_sfx == 2:
                                    mixer.Channel(0).play(mixer.Sound(resource_path('SFX Warehouse Box 2.wav')))
                                
                        if event.key == K_x and item_sorted == True and empty_space in inventory:
                            for i in range(len(inventory)):
                                if inventory[i] == empty_space:
                                    inventory[i] = current_item
                                    break
                            item_sorted = False
                            finished_with_current_item = True
                        elif event.key == K_w and item_sorted == True:
                            item_sorted = False
                            finished_with_current_item = True
                            
                pygame.display.flip()

        # SHIFT TO CONTINUE #
        while True:
            
            screen.fill('black')
            
            text1 = font1.render(f"There are {len(items_left)} items to sort!", True, (255, 255, 255))
            
            text1_rect = text1.get_rect()
            text1_rect.topleft = (0, 485)

            line_separating_text_and_images()

            for i in range(text_emphasis):
                screen.blit(text1, text1_rect)
                screen.blit(shift_text, shift_rect)
                show_inventory(inventory, "INVENTORY:")
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                else:
                    if event.type == KEYDOWN:
                        if event.key == K_LSHIFT or event.key == K_RSHIFT:
                            return None
                pygame.display.flip()

    rng = random.randint(1, 4)
    if rng == 1:
        mixer.music.load(resource_path("Manual Labour 1.wav"))
    elif rng == 2:
        mixer.music.load(resource_path("Manual Labour 2.wav"))
    elif rng == 3:
        mixer.music.load(resource_path("Manual Labour 3.wav"))
    elif rng == 4:
        mixer.music.load(resource_path("Manual Labour 4.wav"))
    mixer.music.set_volume(1)
    mixer.music.play(-1)
        
    while warehouse_ing:
        
        items_left = []
        graphics = []

        for i in range(num_of_lumber):
            items_left.append(lumber)
            graphics.append(lumber_image)
        for i in range(num_of_boxes):
            items_left.append(box_of_goods)
            graphics.append(box_image)

        sort_items(items_left)
        days_in_prison += 1

        mixer.music.stop()
        time.sleep(0.2)
        
        return None










def day4_Fishing():
    
    global days_in_prison
    fishing = True
    cast_net_input = 'Q'
    reel_net_input = 'W'
    pygame.display.set_caption(f"Day {days_in_prison} - Fishing")

    def fish(fish_caught, fish_to_catch):

        num_of_fish_in_net = 0
        used_net = False
        net_casted = False
        net_reeled = True

        frame1 = pygame.image.load(resource_path('kitchen animation f5.png')) # This frame is a black image, so I can reuse it both here and for day 5
        frame1 = pygame.transform.scale(frame1, (1280, 480))
        
        frame2 = pygame.image.load(resource_path('fishing animation f1.png'))
        frame2 = pygame.transform.scale(frame2, (1280, 480))
        
        frame3 = pygame.image.load(resource_path('fishing animation f2.png'))
        frame3 = pygame.transform.scale(frame3, (1280, 480))
        
        frame4 = pygame.image.load(resource_path('fishing animation f3.png'))
        frame4 = pygame.transform.scale(frame4, (1280, 480))
        
        frame5 = pygame.image.load(resource_path('fishing animation f4.png'))
        frame5 = pygame.transform.scale(frame5, (1280, 480))
        
        frame6 = pygame.image.load(resource_path('fishing animation f5.png'))
        frame6 = pygame.transform.scale(frame6, (1280, 480))
        
        frame7 = pygame.image.load(resource_path('fishing animation f6.png'))
        frame7 = pygame.transform.scale(frame7, (1280, 480))
        
        frame8 = pygame.image.load(resource_path('fishing animation f7.png'))
        frame8 = pygame.transform.scale(frame8, (1280, 480))
        
        frame9 = pygame.image.load(resource_path('fishing animation f8.png'))
        frame9 = pygame.transform.scale(frame9, (1280, 480))
        
        frame10 = pygame.image.load(resource_path('fishing animation f9.png'))
        frame10 = pygame.transform.scale(frame10, (1280, 480))
        
        frame11 = pygame.image.load(resource_path('fishing animation f10.png'))
        frame11 = pygame.transform.scale(frame11, (1280, 480))
        
        frame12 = pygame.image.load(resource_path('fishing animation f11.png'))
        frame12 = pygame.transform.scale(frame12, (1280, 480))
        
        frame13 = pygame.image.load(resource_path('fishing animation f12.png'))
        frame13 = pygame.transform.scale(frame13, (1280, 480))
        
        frame14 = pygame.image.load(resource_path('fishing animation f13.png'))
        frame14 = pygame.transform.scale(frame14, (1280, 480))

        class Fishing_Animation(pygame.sprite.Sprite):
            def __init__(self):
                super().__init__()
                self.part1 = [frame1, frame2, frame3, frame4, frame5, frame6, frame7, frame8, frame9]
                self.part2 = [frame10, frame11, frame12, frame13, frame14, frame1]
                self.is_animating = False
                self.current_frame = 0
                self.image = frame1

                self.rect = self.image.get_rect()
                self.rect.topleft = (0, 0)

            def animate(self):
                self.current_frame = 0
                self.is_animating = True

            def update(self):
                    
                if self.is_animating == True:
                    self.current_frame += 0.25

                    if self.current_frame >= len(self.part1) and net_reeled == False:
                        self.current_frame = 8
                        self.is_animating = False
                    if self.current_frame >= len(self.part2) and net_casted == False:
                        self.current_frame = 5
                        self.is_animating = False

                    if net_casted == False:
                        self.image = self.part2[int(self.current_frame)]
                    elif net_reeled == False:
                        self.image = self.part1[int(self.current_frame)]

        animations = pygame.sprite.Group()

        fish_anim = Fishing_Animation()
        animations.add(fish_anim)
        
        while True:

            random_cast = random.randint(1, 3)
            random_reel = random.randint(1, 3)

            if random_cast == 1:
                sfxcast = mixer.Sound(resource_path('SFX Cast Net 1.wav'))
            elif random_cast == 2:
                sfxcast = mixer.Sound(resource_path('SFX Cast Net 2.wav'))
            elif random_cast == 3:
                sfxcast = mixer.Sound(resource_path('SFX Cast Net 3.wav'))

            if random_reel == 1:
                sfxreel = mixer.Sound(resource_path('SFX Reel Net 1.wav'))
            elif random_reel == 2:
                sfxreel = mixer.Sound(resource_path('SFX Reel Net 2.wav'))
            elif random_reel == 3:
                sfxreel = mixer.Sound(resource_path('SFX Reel Net 3.wav'))

            screen.fill('black')

            if fish_to_catch <= 0:
                text1 = font1.render(f"You don't need to catch any more fish!", True, (255, 255, 255))
            else:
                text1 = font1.render(f"You must catch {fish_to_catch} more fish!", True, (255, 255, 255))
            text2 = font1.render(f"Fish caught: {fish_caught}", True, (255, 255, 255))
            text3 = font1.render(f"Press {cast_net_input} to cast net:", True, (255, 255, 255))
            text4 = font1.render(f"Press {reel_net_input} to reel net:", True, (255, 255, 255))
            text5 = font1.render(f"You caught {num_of_fish_in_net} fish!", True, (255, 255, 255))
            
            text1_rect = text1.get_rect()
            text2_rect = text2.get_rect()
            text3_rect = text3.get_rect()
            text4_rect = text4.get_rect()
            text5_rect = text5.get_rect()
            text1_rect.topleft = (5, 485)
            text2_rect.topleft = (5, 515)
            text3_rect.topleft = (5, 545)
            text4_rect.topleft = (5, 545)
            text5_rect.topleft = (5, 575)

            line_separating_text_and_images()

            for i in range(text_emphasis):
                screen.blit(text1, text1_rect)
                screen.blit(text2, text2_rect)
                if net_reeled == True and fish_to_catch > 0:
                    screen.blit(text3, text3_rect)
                elif net_casted == True:
                    screen.blit(text4, text4_rect)
                if used_net == True and net_reeled == True:
                    screen.blit(text5, text5_rect)
                if fish_to_catch <= 0:
                    screen.blit(shift_text, shift_rect)
                show_inventory(inventory, "INVENTORY:")

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                else:   
                    if event.type == KEYDOWN:
                        if event.key == K_q and net_reeled == True and fish_to_catch > 0 and fish_anim.is_animating == False:
                            mixer.Channel(0).play(sfxcast)
                            fish_anim.animate()
                            used_net = True
                            net_casted = True
                            net_reeled = False
                        elif event.key == K_w and net_casted == True and fish_anim.is_animating == False:
                            mixer.Channel(2).play(sfxreel)
                            fish_anim.animate()
                            net_reeled = True
                            net_casted = False
                            num_of_fish_in_net = random.randint(0, 5)
                            fish_caught += num_of_fish_in_net
                            fish_to_catch -= num_of_fish_in_net
                        elif (event.key == K_LSHIFT or event.key == K_RSHIFT) and fish_to_catch <= 0:
                            return fish_caught
                            
            animations.draw(screen)
            animations.update()
            pygame.display.update()
            clock.tick(50)


    rng = random.randint(1, 4)
    if rng == 1:
        mixer.music.load(resource_path("Manual Labour 1.wav"))
    elif rng == 2:
        mixer.music.load(resource_path("Manual Labour 2.wav"))
    elif rng == 3:
        mixer.music.load(resource_path("Manual Labour 3.wav"))
    elif rng == 4:
        mixer.music.load(resource_path("Manual Labour 4.wav"))
    mixer.music.set_volume(1)
    mixer.music.play(-1)
                
    while fishing:
        fish_caught = 0
        fish_to_catch = random.randint(3, 5) * 5

        fish_caught = fish(fish_caught, fish_to_catch)
        num_of_dishes = fish_caught // 5
        days_in_prison += 1

        mixer.music.stop()
        time.sleep(0.2)
        
        return num_of_dishes











def day5_Kitchen(num_of_dishes):

    rng = random.randint(1, 4)
    if rng == 1:
        mixer.music.load(resource_path("Manual Labour 1.wav"))
    elif rng == 2:
        mixer.music.load(resource_path("Manual Labour 2.wav"))
    elif rng == 3:
        mixer.music.load(resource_path("Manual Labour 3.wav"))
    elif rng == 4:
        mixer.music.load(resource_path("Manual Labour 4.wav"))
    mixer.music.set_volume(1)
    mixer.music.play(-1)

    global days_in_prison
    pygame.display.set_caption(f"Day {days_in_prison} - Kitchen")

    main_options = True
    use_item_options = False
    take_item_options = False
    list_of_dishes = []

    current_dish = None

    for i in range(num_of_dishes):
        list_of_dishes.append(prisoner_dish)
    
    item_taken = None

    next_dish = True # Flag variable to check if the player has moved onto serving the next dish.
    takeable_items = [butter_knife, cake_fork]
    
    def hide_knife():
        pygame.draw.rect(screen, (0, 0, 0), pygame.Rect(0, 0, 440, 478))
    def hide_fork():
        pygame.draw.rect(screen, (0, 0, 0), pygame.Rect((screen_width)-440, 0, 600, 478))

    frame1 = pygame.image.load(resource_path('kitchen animation f1.png'))
    frame1 = pygame.transform.scale(frame1, (1280, 480))
    frame2 = pygame.image.load(resource_path('kitchen animation f2.png'))
    frame2 = pygame.transform.scale(frame2, (1280, 480))
    frame3 = pygame.image.load(resource_path('kitchen animation f3.png'))
    frame3 = pygame.transform.scale(frame3, (1280, 480))
    frame4 = pygame.image.load(resource_path('kitchen animation f4.png'))
    frame4 = pygame.transform.scale(frame4, (1280, 480))
    frame5 = pygame.image.load(resource_path('kitchen animation f5.png'))
    frame5 = pygame.transform.scale(frame5, (1280, 480))
    frame6 = pygame.image.load(resource_path('kitchen animation f6.png'))
    frame6 = pygame.transform.scale(frame6, (1280, 480))
    frame7 = pygame.image.load(resource_path('kitchen animation f7.png'))
    frame7 = pygame.transform.scale(frame7, (1280, 480))
    frame8 = pygame.image.load(resource_path('kitchen animation f8.png'))
    frame8 = pygame.transform.scale(frame8, (1280, 480))

    class Kitchen_Animation(pygame.sprite.Sprite):
        def __init__(self):
            super().__init__()
            self.part1 = [frame1, frame2, frame3, frame4, frame5]
            self.all = [frame1, frame2, frame3, frame4, frame5, frame6, frame7, frame8, frame1]
            self.is_animating = False
            self.hidden_knife = False
            self.hidden_fork = False
            self.current_frame = 0
            self.image = frame1

            self.rect = self.image.get_rect()
            self.rect.topleft = (0, 0)

        def animate(self):
            self.current_frame = 0
            self.is_animating = True

        def update(self):
            
            if self.is_animating == True:
                self.current_frame += 0.25

                if self.current_frame >= 5:
                    self.hidden_knife = False
                    self.hidden_fork = False

                if self.current_frame >= 9 and len(list_of_dishes) > 0:
                    self.current_frame = 0
                    self.is_animating = False
                if self.current_frame >= 5 and len(list_of_dishes) <= 0:
                    self.current_frame = 4
                    self.is_animating = False

                if len(list_of_dishes) > 0:
                    self.image = self.all[int(self.current_frame)]
                elif len(list_of_dishes) <= 0:
                    self.image = self.part1[int(self.current_frame)]
                    
    animations = pygame.sprite.Group()

    kitch_anim = Kitchen_Animation()
    animations.add(kitch_anim)

    while True:

        random_sfx = random.randint(1, 2)
        if random_sfx == 1:
            cutlery_sfx = mixer.Sound(resource_path('SFX Cutlery 1.wav'))
        else:
            cutlery_sfx = mixer.Sound(resource_path('SFX Cutlery 2.wav'))

        random_sfx = random.randint(1, 3)
        if random_sfx == 1:
            dish_sfx = mixer.Sound(resource_path('SFX Serve Dish 1.wav'))
        elif random_sfx == 2:
            dish_sfx = mixer.Sound(resource_path('SFX Serve Dish 2.wav'))
        else:
            dish_sfx = mixer.Sound(resource_path('SFX Serve Dish 3.wav'))

        if next_dish == True:
            takeable_items = [butter_knife, cake_fork]
            next_dish = False

        if len(list_of_dishes) <= 0:
            current_dish = None
        else:
            current_dish = list_of_dishes[0]

        if take_item_options == True:
            if item_taken == None:
                text1 = font1.render("Press the corresponding number to take item:", True, (255, 255, 255))
            elif item_taken == empty_space:
                text1 = font1.render("Can't take something that isn't there.", True, (255, 255, 255))
            else:
                text1 = font1.render(f"You took the {item_taken.name}.", True, (255, 255, 255))
        else:
            if len(list_of_dishes) == 1:
                text1 = font1.render(f"You have {len(list_of_dishes)} dish left to serve.", True, (255, 255, 255))
            else:
                text1 = font1.render(f"You have {len(list_of_dishes)} dishes left to serve.", True, (255, 255, 255))

        if take_item_options == True:
            text2 = font1.render("[1] " + takeable_items[0].name, True, (255, 255, 255))
        else:
            text2 = font1.render("Press Q to serve dish:", True, (255, 255, 255))

        if take_item_options == True:
            text3 = font1.render("[2] " + takeable_items[1].name, True, (255, 255, 255))
        else:
            if empty_space not in inventory:
                text3 = font1.render("FULL INVENTORY", True, (255, 255, 255))
            else:
                text3 = take_item
            
        text1_rect = text1.get_rect()
        text2_rect = text2.get_rect()
        text3_rect = text3.get_rect()
        text1_rect.topleft = (5, 485)
        text2_rect.topleft = (5, 515)
        if take_item_options == True:
            text3_rect.topleft = (5, 545)
        else:
            text3_rect.topleft = (5, 575)

            
        screen.fill('black')
            
        for i in range(text_emphasis):
            screen.blit(text1, text1_rect)
            if len(list_of_dishes) > 0:
                screen.blit(text2, text2_rect)
                screen.blit(text3, text3_rect)
            if len(list_of_dishes) <= 0:
                screen.blit(shift_text, shift_rect)
            if take_item_options == True:
                screen.blit(go_back, go_back_rect)
            show_inventory(inventory, "INVENTORY:")
        line_separating_text_and_images()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            else:
                if event.type == KEYDOWN:
                    if event.key == K_0 and main_options == False:
                        use_item_options = False
                        take_item_options = False
                        main_options = True
                        item_taken = None
                    if event.key == K_x and main_options == True and empty_space in inventory and len(list_of_dishes) > 0:
                        take_item_options = True
                        main_options = False
                    if event.key == K_q and main_options == True and kitch_anim.is_animating == False and len(list_of_dishes) > 0:
                        del list_of_dishes[0]
                        next_dish = True
                        mixer.Channel(2).play(dish_sfx)
                        kitch_anim.animate()
                    if event.key == K_LSHIFT or event.key == K_RSHIFT and len(list_of_dishes) <= 0:
                        days_in_prison += 1
                        mixer.music.stop()
                        time.sleep(0.2)
                        return None

                    ## Take items ##
                    if event.key == K_1 and take_item_options == True:
                        item_taken = takeable_items[0]
                        for i in range(len(inventory)):
                            if inventory[i] == empty_space:
                                inventory[i] = takeable_items[0]
                                takeable_items[0] = empty_space
                                kitch_anim.hidden_knife = True
                                mixer.Channel(0).play(cutlery_sfx)
                                break
                        if empty_space not in inventory:
                            take_item_options = False
                            main_options = True
                            item_taken = None
                    if event.key == K_2 and take_item_options == True:
                        item_taken = takeable_items[1]
                        for i in range(len(inventory)):
                            if inventory[i] == empty_space:
                                inventory[i] = takeable_items[1]
                                takeable_items[1] = empty_space
                                kitch_anim.hidden_fork = True
                                mixer.Channel(0).play(cutlery_sfx)
                                break
                        if empty_space not in inventory:
                            take_item_options = False
                            main_options = True
                            item_taken = None

        animations.draw(screen)
        if kitch_anim.hidden_knife == True and kitch_anim.hidden_fork == True:
            hide_fork()
            hide_knife()
        elif kitch_anim.hidden_knife == True and kitch_anim.hidden_fork == False:
            hide_knife()
        elif kitch_anim.hidden_knife == False and kitch_anim.hidden_fork == True:
            hide_fork()
        animations.update()
        pygame.display.flip()
        clock.tick(60)










def day6_Laundry():
    
    global days_in_prison
    laundry_ing = True
    next_item_input = 'Q'
    pygame.display.set_caption(f"Day {days_in_prison} - Laundry")

    jumpsuit_image = pygame.image.load(resource_path("laundry - prisoner jumpsuit.png"))
    jumpsuit_image = pygame.transform.scale(jumpsuit_image, (1280, 480))
    coat_image = pygame.image.load(resource_path("laundry - officers coat.png"))
    coat_image = pygame.transform.scale(coat_image, (1280, 480))
    hat_image = pygame.image.load(resource_path("laundry - officers hat.png"))
    hat_image = pygame.transform.scale(hat_image, (1280, 480))
    bedsheet_image = pygame.image.load(resource_path("laundry - bedsheet.png"))
    bedsheet_image = pygame.transform.scale(bedsheet_image, (1280, 480))
    pillowcase_image = pygame.image.load(resource_path("laundry - pillowcase.png"))
    pillowcase_image = pygame.transform.scale(pillowcase_image, (1280, 480))

    def wash_laundry(laundry_left):

        global take
        current_item = empty_space # set default value to avoid crashing
        current_image = graphics_left[0]

        item_washed = False
        finished_with_current_item = False

        while len(laundry_left) > 0 or finished_with_current_item == False:
            
            finished_with_current_item = False

            screen.fill('black')

            if item_washed == False:
                text1 = font1.render(f"There are {len(laundry_left)} items to wash!", True, (255, 255, 255))
            else:
                text1 = font1.render(f"Item you just washed: {current_item.name}!", True, (255, 255, 255))
                
            if item_washed == False:
                text2 = font1.render(f"Press {next_item_input} to wash next item:", True, (255, 255, 255))
                text2_rect = text2.get_rect()
                text2_rect.topleft = (5, 515)
            elif item_washed == True and empty_space in inventory:
                text2 = take_item
                text2_rect = text2.get_rect()
                text2_rect.topleft = (5, 535)
            else:
                text2 = font1.render("FULL INVENTORY", True, (255, 255, 255))
                text2_rect = text2.get_rect()
                text2_rect.topleft = (5, 535)

            text3 = font1.render(f"Press W to move item to collecting:", True, (255, 255, 255))

            text1_rect = text1.get_rect()
            text3_rect = text3.get_rect()
            text1_rect.topleft = (5, 485)
            text3_rect.topleft = (5, 565)

            item_desc = font2.render(f"({current_item.desc})", True, (200, 200, 200))
            item_rect = item_desc.get_rect()
            item_rect.topleft = (5, 515)

            for i in range(text_emphasis):
                screen.blit(text1, text1_rect)
                screen.blit(text2, text2_rect)
                if item_washed == True:
                    screen.blit(current_image, (0, 0))
                    screen.blit(text3, text3_rect)
                    screen.blit(item_desc, item_rect)
                show_inventory(inventory, "INVENTORY:")
            line_separating_text_and_images()
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                else:
                    if event.type == KEYDOWN:
                        if event.key == K_q and item_washed == False:
                            current_item = (laundry_left.pop(0))
                            current_image = (graphics_left.pop(0))
                            item_name = current_item.name
                            item_desc = current_item.desc
                            item_washed = True

                            if current_item == officers_hat:
                                mixer.Channel(0).play(mixer.Sound(resource_path('SFX Laundry 3.wav')))
                            else:
                                random_sfx = random.randint(1, 2)
                                if random_sfx == 1:
                                   mixer.Channel(0).play(mixer.Sound(resource_path('SFX Laundry 1.wav')))
                                else:
                                    mixer.Channel(0).play(mixer.Sound(resource_path('SFX Laundry 2.wav')))
                                    
                        if event.key == K_x and item_washed == True and empty_space in inventory:
                            for i in range(len(inventory)):
                                if inventory[i] == empty_space:
                                    inventory[i] = current_item
                                    break
                            item_washed = False
                            finished_with_current_item = True
                        elif event.key == K_w and item_washed == True:
                            item_washed = False
                            finished_with_current_item = True
                            
            pygame.display.flip()
            

        # SHIFT TO CONTINUE #
        while True:
            
            screen.fill('black')
            
            text1 = font1.render(f"There are {len(laundry_left)} items to wash!", True, (255, 255, 255))
            
            text1_rect = text1.get_rect()
            text1_rect.topleft = (0, 485)

            line_separating_text_and_images()

            for i in range(text_emphasis):
                screen.blit(text1, text1_rect)
                screen.blit(shift_text, shift_rect)
                show_inventory(inventory, "INVENTORY:")
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                else:
                    if event.type == KEYDOWN:
                        if event.key == K_LSHIFT or event.key == K_RSHIFT:
                            return None
                pygame.display.flip()
                
    rng = random.randint(1, 4)
    if rng == 1:
        mixer.music.load(resource_path("Manual Labour 1.wav"))
    elif rng == 2:
        mixer.music.load(resource_path("Manual Labour 2.wav"))
    elif rng == 3:
        mixer.music.load(resource_path("Manual Labour 3.wav"))
    elif rng == 4:
        mixer.music.load(resource_path("Manual Labour 4.wav"))
    mixer.music.set_volume(1)
    mixer.music.play(-1)

    while laundry_ing:

        list_of_possible_laundry = [prisoner_jumpsuit, prisoner_jumpsuit, prisoner_jumpsuit, officers_coat, officers_hat, bedsheet,       pillowcase,      pillowcase]
        list_of_graphics =         [jumpsuit_image,    jumpsuit_image,    jumpsuit_image,    coat_image,    hat_image,    bedsheet_image, pillowcase_image, pillowcase_image]
        laundry_left = []
        graphics_left = []

        for i in range(10):
            laundry_item = random.randint(0, len(list_of_possible_laundry)-1)
            laundry_left.append(list_of_possible_laundry[laundry_item])
            graphics_left.append(list_of_graphics[laundry_item])

        wash_laundry(laundry_left)
        days_in_prison += 1

        mixer.music.stop()
        time.sleep(0.2)
        
        return None










def bruce():

    global accessories
    
    mixer.music.load(resource_path("Spotted.wav"))
    mixer.music.set_volume(0.5)

    bruce_image = pygame.image.load(resource_path("bruce.png"))
    bruce_image = pygame.transform.scale(bruce_image, (1280, 480))
    bruce_afraid = pygame.image.load(resource_path("bruce afraid.png"))
    bruce_afraid = pygame.transform.scale(bruce_afraid, (1280, 480))
    bruce_disappointed = pygame.image.load(resource_path("bruce disappointed.png"))
    bruce_disappointed = pygame.transform.scale(bruce_disappointed, (1280, 480))
    
    count = 1

    if len(accessories) > 0:

        while count < 2:

            screen.fill('black')
            line_separating_text_and_images()
            
            text1 = font1.render("Bruce turns a blind eye to your totally legitimate uniform!", True, (255, 255, 255))                    

            text1_rect = text1.get_rect()
            text1_rect.topleft = (5, 485)
            shift_rect.bottomleft = (0, 720)

            for i in range(text_emphasis):
                screen.blit(text1, text1_rect)
                screen.blit(shift_text, shift_rect)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                else:
                    if event.type == KEYDOWN:
                        if event.key == K_LSHIFT or event.key == K_RSHIFT:
                            count += 1
                pygame.display.flip()

    elif doorknob in inventory:

        mixer.music.play()

        while count < 3:

            screen.fill('black')
            line_separating_text_and_images()

            if count == 1:
                text1 = font1.render("BRUCE: Bruce wants something from you! Give it!", True, (255, 255, 255))
                screen.blit(bruce_image, (0, 0))
            elif count == 2:
                text1 = font1.render("BRUCE: OH F**K! THAT'S A DOORKNOB! GET AWAY! GET AWAY!", True, (255, 255, 255))
                screen.blit(bruce_afraid, (0, 0))

            text1_rect = text1.get_rect()
            text1_rect.topleft = (5, 485)
            shift_rect.bottomleft = (0, 720)

            for i in range(text_emphasis):
                screen.blit(text1, text1_rect)
                screen.blit(shift_text, shift_rect)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                else:
                    if event.type == KEYDOWN:
                        if event.key == K_LSHIFT or event.key == K_RSHIFT:
                            count += 1
                pygame.display.flip()

    elif inventory.count(empty_space) == 5:

        mixer.music.play()

        while count < 3:

            screen.fill('black')
            line_separating_text_and_images()

            if count == 1:
                text1 = font1.render("BRUCE: Bruce wants something from you! Give it!", True, (255, 255, 255))
                screen.blit(bruce_image, (0, 0))
            elif count == 2:
                text1 = font1.render("BRUCE: Wait, you have NOTHING?! Bruce lets you off this time...", True, (255, 255, 255))
                screen.blit(bruce_disappointed, (0, 0))

            text1_rect = text1.get_rect()
            text1_rect.topleft = (5, 485)
            shift_rect.bottomleft = (0, 720)

            for i in range(text_emphasis):
                screen.blit(text1, text1_rect)
                screen.blit(shift_text, shift_rect)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                else:
                    if event.type == KEYDOWN:
                        if event.key == K_LSHIFT or event.key == K_RSHIFT:
                            count += 1
                pygame.display.flip()
        
                
    else:

        mixer.music.play()
        
        while count < 4:

            screen.fill('black')
            line_separating_text_and_images()
            
            if count == 1:
                text1 = font1.render("BRUCE: Bruce wants something from you! Give it!", True, (255, 255, 255))
                text1_rect = text1.get_rect()
                text1_rect.topleft = (5, 485)
            elif count == 3:
                text1 = font1.render("BRUCE: Thanks for the item, chump!", True, (255, 255, 255))
                text1_rect = text1.get_rect()
                text1_rect.topleft = (5, 485)
            
            shift_rect.bottomleft = (0, 720)
            screen.blit(bruce_image, (0, 0))
            
            if count == 2:
                show_interactable_inventory(inventory, "Give an item to Bruce:", "", False)
            
            for i in range(text_emphasis):
                if count != 2:
                    screen.blit(text1, text1_rect)
                    screen.blit(shift_text, shift_rect)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                else:
                    if event.type == KEYDOWN:
                        if event.key == K_LSHIFT or event.key == K_RSHIFT and count != 2:
                            count += 1
                        if event.key == K_1 and count == 2 and inventory[0] != empty_space:
                            inventory[0] = empty_space
                            count += 1
                        if event.key == K_2 and count == 2 and inventory[1] != empty_space:
                            inventory[1] = empty_space
                            count += 1
                        if event.key == K_3 and count == 2 and inventory[2] != empty_space:
                            inventory[2] = empty_space
                            count += 1
                        if event.key == K_4 and count == 2 and inventory[3] != empty_space:
                            inventory[3] = empty_space
                            count += 1
                        if event.key == K_5 and count == 2 and inventory[4] != empty_space:
                            inventory[4] = empty_space
                            count += 1
                pygame.display.flip()





def day7_Courtyard():

    global days_in_prison
    pygame.display.set_caption(f"Day {days_in_prison} - Free Time")

    leave_courtyard = False

    unoccupied = True
    talk_to_theo = False
    talk_to_sid = False
    talk_to_craig = False

    craig_image = pygame.image.load(resource_path("craig.png"))
    craig_image = pygame.transform.scale(craig_image, (1280, 480))
    sid_image = pygame.image.load(resource_path("sid.png"))
    sid_image = pygame.transform.scale(sid_image, (1280, 480))
    theo_image = pygame.image.load(resource_path("theo.png"))
    theo_image = pygame.transform.scale(theo_image, (1280, 480))

    if days_in_prison > 70:
        theos_time = 'pretty soon'
    elif 70 >= days_in_prison > 40:
        theos_time = 'in a month'
    else:
        theos_time = 'in a couple of months'

    list_of_line1 = ["THEO: Hello.",
                     "THEO: There are so many floors to this prison! I bet you'd need a parachute to jump",
                     "THEO: How come no officers watch people on kitchen duty? There have been quite a ",
                     "THEO: The most popular method of escaping I've been told is through the vents, but ",
                     "THEO: Apparently the walkway that goes up to the roof has collapsed. I bet some ",
                     "THEO: I heard Bruce has an extreme fear of doorknobs.",
                     "THEO: Everyone here is so stupid. I bet you could walk around wearing even just half",
                     "THEO: An inmate tried climbing through the vents in the dark a few years ago. He got",
                     "THEO: Someone was viciously spreading leprosy around here a few months back. Don't ",
                     "THEO: The fact Sid and Craig are willing to stay in prison to help others escape is ",
                     "THEO: I would've definitely broken out of this hellhole by now, but I'll have done  "]
    list_of_line2 = ["",
                     "from the roof to the ground without dying.",
                     "few stabbings due to people taking the cutlery!",
                     "what item would be thin enough to let you unscrew it from the wall?",
                     "sneaky escapist is still gonna find a way past it though.",
                     "",
                     "of an officer's uniform and it would take people a while to catch on!",
                     "stuck and died. We were all put on lockdown for a week while they found the body.",
                     "worry, it's been sorted now.",
                     "truly respectable.",
                     f"my time {theos_time} and would rather not risk extending it again."]

    if len(accessories) == 1 and officers_coat in accessories:
        list_of_line1[6] = "THEO: Nice coat. If only you had a hat as well."
        list_of_line2[6] = ""
    elif len(accessories) == 1 and officers_hat in accessories:
        list_of_line1[6] = "THEO: Nice hat. If only you had a coat as well."
        list_of_line2[6] = ""
    elif len(accessories) >= 2:
        list_of_line1[6] = "THEO: Nice uniform. "
        list_of_line2[6] = ""
    
    discussion = 0
    item_bought = None
    item_crafted = None
    
    mixer.music.load(resource_path("Courtyard Discussions.wav"))
    mixer.music.set_volume(0.25)
    mixer.music.play(-1)

    while leave_courtyard == False:

        screen.fill('black')
        line_separating_text_and_images()

        if unoccupied == True:
            text1 = font1.render("Press A to talk to Theo:", True, (255, 255, 255))
            text2 = font1.render("Press S to talk to Sid:", True, (255, 255, 255))
            text3 = font1.render("Press D to talk to Craig:", True, (255, 255, 255))
            text4 = font1.render("", True, (255, 255, 255))
        elif talk_to_theo == True:
            if days_in_prison < 100:
                screen.blit(theo_image, (0, 0))
                text1 = font1.render(list_of_line1[discussion], True, (255, 255, 255))
                text2 = font1.render(list_of_line2[discussion], True, (255, 255, 255))
                text3 = font1.render("", True, (255, 255, 255))
                text4 = font1.render("[Q] Talk", True, (255, 255, 255))
            else:
                text1 = font1.render("Theo is not here. Seems he's done his time.", True, (255, 255, 255))
                text2 = font1.render("", True, (255, 255, 255))
                text3 = font1.render("", True, (255, 255, 255))
                text4 = font1.render("", True, (255, 255, 255))
        elif talk_to_sid == True:
            screen.blit(sid_image, (0, 0))
            if item_bought == None:
                text1 = font1.render("SID: Which o' these stolen possessions would ya like?", True, (255, 255, 255))
            else:
                text1 = font1.render(f"SID: {item_bought.desc}", True, (255, 255, 255))
            text2 = font1.render("[1] SCREWDRIVER.......(wants BOX OF GOODS)", True, (255, 255, 255))
            text3 = font1.render("[2] TORCH.............(wants PRISONER JUMPSUIT)", True, (255, 255, 255))
            text4 = font1.render("[3] DOORKNOB..........(wants BUTTER KNIFE/CAKE FORK)", True, (255, 255, 255))
        elif talk_to_craig == True:
            screen.blit(craig_image, (0, 0))
            if item_crafted == None:
                text1 = font1.render("CRAIG:  *sigh*  What do you want?", True, (255, 255, 255))
            else:
                text1 = font1.render(f"CRAIG: {item_crafted.desc}", True, (255, 255, 255))
            text2 = font1.render("[1] LUMBER BEAM............(need 2 LUMBER)", True, (255, 255, 255))
            text3 = font1.render("[2] PILLOWCASE PARACHUTE...(need 3 PILLOWCASES)", True, (255, 255, 255))
            text4 = font1.render("[3] BEDSHEET PARACHUTE.....(need 2 BEDSHEETS)", True, (255, 255, 255))

        if unoccupied == True:
            go_back = font1.render("Press 0 to leave courtyard:", True, (255, 255, 255))
        else:
            go_back = font1.render("Press 0 to go back:", True, (255, 255, 255))

        for i in range(text_emphasis):
            screen.blit(text1, (10, 485))
            screen.blit(text2, (10, 511))
            screen.blit(text3, (10, 537))
            screen.blit(text4, (10, 563))
            screen.blit(go_back, go_back_rect)
            if talk_to_sid == True or talk_to_craig == True:
                show_inventory(inventory, "INVENTORY: ")

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            else:
                if event.type == KEYDOWN:
                    
                    if event.key == K_0:
                        if unoccupied == False:
                            talk_to_theo = False
                            talk_to_sid = False
                            talk_to_craig = False
                            unoccupied = True
                            item_bought = None
                            item_crafted = None
                        else:
                            leave_courtyard = True
                            days_in_prison += 1
                            mixer.music.stop()
                            time.sleep(0.2)

                    # THEO #
                    if event.key == K_a and unoccupied == True:
                        unoccupied = False
                        talk_to_theo = True
                        discussion = 0
                    if event.key == K_q and talk_to_theo == True and days_in_prison < 100:
                        discussion += 1
                        if discussion >= len(list_of_line1):
                            discussion = 1

                    # SID #
                    if event.key == K_s and unoccupied == True:
                        unoccupied = False
                        talk_to_sid = True
                    if event.key == K_1 and talk_to_sid == True and box_of_goods in inventory:
                        mixer.Channel(0).play(mixer.Sound(resource_path('SFX Cutlery 2.wav')))
                        for i in range(len(inventory)):
                            if inventory[i] == box_of_goods:
                                inventory[i] = screwdriver
                                item_bought = screwdriver
                                break
                    if event.key == K_2 and talk_to_sid == True and prisoner_jumpsuit in inventory:
                        mixer.Channel(0).play(mixer.Sound(resource_path('SFX Laundry 2.wav')))
                        for i in range(len(inventory)):           # Replaces first jumpsuit with torch.
                            if inventory[i] == prisoner_jumpsuit:
                                inventory[i] = torch
                                item_bought = torch
                                break
                    if event.key == K_3 and talk_to_sid == True and (butter_knife in inventory or cake_fork in inventory):
                        mixer.Channel(0).play(mixer.Sound(resource_path('SFX Warehouse Box 1.wav')))
                        for i in range(len(inventory)):
                            if inventory[i] == butter_knife or inventory[i] == cake_fork:
                                inventory[i] = doorknob
                                item_bought = doorknob
                                break

                    # CRAIG #
                    if event.key == K_d and unoccupied == True:
                        unoccupied = False
                        talk_to_craig = True
                    if event.key == K_1 and talk_to_craig == True and inventory.count(lumber) >= 2:
                        mixer.Channel(0).play(mixer.Sound(resource_path('SFX Warehouse Lumber 1.wav')))
                        for i in range(len(inventory)):
                            if inventory[i] == lumber:
                                inventory[i] = lumber_beam
                                item_crafted = lumber_beam
                                break
                        for i in range(len(inventory)):
                            if inventory[i] == lumber:
                                inventory[i] = empty_space
                                break
                    if event.key == K_2 and talk_to_craig == True and inventory.count(pillowcase) >= 3:
                        mixer.Channel(0).play(mixer.Sound(resource_path('SFX Laundry 1.wav')))
                        for i in range(len(inventory)):
                            if inventory[i] == pillowcase:
                                inventory[i] = pillowcase_parachute
                                item_crafted = pillowcase_parachute
                                break
                        for j in range(2):
                            for i in range(len(inventory)):
                                if inventory[i] == pillowcase:
                                    inventory[i] = empty_space
                                    break
                    if event.key == K_3 and talk_to_craig == True and inventory.count(bedsheet) >= 2:
                        mixer.Channel(0).play(mixer.Sound(resource_path('SFX Laundry 2.wav')))
                        for i in range(len(inventory)):
                            if inventory[i] == bedsheet:
                                inventory[i] = bedsheet_parachute
                                item_crafted = bedsheet_parachute
                                break
                        for i in range(len(inventory)):
                            if inventory[i] == bedsheet:
                                inventory[i] = empty_space
                                break
                                
        pygame.display.update()
        








escaped = False

def escape_segment():

    global escaping
    global escaped

    pygame.display.set_caption(f"Night {days_in_prison - 1} - Escaping")

    vent1 = pygame.image.load(resource_path("vents no light.png"))
    vent1 = pygame.transform.scale(vent1, (1280, 480))
    vent2 = pygame.image.load(resource_path("vents with light.png"))
    vent2 = pygame.transform.scale(vent2, (1280, 480))
    beam1 = pygame.image.load(resource_path("beam area no beam.png"))
    beam1 = pygame.transform.scale(beam1, (1280, 480))
    beam2 = pygame.image.load(resource_path("beam area with beam.png"))
    beam2 = pygame.transform.scale(beam2, (1280, 480))
    rooftop = pygame.image.load(resource_path("rooftop.png"))
    rooftop = pygame.transform.scale(rooftop, (1280, 480))
    
    section = 1
    transition = False

    sec1_usable_items = [torch]
    sec2_usable_items = [lumber_beam]
    sec3_usable_items = [pillowcase_parachute, bedsheet_parachute]

    item_used = None

    global used_torch
    used_torch = False

    global used_beam
    used_beam = False

    global used_parachute
    used_parachute = False

    already_used_torch = False
    already_used_beam = False
    already_used_parachute = False

    main_options = True
    use_item_options = False

    go_back = font1.render("Press 0 to give up:", True, (255, 255, 255))
    
    mixer.music.load(resource_path("Escaping.wav"))
    mixer.music.set_volume(0.5)
    mixer.music.play(-1)

    def use_items(inventory, hint, image):

        global used_torch
        global used_beam
        global used_parachute

        global specific_parachute

        screen.fill('black')
        screen.blit(image, (0, 0))
        line_separating_text_and_images()

        if item_used == None:
            show_interactable_inventory(inventory, "Press the corresponding number to use item:", hint, True)
        elif item_used == empty_space:
            show_interactable_inventory(inventory, "Di- did you just try to use an empty slot as if it were an item?", hint, True)
            
        elif item_used == torch and already_used_torch == False and section == 1:
            used_torch = True
            show_interactable_inventory(inventory, "You turned on the torch you bought from Sid.", hint, True)
        elif item_used == torch and already_used_torch == True and section == 1:
            show_interactable_inventory(inventory, "You are already using a torch.", hint, True)

        elif item_used == lumber_beam and already_used_beam == False and section == 2:
            used_beam = True
            show_interactable_inventory(inventory, "You pushed the big beam so that it reaches the other side.", hint, True)
        elif item_used == lumber_beam and already_used_beam == True and section == 2:
            show_interactable_inventory(inventory, "There is already a beam here.", hint, True)

        elif item_used == pillowcase_parachute and already_used_parachute == False and section == 3:
            used_parachute = True
            specific_parachute = pillowcase_parachute
            show_interactable_inventory(inventory, "You got out the parachute put together by Craig.", hint, True)
        elif item_used == bedsheet_parachute and already_used_parachute == False and section == 3:
            used_parachute = True
            specific_parachute = bedsheet_parachute
            show_interactable_inventory(inventory, "You got out the parachute put together by Craig.", hint, True)
        elif (item_used == pillowcase_parachute or item_used == pillowcase_parachute) and already_used_parachute == True and section == 3:
            show_interactable_inventory(inventory, "You've already got out a parachute.", hint, True)
            
        elif item_used == officers_coat:
            if officers_coat not in accessories:
                show_interactable_inventory(inventory, heading, hint, True)
            else:
                show_interactable_inventory(inventory, heading, hint, True)
        elif item_used == officers_hat:
            if officers_hat not in accessories:
                show_interactable_inventory(inventory, heading, hint, True)
            else:
                show_interactable_inventory(inventory, heading, hint, True)
        else:
            show_interactable_inventory(inventory, "That item cannot be used right now.", hint, True)

    while escaping == True:

        if section == 1:
            if transition == True:
                text1 = font1.render("You crawled through the vents, eventually reaching another room!", True, (255, 255, 255))
                text3 = font1.render("", True, (255, 255, 255))
            else:
                if used_torch == False:
                    text1 = font1.render("It's very dark in the vents. Going without a light source is unwise...", True, (255, 255, 255))
                    text3 = font1.render("", True, (255, 255, 255))
                else:
                    text1 = font1.render("It is much easier to see where you are going now.", True, (255, 255, 255))
                    text3 = font1.render("Press Q to crawl forward:", True, (255, 255, 255))
        elif section == 2:
            if transition == True:
                text1 = font1.render("You crossed the gap with caution and headed up the stairs to the roof!", True, (255, 255, 255))
                text3 = font1.render("", True, (255, 255, 255))
            else:
                if used_beam == False:
                    text1 = font1.render("There seems to be an unexpected large gap in the way!", True, (255, 255, 255))
                    text3 = font1.render("", True, (255, 255, 255))
                else:
                    text1 = font1.render("It looks safe to cross now.", True, (255, 255, 255))
                    text3 = font1.render("Press Q to walk across:", True, (255, 255, 255))
        elif section == 3:
            if transition == True:
                text1 = font1.render("You took a deep breath and jumped off the building.", True, (255, 255, 255))
                text3 = font1.render("", True, (255, 255, 255))
            else:
                if used_parachute == False:
                    text1 = font1.render("You're on the roof! How should you get safely down?", True, (255, 255, 255))
                    text3 = font1.render("", True, (255, 255, 255))
                else:
                    text1 = font1.render("Time to get out of this terrible joint once and for all!", True, (255, 255, 255))
                    text3 = font1.render("Press Q to jump:", True, (255, 255, 255))

        text2 = use_item

        screen.fill('black')
        line_separating_text_and_images()        

        if main_options == True:

            if section == 1 and used_torch == False:
                screen.blit(vent1, (0, 0))
            elif section == 1 and used_torch == True:
                screen.blit(vent2, (0, 0))
            elif section == 2 and used_beam == False:
                screen.blit(beam1, (0, 0))
            elif section == 2 and used_beam == True:
                screen.blit(beam2, (0, 0))
            elif section == 3 and transition == False:
                screen.blit(rooftop, (0, 0))
            
            for i in range(text_emphasis):
                screen.blit(text1, (5, 485))
                if transition == True:
                    screen.blit(shift_text, shift_rect)
                else:
                    screen.blit(go_back, go_back_rect)
                    screen.blit(text2, (5, 537))
                if (section == 1 and used_torch == True) or (section == 2 and used_beam == True) or (section == 3 and used_parachute == True):
                    screen.blit(text3, (5, 563))
                    
        if use_item_options == True:
            if section == 1 and used_torch == False:
                use_items(inventory, "What could light the way forward?", vent1)
            elif section == 1 and used_torch == True:
                use_items(inventory, "", vent2)
            elif section == 2 and used_beam == False:
                use_items(inventory, "Something long and hard should do the trick.", beam1)
            elif section == 2 and used_beam == True:
                use_items(inventory, "", beam2)
            elif section == 3 and used_parachute == False:
                use_items(inventory, "If only there were a way to slow your fall...", rooftop)
            elif section == 3 and used_parachute == True:
                use_items(inventory, "", rooftop)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            else:
                if event.type == KEYDOWN:
                    if event.key == K_LSHIFT or event.key == K_RSHIFT and transition == True:
                        transition = False
                        if section == 1:
                            mixer.Channel(0).play(mixer.Sound(resource_path("SFX Exit Vent.wav")))
                        section += 1
                        time.sleep(0.1)
                        if section >= 4:
                            return True
                    if event.key == K_z:
                        use_item_options = True
                        main_options = False
                    if event.key == K_q and main_options == True:
                        transition = True
                        if section == 1:
                            mixer.Channel(0).play(mixer.Sound(resource_path("SFX Inside Vent.wav")))
                        if section == 3:
                            mixer.music.stop()
                    if event.key == K_0 and transition == False:
                        if main_options == False:
                            use_item_options = False
                            main_options = True
                            item_used = None
                        elif main_options == True:
                            mixer.music.stop()
                            time.sleep(0.2)
                            escaping = False

                    if event.key == K_1 and use_item_options == True:
                        item_used = inventory[0]
                        if inventory[0] == officers_coat:
                            if officers_coat not in accessories:
                                accessories.append(officers_coat)
                                heading = "You put on the officer's coat."
                                inventory[0] = empty_space
                            else:
                                heading = "You are already wearing an officer's coat."
                        elif inventory[0] == officers_hat:
                            if officers_hat not in accessories:
                                accessories.append(officers_hat)
                                heading = "You put on the officer's hat."
                                inventory[0] = empty_space
                            else:
                                heading = "You are already wearing an officer's hat."
                        if section == 1:
                            if len(sec1_usable_items) == 0:
                                already_used_torch = True
                            if item_used in sec1_usable_items:
                                sec1_usable_items.remove(item_used)
                                mixer.Channel(0).play(mixer.Sound(resource_path("SFX Torch.wav")))
                        elif section == 2:
                            if len(sec2_usable_items) == 0:
                                already_used_beam = True
                            if item_used in sec2_usable_items:
                                inventory[0] = empty_space
                                sec2_usable_items.remove(item_used)
                                mixer.Channel(0).play(mixer.Sound(resource_path("SFX Warehouse Lumber 2.wav")))
                        elif section == 3:
                            if len(sec3_usable_items) == 1:
                                already_used_parachute = True
                            if item_used in sec3_usable_items:
                                inventory[0] = empty_space
                                sec3_usable_items.remove(item_used)
                                mixer.Channel(0).play(mixer.Sound(resource_path("SFX Laundry 2.wav")))

                    if event.key == K_2 and use_item_options == True:
                        item_used = inventory[1]
                        if inventory[1] == officers_coat:
                            if officers_coat not in accessories:
                                accessories.append(officers_coat)
                                heading = "You put on the officer's coat."
                                inventory[1] = empty_space
                            else:
                                heading = "You are already wearing an officer's coat."
                        elif inventory[1] == officers_hat:
                            if officers_hat not in accessories:
                                accessories.append(officers_hat)
                                heading = "You put on the officer's hat."
                                inventory[1] = empty_space
                            else:
                                heading = "You are already wearing an officer's hat."
                        if section == 1:
                            if len(sec1_usable_items) == 0:
                                already_used_torch = True
                            if item_used in sec1_usable_items:
                                sec1_usable_items.remove(item_used)
                                mixer.Channel(0).play(mixer.Sound(resource_path("SFX Torch.wav")))
                        elif section == 2:
                            if len(sec2_usable_items) == 0:
                                already_used_beam = True
                            if item_used in sec2_usable_items:
                                inventory[1] = empty_space
                                sec2_usable_items.remove(item_used)
                                mixer.Channel(0).play(mixer.Sound(resource_path("SFX Warehouse Lumber 2.wav")))
                        elif section == 3:
                            if len(sec3_usable_items) == 1:
                                already_used_paracuhte = True
                            if item_used in sec3_usable_items:
                                inventory[1] = empty_space
                                sec3_usable_items.remove(item_used)
                                mixer.Channel(0).play(mixer.Sound(resource_path("SFX Laundry 2.wav")))

                    if event.key == K_3 and use_item_options == True:
                        item_used = inventory[2]
                        if inventory[2] == officers_coat:
                            if officers_coat not in accessories:
                                accessories.append(officers_coat)
                                heading = "You put on the officer's coat."
                                inventory[2] = empty_space
                            else:
                                heading = "You are already wearing an officer's coat."
                        elif inventory[2] == officers_hat:
                            if officers_hat not in accessories:
                                accessories.append(officers_hat)
                                heading = "You put on the officer's hat."
                                inventory[2] = empty_space
                            else:
                                heading = "You are already wearing an officer's hat."
                        if section == 1:
                            if len(sec1_usable_items) == 0:
                                already_used_torch = True
                            if item_used in sec1_usable_items:
                                sec1_usable_items.remove(item_used)
                                mixer.Channel(0).play(mixer.Sound(resource_path("SFX Torch.wav")))
                        elif section == 2:
                            if len(sec2_usable_items) == 0:
                                already_used_beam = True
                            if item_used in sec2_usable_items:
                                inventory[2] = empty_space
                                sec2_usable_items.remove(item_used)
                                mixer.Channel(0).play(mixer.Sound(resource_path("SFX Warehouse Lumber 2.wav")))
                        elif section == 3:
                            if len(sec3_usable_items) == 1:
                                already_used_parachute = True
                            if item_used in sec3_usable_items:
                                inventory[2] = empty_space
                                sec3_usable_items.remove(item_used)
                                mixer.Channel(0).play(mixer.Sound(resource_path("SFX Laundry 2.wav")))

                    if event.key == K_4 and use_item_options == True:
                        item_used = inventory[3]
                        if inventory[3] == officers_coat:
                            if officers_coat not in accessories:
                                accessories.append(officers_coat)
                                heading = "You put on the officer's coat."
                                inventory[3] = empty_space
                            else:
                                heading = "You are already wearing an officer's coat."
                        elif inventory[3] == officers_hat:
                            if officers_hat not in accessories:
                                accessories.append(officers_hat)
                                heading = "You put on the officer's hat."
                                inventory[3] = empty_space
                            else:
                                heading = "You are already wearing an officer's hat."
                        if section == 1:
                            if len(sec1_usable_items) == 0:
                                already_used_torch = True
                            if item_used in sec1_usable_items:
                                sec1_usable_items.remove(item_used)
                                mixer.Channel(0).play(mixer.Sound(resource_path("SFX Torch.wav")))
                        elif section == 2:
                            if len(sec2_usable_items) == 0:
                                already_used_beam = True
                            if item_used in sec2_usable_items:
                                inventory[3] = empty_space
                                sec2_usable_items.remove(item_used)
                                mixer.Channel(0).play(mixer.Sound(resource_path("SFX Warehouse Lumber 2.wav")))
                        elif section == 3:
                            if len(sec3_usable_items) == 1:
                                already_used_parachute = True
                            if item_used in sec3_usable_items:
                                inventory[3] = empty_space
                                sec3_usable_items.remove(item_used)
                                mixer.Channel(0).play(mixer.Sound(resource_path("SFX Laundry 2.wav")))

                    if event.key == K_5 and use_item_options == True:
                        item_used = inventory[4]
                        if inventory[4] == officers_coat:
                            if officers_coat not in accessories:
                                accessories.append(officers_coat)
                                heading = "You put on the officer's coat."
                                inventory[4] = empty_space
                            else:
                                heading = "You are already wearing an officer's coat."
                        elif inventory[4] == officers_hat:
                            if officers_hat not in accessories:
                                accessories.append(officers_hat)
                                heading = "You put on the officer's hat."
                                inventory[4] = empty_space
                            else:
                                heading = "You are already wearing an officer's hat."
                        if section == 1:
                            if len(sec1_usable_items) == 0:
                                already_used_torch = True
                            if item_used in sec1_usable_items:
                                sec1_usable_items.remove(item_used)
                                mixer.Channel(0).play(mixer.Sound(resource_path("SFX Torch.wav")))
                        elif section == 2:
                            if len(sec2_usable_items) == 0:
                                already_used_beam = True
                            if item_used in sec2_usable_items:
                                inventory[4] = empty_space
                                sec2_usable_items.remove(item_used)
                                mixer.Channel(0).play(mixer.Sound(resource_path("SFX Warehouse Lumber 2.wav")))
                        elif section == 3:
                            if len(sec3_usable_items) == 1:
                                already_used_parachute = True
                            if item_used in sec3_usable_items:
                                inventory[4] = empty_space
                                sec3_usable_items.remove(item_used)
                                mixer.Channel(0).play(mixer.Sound(resource_path("SFX Laundry 2.wav")))

                    
        pygame.display.update()

    # If the player gave up #
    while escaping == False and escaped == False:

        screen.fill('black')
        line_separating_text_and_images()

        if used_beam == True:
            for i in range(len(inventory)):
                if inventory[i] == empty_space:
                    inventory[i] = lumber_beam
                    break
        if used_parachute == True:
            for i in range(len(inventory)):
                if inventory[i] == empty_space and pillowcase_parachute not in sec3_usable_items:
                    inventory[i] = pillowcase_parachute
                    break
                if inventory[i] == empty_space and bedsheet_parachute not in sec3_usable_items:
                    inventory[i] = bedsheet_parachute
                    break

        if section == 3 and used_parachute == True:
            text1 = font1.render("You picked up the parachute and lumber beam before heading back to your cell.", True, (255, 255, 255))
        elif section >= 2 and used_beam == True:
            text1 = font1.render("You picked up the lumber beam before heading back to your cell.", True, (255, 255, 255))
        else:
            text1 = font1.render("You headed back to your cell.", True, (255, 255, 255))
        
        for i in range(text_emphasis):
            screen.blit(text1, (5, 485))
            screen.blit(shift_text, shift_rect)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            else:
                if event.type == KEYDOWN:
                    if event.key == K_LSHIFT or event.key == K_RSHIFT:
                        return False
        pygame.display.update()





def ending():

    global shift_text

    count = 1

    if specific_parachute == bedsheet_parachute:
        image = pygame.image.load(resource_path('end image bedpar.png')) # bedpar = bedsheet parachute
    else:
        image = pygame.image.load(resource_path('end image pilpar.png')) # pilpar = pillowcase parachute
    image = pygame.transform.scale(image, (1280, 480))
    
    mixer.music.load(resource_path("Escaped.wav"))
    mixer.music.set_volume(0.5)
    mixer.music.play(-1)

    while True:

        screen.fill('black')

        if count == 1:
            text1 = font1.render("As you soar over the canopy, you look back towards the prison and breathe a sigh of ", True, (255, 255, 255))
            text2 = font1.render("relief, knowing your days being locked up have, for now, come to an end.", True, (255, 255, 255))
        elif count == 2:
            text1 = font1.render("Your next best option is to head to the village a few miles north from here in hopes", True, (255, 255, 255))
            text2 = font1.render("of finding refuge and to clear your name, but the police won't be too far behind.", True, (255, 255, 255))
        elif count == 3:
            text1 = font1.render("Will you manage to outrun your past life of crime, or will it catch up to you again?", True, (255, 255, 255))
            text2 = font1.render("Until then, well done for escaping the Black Bayou Box!", True, (255, 255, 255))
        else:
            text1 = font1.render(f"Days spent in prison: {days_in_prison - 1}", True, (255, 255, 255))
            text2 = font1.render(f"Escape attempts: {escape_attempts}", True, (255, 255, 255))
        if count >= 4:
            shift_text = font1.render("Thank you for playing!", True, (255, 255, 255))

        line_separating_text_and_images()
        screen.blit(image, (0, 0))

        for i in range(text_emphasis):
            screen.blit(text1, (5, 485))
            screen.blit(text2, (5, 515))
            screen.blit(shift_text, shift_rect)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            else:
                if event.type == KEYDOWN:
                    if event.key == K_LSHIFT or event.key == K_RSHIFT:
                        count += 1
        pygame.display.update()
        


        
                        
                        

def title_screen():
    
    on_the_title_screen = True
    info = False
    Credits = False
    quit_game = False

    pygame.display.set_caption(f"BLACK BAYOU BOX")
    
    mixer.music.load(resource_path("Title Theme.wav"))
    mixer.music.set_volume(0.5)
    mixer.music.play(-1)

    while on_the_title_screen:

        screen.fill('black')
        line_separating_text_and_images()
        title = pygame.image.load(resource_path('title_screen.png'))
        title = pygame.transform.scale(title, (1280, 480))
        title_rect = title.get_rect()
        title_rect.topleft = (0, 0)
        
        heading = font3.render("[[[BLACK-BAYOU-BOX]]]", True, (255, 255, 255))
        heading_rect = heading.get_rect()
        heading_rect.center = ((screen_width // 2), 520)

        if info == False and Credits == False:
            text1 = font1.render("[Press Q to begin]", True, (255, 255, 255))
            text1_rect = text1.get_rect()
            text1_rect.center = ((screen_width // 2), 580)
            text2 = font1.render("[Press W for context]", True, (255, 255, 255))
            text2_rect = text2.get_rect()
            text2_rect.center = ((screen_width // 2), 610)
            text3 = font1.render("[Press E for credits]", True, (255, 255, 255))
            text3_rect = text3.get_rect()
            text3_rect.center = ((screen_width // 2), 640)
            text4 = font1.render("[Press R to quit]", True, (255, 255, 255))
            text4_rect = text4.get_rect()
            text4_rect.center = ((screen_width // 2), 670)
        elif info == True and Credits == False:
            text1 = font1.render("This is my first video game, and was made for the 2026 bad ideas game jam.", True, (255, 255, 255))
            text1_rect = text1.get_rect()
            text1_rect.topleft = (5, 485)
            text2 = font1.render("Your goal is to escape a prison by smuggling items around the building.", True, (255, 255, 255))
            text2_rect = text2.get_rect()
            text2_rect.topleft = (5, 515)
            text3 = font1.render("Expect some of this game not to make much sense. Just saying.", True, (255, 255, 255))
            text3_rect = text3.get_rect()
            text3_rect.topleft = (5, 545)
        elif info == False and Credits == True:
            text1 = font1.render("Concept, art, animation, SFX and most of the programming by me.", True, (255, 255, 255))
            text1_rect = text1.get_rect()
            text1_rect.topleft = (5, 485)
            text2 = font1.render("Learnt how to use pygame with the help of geeksforgeeks.", True, (255, 255, 255))
            text2_rect = text2.get_rect()
            text2_rect.topleft = (5, 515)
            text3 = font1.render("Code for displaying animations from a YouTube Tutorial by 'Clear Code'.", True, (255, 255, 255))
            text3_rect = text3.get_rect()
            text3_rect.topleft = (5, 545)
            text5 = font1.render("My sibling helped me design Theo's character (I was out of ideas).", True, (255, 255, 255))
            text5_rect = text5.get_rect()
            text5_rect.topleft = (5, 575)

        go_back_rect.center = ((screen_width // 2), 680)

        screen.blit(title, title_rect)
        for i in range(text_emphasis):
            if info == False and Credits == False:
                screen.blit(heading, heading_rect)
                screen.blit(text4, text4_rect)
            else:
                screen.blit(go_back, go_back_rect)
            if Credits == True:
                screen.blit(text5, text5_rect)
            screen.blit(text1, text1_rect)
            screen.blit(text2, text2_rect)
            screen.blit(text3, text3_rect)

        for event in pygame.event.get():
            if event.type == pygame.QUIT or quit_game == True:
                pygame.quit()
                sys.exit()
            else:
                if event.type == KEYDOWN:
                    if event.key == K_q and info == False and Credits == False:
                        on_the_title_screen = False
                    elif event.key == K_w and info == False and Credits == False:
                        info = True
                    elif event.key == K_e and info == False and Credits == False:
                        Credits = True
                    elif event.key == K_r and info == False and Credits == False:
                        time.sleep(0.3)
                        quit_game = True
                    elif event.key == K_0:
                        info = False
                        Credits = False
        pygame.display.update()

    go_back_rect.bottomleft = (5, screen_height) # resets the positon of the 'go back' text for future uses.
    mixer.music.stop()
    time.sleep(0.4)










completed = False

while True:
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        
        title_screen()
        inside_cell()

        while True:

            if escaping == True:
                day_blank('Escaping')
                escaped = escape_segment()
                if escaped == True:
                    ending()
                    break


            day_blank('Chopping')
            num_of_lumber = day1_Chopping()
            inspect_inventory(inventory)
            inside_cell()

            if escaping == True:
                day_blank('Escaping')
                escaped = escape_segment()
                if escaped == True:
                    ending()
                    break


            day_blank('Mining')
            num_of_boxes = day2_Mining()
            inspect_inventory(inventory)
            inside_cell()

            if escaping == True:
                day_blank('Escaping')
                escaped = escape_segment()
                if escaped == True:
                    ending()
                    break


            day_blank('Warehouse')
            day3_Warehouse(num_of_lumber, num_of_boxes)
            inspect_inventory(inventory)
            inside_cell()

            if escaping == True:
                day_blank('Escaping')
                escaped = escape_segment()
                if escaped == True:
                    ending()
                    break


            day_blank('Fishing')
            num_of_dishes = day4_Fishing()
            inspect_inventory(inventory)
            inside_cell()

            if escaping == True:
                day_blank('Escaping')
                escaped = escape_segment()
                if escaped == True:
                    ending()
                    break


            day_blank('Kitchen')
            day5_Kitchen(num_of_dishes)
            inspect_inventory(inventory)
            inside_cell()

            if escaping == True:
                day_blank('Escaping')
                escaped = escape_segment()
                if escaped == True:
                    ending()
                    break


            day_blank('Laundry')
            amount_of_laundry = day6_Laundry()
            inspect_inventory(inventory)
            inside_cell()

            if escaping == True:
                day_blank('Escaping')
                escaped = escape_segment()
                if escaped == True:
                    ending()
                    break


            day_blank('Free Time')
            bruce()
            day7_Courtyard()
            inspect_cell(mattress, pillow, hole)
            inside_cell()

            if escaping == True:
                day_blank('Escaping')
                escaped = escape_segment()
                if escaped == True:
                    ending()
                    break
            
    pygame.display.update()
# Can you tell I was lazy with my code optimisation?
