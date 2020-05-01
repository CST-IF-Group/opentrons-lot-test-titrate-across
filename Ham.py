from opentrons import protocol_api

# Metadata
metadata = {
    'protocolName': 'IF-IC lot test',
    'author': 'John Burford',
    'description': 'Protocol to take lot testing material from tubes, titrate and stamp on cell plates',
    'apiLevel': '2.0'
}


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
    adb_trough = protocol.load_labware('agilent_1_reservoir_290ml', 8, label='ADB Trough')

    # Deep-well plate in slot 9 - this is the plate you will be doing the dilutions in
    DilutionPlate = protocol.load_labware('nest_96_wellplate_200ul_flat', 9, label='Dilution Plate')

    # cell plate1 in slot 4 - this is cell plate 1 to be loaded with 100ul PBS added
    CellPlate1 = protocol.load_labware('corning_96_wellplate_360ul_flat', 4, label='Cell Plate1')

    # cell plate2 in slot 5 - this is cell plate 2 to be loaded with 100ul PBS added
    CellPlate2 = protocol.load_labware('corning_96_wellplate_360ul_flat', 5, label='Cell Plate2')

    # Deep-well plate for liquid waste in slot 6 - this is where liquid waste will go
    LiquidWaste = protocol.load_labware('nest_96_wellplate_200ul_flat', 1, label='Liquid Waste')
    # Lot Material in slot 6 - this is where the old and new lot material will go
    tube_rack = protocol.load_labware('opentrons_24_tuberack_nest_1.5ml_screwcap', 6, label='tube_rack')

    # Pipettes
    # double check pipette location - p10 on the left and p300 on the right
    p10 = protocol.load_instrument('p10_single', 'left', tip_racks=[tiprack10])
    p300 = protocol.load_instrument('p300_multi', 'right', tip_racks=[tiprack300])

    # putting tips on 300 ul pipette and transferring ABD to the dilution plate

    p300.pick_up_tip()

    p300.transfer(
        200,
        adb_trough.columns_by_name()['1'],
        DilutionPlate.columns_by_name()['1'],
        new_tip='never')

    column_set = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12']

    for i in column_set:
        p300.transfer(
            200,
            adb_trough.columns_by_name()['1'],
            DilutionPlate.columns(i),
            new_tip='never')

    p300.drop_tip()

    # Move sample material from tubes to dilution plate

    old_lot = ('A1', 'B1', 'C1', 'D1')
    new_lot = ('E1', 'F1', 'G1', 'H1')

    p10.flow_rate.aspirate = 50

    for i in old_lot:
        p10.transfer(
            6,
            tube_rack.wells_by_name()['A1'],
            DilutionPlate.wells_by_name()[i],
            new_tip='always',
            touch_tip=True,
            blow_out=True,
            aspirate=5,
            mix_after=(5, 10)
        )

    for i in new_lot:
        p10.transfer(
            6,
            tube_rack.wells_by_name()['B1'],
            DilutionPlate.wells_by_name()[i],
            new_tip='always',
            touch_tip=True,
            blow_out=True,
            aspirate=5,
            mix_after=(5, 10)
        )
    # Titrate material in dilution plate across plate (leaving column 12 open)

    p300.pick_up_tip()

    column_set2 = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11']

    for i in column_set2:
        p300.transfer(
            200,
            DilutionPlate.columns_by_name()['1'],
            DilutionPlate.columns(i),
            new_tip='never',
            mix_after=(5, 200))

    p300.drop_tip()

    # aspirate PBS off of cell plates

    p300.pick_up_tip()

    for i in column_set:

        p300.transfer(
            200,
            CellPlate1.columns_by_name()[i],
            LiquidWaste.columns_by_name()['6'],
            new_tip='never',
                     )
        p300.transfer(
            200,
            CellPlate2.columns_by_name()[i],
            LiquidWaste.columns_by_name()['6'],
            new_tip='never',
                     )
    p300.drop_tip()

    """"
    # transfer material from dilution plate to CellPlate2 and CellPlate2
    
    p300.pick_up_tip()

    for i in column_set:

         p300.transfer
    """
