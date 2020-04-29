import pandas as pd
from opentrons import protocol_api

# Metadata
metadata = {
    'protocolName': 'IF-IC lot test',
    'author': 'John Burford',
    'description': 'Protocol to take lot testing material from tubes, titrate and stamp on cell plates',
    'apiLevel': '2.0'

def run(protocol: protocol_api.ProtocolContext):

# Labware

# 10uL tips in slot 11, 300uL tips in slot 10 and 7
tiprack10 = protocol.load_labware('opentrons_96_tiprack_10ul', 11)
tiprack300 = protocol.load_labware('opentrons_96_tiprack_300ul', 10)
tiprack301 = protocol.load_labware('opentrons_96_tiprack_300ul', 7)

# Use this section to specify where the starting tip is in a tip rack, if not A1 (un-hash if you need it)
# specify which pipette (p10 or p300) and which tiprack (tiprack10 or tiprack300)
# p10.starting_tip = tiprack10.well('C3')

# ADB trough in slot 8 - this needs to be filled with ADB prior to running this protocol
ADBTrough = protocol.load_labware('agilent_1_reservoir_290ml', 8, label='ADB Trough')

# Deep-well plate in slot 9 - this is the plate you will be doing the dilutions in
DilutionPlate = protocol.load_labware('nest_96_wellplate_200ul_flat', 9, label='Dilution Plate')

# cell plate1 in slot 4 - this is cell plate 1 to be loaded with 100ul PBS added
CellPlate1 = protocol.load_labware('corning_96_wellplate_360ul_flat', 4, label='Cell Plate1')

# cell plate2 in slot 5 - this is cell plate 2 to be loaded with 100ul PBS added
CellPlate2 = protocol.load_labware('corning_96_wellplate_360ul_flat', 5, label='Cell Plate2')

# Deep-well plate for liquid waste in slot 6 - this is where liquid waste will go
LiquidWaste = protocol.load_labware('nest_96_wellplate_200ul_flat', 6, label='Liquid Waste')

# Lot Material in slot 6 - this is where the old and new lot material will go
tube_rack = labware.load('tube-rack-2ml', 6, label='tube_rack')

# Pipettes
# double check pipette location - p10 on the left and p300 on the right
p10 = protocol.load_instrument('p10_single', 'left', tip_racks=[tiprack10])
p300 = protocol.load_instrument('p300_single_gen2', 'right', tip_racks=[tiprack300])
p301 = protocol.load_instrument('p300_single_gen2', 'right', tip_racks=[tiprack301])

#putting tips on 300 ul pipette and transferring ABD to the dilution plate
p300.pick_up_tip(
        tiprack_300.('A1,A2,A3,A4,A5,A6'))
p300.aspirate(
        288,
        ADBTrough.cols('6'),
        [cols[0].bottom(3.5) for cols in cell_plate.cols()],
        new_tip='never',
        air_gap=10,
        disposal_vol = 0)
p300.dispense(288, DilutionPlate('A1,A2,A3,A4,A5,A6'),new_tip='never')
p300.aspirate(
        300,
        ADBTrough.cols('6'),
        [cols[0].bottom(3.5) for cols in cell_plate.cols()],
        new_tip='never',
        air_gap=0,
        disposal_vol = 0)
p300.dispense(150, DilutionPlate('B1,B2,B3,B4,B5,B6'),new_tip='never')
p300.dispense(150, DilutionPlate('C1,C2,C3,C4,C5,C6'),new_tip='never')
p300.aspirate(
        300,
        ADBTrough.cols('6'),
        [cols[0].bottom(3.5) for cols in cell_plate.cols()],
        new_tip='never',
        air_gap=0,
        disposal_vol = 0)
p300.dispense(150, DilutionPlate('D1,D2,D3,D4,D5,D6'),new_tip='never')
p300.dispense(150, DilutionPlate('E1,E2,E3,E4,E5,E6'),new_tip='never')
p300.aspirate(
        300,
        ADBTrough.cols('6'),
        [cols[0].bottom(3.5) for cols in cell_plate.cols()],
        new_tip='never',
        air_gap=0,
        disposal_vol = 0)
p300.dispense(150, DilutionPlate('F1,F2,F3,F4,F5,F6'),new_tip='never')
p300.dispense(150, DilutionPlate('G1,G2,G3,G4,G5,G6'),new_tip='never')
p300.droptip()

#Transfer old and new lot to titration plate
p10.pick_up_tip(tiprack10.(A1))
p10.aspirate(12, tube_rack(A1))
p10.dispense(DilutionPlate(A1))
p10.droptip()

p10.pick_up_tip(tiprack10.(A2))
p10.aspirate(12, tube_rack(A1))
p10.dispense(DilutionPlate(A2))
p10.droptip()

p10.pick_up_tip(tiprack10.(A3))
p10.aspirate(12, tube_rack(A1))
p10.dispense(DilutionPlate(A3))
p10.droptip()

p10.pick_up_tip(tiprack10.(A4))
p10.aspirate(12, tube_rack(A2))
p10.dispense(DilutionPlate(A4))
p10.droptip()

p10.pick_up_tip(tiprack10.(A5))
p10.aspirate(12, tube_rack(A2))
p10.dispense(DilutionPlate(A5))
p10.droptip()

p10.pick_up_tip(tiprack10.(A6))
p10.aspirate(12, tube_rack(A2))
p10.dispense(DilutionPlate(A6))
p10.droptip()

#Titrate material in dilution plate
p300.pick_up_tip(tiprack_300.('B1,B2,B3,B4,B5,B6'))
