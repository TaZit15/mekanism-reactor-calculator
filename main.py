import PySimpleGUI as sg
import time

sg.theme('TanBlue')  # i dunno, i liked it
# there should be a better solution, but i use a 1px b64 image (black) to resize the buttons to a certain size
black64 = "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mNk+A8AAQUBAScY42YAAAAASUVORK5CYII="

# behold the behemoth of creating 18 different layouts (button grids) because there is no dynamic layout change in pysimplegui
# this just hits different
gridlist = [*[[sg.Frame(layout=[*[[sg.Button('', border_width=1, image_data=black64, image_size=(30, 30),
                                             button_color=("black", "black"), key=f'Button{i}-{y}-{x}') for y in range(i)]
                                  for x in range(i)]],
                        title='Reactor grid layout:', key=f"reactorGrid{i}")] for i in range(19)]]

# Button ID's work like this: 4x4 Grid -> Button 4-x-x (first number shows which gridsize)
#                             From top left to bottom right counting up
#                             f. ex. leftmost column top to bottom are 0-3: 400, 401, 402, 403
#                             next column would be (top to bottom): 410, 411, 412, 413
#                             ...


# rest of the gui layout
col1 = sg.Column([
    [sg.Frame(
        layout=[
            [
                sg.Radio('Water', 'radio1', default=True, size=(10, 1)),
                sg.Radio('Sodium', 'radio1', size=(10, 1))
            ]
        ],
        title='Reactor specs:')
    ],
    
    [sg.Frame(
        layout=[[sg.Text('Size (X, Y, Z):')],
                [
                    sg.Input(size=(3, 1), enable_events=True, tooltip='x: width', key='-X-'),
                    sg.Input(size=(3, 1), enable_events=True, tooltip='y: height', key='-Y-'),
                    sg.Input(size=(3, 1), enable_events=True, tooltip='z: depth', key='-Z-'),
                    sg.Text(text='Reactor hulls: 0   0x64 + 0', size=(35, 1), key='-textBlockCount-')
                ],
                [sg.Button(button_text='Show')],
                [sg.Text(size=(25, 2), text_color='red', key='-textInvalid-')],
                [sg.Text('Reactor stats:')],
                [sg.Slider(size=(10, 5))],
                ],
        title='Information:')], ])

# building the final layout for the gui
# making the first grid (0x0) visible, the other 17 (until 18x18) invisible
layout = [
    [col1, sg.Column([gridlist[0]], key=f'-GRID0-')] + [sg.Column([gridlist[x]], visible=False, key=f'-GRID{x}-') for x
                                                        in range(1, 19)],
    [sg.Frame(layout=[[sg.Button(button_text='Reset'), sg.Button(button_text='Max rod density'),
                       sg.Sizer(280, 10)]], title='')]]

# do the windooow
window = sg.Window('Mekanism (1.16.4) Fission reactor calculator v0.1', layout)


# some functions finally
def reactor_size_check(x, y, z):
    try:
        x = int(x)
        y = int(y)
        z = int(z)
    # dO nOt UsE bArE eXcEpT
    # go ahead and cry
    except:
        x, y, z = 0, 0, 0
    # returning 0 if size invalid, 1 if sides not same length
    if x < 3 or y < 4 or z < 3:
        return 0
    elif x > 18 or y > 18 or z > 18:
        return 0
    elif x != z:
        return 1
    # return hull block count - 4 port blocks
    count = ((2 * x * z) + (2 * (y - 2) * x) + (2 * (y - 2) * (z - 2))) - 4
    stacks = count // 64
    items = count % 64
    return (count, stacks, items)


# loooooooooooooooooooooop
while True:
    event, values = window.read()
    if event == sg.WIN_CLOSED:
        break
    # click the show button. do it.
    if event == 'Show':
        # bad reactor size handling
        if reactor_size_check(values['-X-'], values['-Y-'], values['-Z-']) == 0:
            window['-textInvalid-'].update('Invalid reactor size!\nMust be 3x4x3 - 18x18x18')
        elif reactor_size_check(values['-X-'], values['-Y-'], values['-Z-']) == 1:
            window['-textInvalid-'].update('Both sides must be equal (X & Z)!')
        else:
            # grid action and text action
            blocks = reactor_size_check(values['-X-'], values['-Y-'], values['-Z-'])
            window['-textBlockCount-'].update(f"Reactor hulls: {blocks[0]}   {blocks[1]}x64 + {blocks[2]}")
            window['-textInvalid-'].update('')
            
            # make all grids invisible, turn right grid visible
            for i in range(19):
                window[f'-GRID{i}-'].update(visible=False)
            window[f"-GRID{int(values['-X-'])}-"].update(visible=True)
            # color fuel rod area grey
            for i in range(1, int(values['-X-'])-1):
                for j in range(1, int(values['-X-'])-1):
                    window.FindElement(f"Button{int(values['-X-'])}-{j}-{i}").Update(button_color=('grey', 'grey'))
            
            # for now, there wont be custom fuel rod placement. maybe sometime in the future
            # color max fuel rod density (checkerboard pattern)
            for i in range(1, int(values['-X-']) - 1):
                for j in range(1, int(values['-X-']) - 1):
                    if i % 2 == 1:
                        if j % 2 == 1:
                            window.FindElement(f"Button{int(values['-X-'])}-{j}-{i}").Update(
                                button_color=('yellow', 'yellow'))
                    else:
                        if j % 2 == 0:
                            window.FindElement(f"Button{int(values['-X-'])}-{j}-{i}").Update(
                                button_color=('yellow', 'yellow'))
    
    # for debug purposes
    print(event)

window.close()

# Todo: control rod custom grid
# Todo: calc reactor data
