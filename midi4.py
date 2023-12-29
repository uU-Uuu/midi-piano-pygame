import mido
from mido import MidiFile

from threading import Event


def openOutport():
    """open the first output port found on the device"""
    try:
        outport_name = mido.get_output_names()[0]
        print(f'Opened an output port: {outport_name}')
        outport = mido.open_output(outport_name)
        outport.send(mido.Message('note_on',  note=43, velocity=0))
    except OSError as e:
        print(f'{e}\nFailed to find or open the output port')
    except:
        print('Failed to find or open the output port')
    else: 
        return outport



def openInport():
    """open the first input port found on the device"""
    try:
        inport_name = mido.get_input_names()[0]
        print(f'Opened an input port: {inport_name}')
        inport = mido.open_input(inport_name)
    except IndexError:
        print(f'Failed to find or open the input port')
    else:
        return inport



def createMIDIList(midfile=str):
    """convert a .mid file into a list of dict"""
    try:
        mid = MidiFile(midfile)
    except FileNotFoundError as e:
        print(f'{e}')
        return None
    else:
        li_midi = []
        for msg in mid:
            if not msg.is_meta:
                li_midi.append(msg.dict())
        return li_midi, mid



def playSong(event: Event, midfile=str, outport=str):
    """play midifile to the assigned output port"""
    for msg in midfile.play():
        outport.send(msg)
        if event.is_set():
            outport.reset()
            break


def playNote(note_x):
    msg = mido.Message('note_on', note=note_x, velocity=80, time=3)
    return msg