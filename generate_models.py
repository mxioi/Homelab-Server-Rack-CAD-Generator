from pathlib import Path

import cadquery as cq


# Units: millimeters
GPU = {
    "name": "gpu_frontier_air",
    "length": 267.0,
    "height": 111.0,
    "thickness": 40.0,
}

PSU = {
    "name": "psu_rm750x",
    "length": 160.0,
    "width": 150.0,
    "height": 86.0,
}

# Provisional placeholder from listing dimensions.
# Replace once exact board + bracket measurements are confirmed.
OCULINK = {
    "name": "oculink_adapter",
    "length": 174.0,
    "width": 47.3,
    "height": 14.0,
    "board_thickness": 1.6,
}

# Rack holder assumptions based on 19-inch rack hardware and VEVOR open frame class.
# Tune these before printing on your exact rack.
HOLDER = {
    "name": "rack_gpu_holder",
    "rack_panel_width": 482.6,
    "rail_hole_spacing": 465.0,
    "usable_depth": 320.0,
    "base_width": 170.0,
    "base_thickness": 6.0,
    "side_wall_thickness": 5.0,
    "side_wall_height": 62.0,
    "gpu_channel_width": 48.0,
    "gpu_channel_height": 46.0,
    "adapter_pad_length": 190.0,
}

RACK = {
    "name": "vevor_20u_rack",
    "outer_width": 510.0,
    "outer_depth": 585.0,
    "outer_height": 982.0,
    "post_size": 30.0,
    "beam_size": 30.0,
    "rack_usable_width": 440.0,
    "rack_hole_pitch": 44.45,  # 1U
    "rack_hole_diameter": 6.8,
    "units": 20,
    "caster_height": 70.0,
    "caster_wheel_diameter": 32.0,
    "top_panel_thickness": 2.0,
}

OUTPUT_DIR = Path("exports")


def make_gpu_envelope() -> cq.Workplane:
    body = cq.Workplane("XY").box(
        GPU["length"],
        GPU["thickness"],
        GPU["height"],
        centered=(True, True, False),
    )

    # Metal mounting bracket with screw hole and latch tab.
    bracket = (
        cq.Workplane("XY")
        .transformed(offset=(-GPU["length"] / 2 - 8, 0, 0))
        .box(16, 1.6, 120, centered=(True, True, False))
    )

    bracket = bracket.cut(
        cq.Workplane("YZ", origin=(-GPU["length"] / 2 - 8, 0, 0))
        .center(0, 100)
        .circle(2.2)
        .extrude(20)
    )

    latch_tab = (
        cq.Workplane("XY")
        .transformed(offset=(-GPU["length"] / 2 - 14, 0, 8))
        .box(5, 1.6, 14, centered=(True, True, False))
    )

    # Blower fan recessed into the shroud.
    fan_x = 55.0
    fan_z = 62.0
    fan_outer_r = 24.0
    fan_inner_r = 17.0

    fan_recess = (
        cq.Workplane("XZ", origin=(0, GPU["thickness"] / 2, 0))
        .center(fan_x, fan_z)
        .circle(fan_outer_r)
        .extrude(-4.0)
    )
    fan_hole = (
        cq.Workplane("XZ", origin=(0, GPU["thickness"] / 2 - 0.2, 0))
        .center(fan_x, fan_z)
        .circle(fan_inner_r)
        .extrude(-6.0)
    )

    fan_ring = (
        cq.Workplane("XZ", origin=(0, GPU["thickness"] / 2 - 2.0, 0))
        .center(fan_x, fan_z)
        .circle(fan_outer_r)
        .circle(fan_inner_r)
        .extrude(2.0)
    )

    # PCIe edge tab and gold contacts at the bottom.
    edge_tab = (
        cq.Workplane("XY")
        .transformed(offset=(-5, 0, -8))
        .box(110, 2.2, 8, centered=(True, True, False))
    )
    edge_notch = (
        cq.Workplane("XY")
        .transformed(offset=(15, 0, -8))
        .box(12, 3.0, 8, centered=(True, True, False))
    )
    contacts = (
        cq.Workplane("XY")
        .transformed(offset=(-5, 0, -8))
        .box(95, 0.6, 1.2, centered=(True, True, False))
    )

    # Dual 8-pin power connectors on top edge.
    pwr1 = (
        cq.Workplane("XY")
        .transformed(offset=(75, 0, GPU["height"]))
        .box(14, 12, 11, centered=(True, True, False))
    )
    pwr2 = (
        cq.Workplane("XY")
        .transformed(offset=(92, 0, GPU["height"]))
        .box(14, 12, 11, centered=(True, True, False))
    )
    pwr1_cut = (
        cq.Workplane("XY")
        .transformed(offset=(75, 0, GPU["height"] + 2))
        .box(9.5, 7, 8.0, centered=(True, True, False))
    )
    pwr2_cut = (
        cq.Workplane("XY")
        .transformed(offset=(92, 0, GPU["height"] + 2))
        .box(9.5, 7, 8.0, centered=(True, True, False))
    )

    gpu = body.union(bracket).union(latch_tab)
    gpu = gpu.cut(fan_recess).cut(fan_hole).union(fan_ring)
    gpu = gpu.union(edge_tab).cut(edge_notch).union(contacts)
    gpu = gpu.union(pwr1).union(pwr2).cut(pwr1_cut).cut(pwr2_cut)
    return gpu


def make_psu_envelope() -> cq.Workplane:
    body = cq.Workplane("XY").box(
        PSU["length"],
        PSU["width"],
        PSU["height"],
        centered=(True, True, False),
    )

    # Top fan opening and ring.
    fan_cut = (
        cq.Workplane("XY", origin=(0, 0, PSU["height"] - 0.1))
        .circle(56)
        .extrude(-3.0)
    )
    fan_ring = (
        cq.Workplane("XY", origin=(0, 0, PSU["height"] - 2.8))
        .circle(58)
        .circle(52)
        .extrude(2.8)
    )

    # Rear AC inlet and rocker switch cutouts.
    rear_x = -PSU["length"] / 2
    ac_cut = (
        cq.Workplane("YZ", origin=(rear_x + 0.2, 0, 0))
        .center(48, 28)
        .rect(27, 22)
        .extrude(-4.0)
    )
    switch_cut = (
        cq.Workplane("YZ", origin=(rear_x + 0.2, 0, 0))
        .center(20, 28)
        .rect(14, 19)
        .extrude(-4.0)
    )
    ac_bezel = (
        cq.Workplane("YZ", origin=(rear_x, 0, 0))
        .center(48, 28)
        .rect(35, 30)
        .extrude(-3.0)
    )
    switch_body = (
        cq.Workplane("YZ", origin=(rear_x, 0, 0))
        .center(20, 28)
        .rect(16, 21)
        .extrude(-2.5)
    )

    # Front modular connector blocks (motherboard + PCIe/CPU + SATA).
    front_x = PSU["length"] / 2
    port_defs = [
        (-48, 58, 18, 12),  # SATA/PATA
        (-5, 58, 18, 12),
        (40, 58, 30, 12),  # Motherboard pair
        (-45, 38, 18, 12),
        (-22, 38, 18, 12),
        (2, 38, 18, 12),
        (26, 38, 18, 12),
        (50, 38, 18, 12),
    ]

    ports = None
    port_voids = None
    for y_pos, z_pos, w, h in port_defs:
        port = (
            cq.Workplane("YZ", origin=(front_x, 0, 0))
            .center(y_pos, z_pos)
            .rect(w, h)
            .extrude(4.0)
        )
        void = (
            cq.Workplane("YZ", origin=(front_x + 0.1, 0, 0))
            .center(y_pos, z_pos)
            .rect(max(8.0, w - 4), max(8.0, h - 3))
            .extrude(3.2)
        )
        ports = port if ports is None else ports.union(port)
        port_voids = void if port_voids is None else port_voids.union(void)

    psu = body.cut(fan_cut).union(fan_ring)
    psu = psu.cut(ac_cut).cut(switch_cut).union(ac_bezel).union(switch_body)
    psu = psu.union(ports).cut(port_voids)
    return psu


def make_oculink_envelope() -> tuple[cq.Workplane, cq.Workplane]:
    board = cq.Workplane("XY").box(
        OCULINK["length"],
        OCULINK["width"],
        OCULINK["board_thickness"],
        centered=(True, True, False),
    )

    # Long PCIe x16 slot housing and key notch.
    pcie_slot = (
        cq.Workplane("XY")
        .transformed(offset=(-OCULINK["length"] / 2 + 56, 6.5, OCULINK["board_thickness"]))
        .box(89, 11, 12, centered=(True, True, False))
    )
    pcie_slot_key = (
        cq.Workplane("XY")
        .transformed(offset=(-OCULINK["length"] / 2 + 64, 6.5, OCULINK["board_thickness"] + 1))
        .box(9, 9, 10, centered=(True, True, False))
    )

    # 24-pin motherboard connector at the right side.
    atx24 = (
        cq.Workplane("XY")
        .transformed(offset=(OCULINK["length"] / 2 - 30, 13, OCULINK["board_thickness"]))
        .box(54, 11, 12, centered=(True, True, False))
    )
    atx24_void = (
        cq.Workplane("XY")
        .transformed(offset=(OCULINK["length"] / 2 - 30, 13, OCULINK["board_thickness"] + 2))
        .box(48, 7, 8, centered=(True, True, False))
    )

    # Oculink connector and switch.
    oculink_conn = (
        cq.Workplane("XY")
        .transformed(offset=(-OCULINK["length"] / 2 + 30, -2, OCULINK["board_thickness"]))
        .box(18, 8, 5, centered=(True, True, False))
    )
    switch = (
        cq.Workplane("XY")
        .transformed(offset=(OCULINK["length"] / 2 - 8, -19, OCULINK["board_thickness"]))
        .box(10, 4, 3, centered=(True, True, False))
    )

    # Cylindrical capacitors.
    caps = None
    for x_pos, y_pos, dia, h in [
        (-72, 16, 8, 10),
        (-58, 14, 7, 8),
        (-75, -12, 8, 9),
        (12, 15, 7, 9),
    ]:
        cap = cq.Workplane("XY").center(x_pos, y_pos).circle(dia / 2).extrude(h)
        caps = cap if caps is None else caps.union(cap)

    # Cable represented as two joined segments from the Oculink connector.
    cable_start_x = -OCULINK["length"] / 2 + 38
    cable_start_y = -2
    cable_z = OCULINK["board_thickness"] + 2.5

    cable_seg1 = (
        cq.Workplane("XY")
        .box(78, 5.2, 5.2, centered=(False, True, True))
        .translate((cable_start_x, cable_start_y, cable_z))
    )
    cable_seg2 = (
        cq.Workplane("XY")
        .box(65, 5.2, 5.2, centered=(False, True, True))
        .rotate((0, 0, 0), (0, 0, 1), 28)
        .translate((cable_start_x + 70, cable_start_y + 4, cable_z + 1.5))
    )
    cable = cable_seg1.union(cable_seg2)

    oculink = board.union(pcie_slot).union(atx24).cut(pcie_slot_key).cut(atx24_void)
    oculink = oculink.union(oculink_conn).union(switch)
    if caps is not None:
        oculink = oculink.union(caps)

    return oculink, cable


def make_rack_gpu_holder() -> cq.Workplane:
    depth = HOLDER["usable_depth"]
    base_w = HOLDER["base_width"]
    base_t = HOLDER["base_thickness"]
    wall_t = HOLDER["side_wall_thickness"]
    wall_h = HOLDER["side_wall_height"]

    # Main printable base tray.
    base = cq.Workplane("XY").box(depth, base_w, base_t, centered=(True, True, False))

    # Side walls form a horizontal GPU channel to prevent sag/bending.
    wall_left = (
        cq.Workplane("XY")
        .transformed(offset=(0, -base_w / 2 + wall_t / 2, base_t))
        .box(depth, wall_t, wall_h, centered=(True, True, False))
    )
    wall_right = (
        cq.Workplane("XY")
        .transformed(offset=(0, base_w / 2 - wall_t / 2, base_t))
        .box(depth, wall_t, wall_h, centered=(True, True, False))
    )

    # Internal channel relief for GPU thickness with clearance.
    channel = (
        cq.Workplane("XY")
        .transformed(offset=(0, 0, base_t + 4))
        .box(
            depth - 10,
            HOLDER["gpu_channel_width"],
            HOLDER["gpu_channel_height"],
            centered=(True, True, False),
        )
    )

    # Oculink adapter support platform at rear quarter.
    adapter_pad = (
        cq.Workplane("XY")
        .transformed(offset=(depth / 2 - HOLDER["adapter_pad_length"] / 2 - 18, 0, base_t))
        .box(HOLDER["adapter_pad_length"], 95, 5, centered=(True, True, False))
    )

    # Small anti-bend bridge between GPU channel and adapter zone.
    bridge = (
        cq.Workplane("XY")
        .transformed(offset=(depth / 2 - 115, 0, base_t + 5))
        .box(26, 62, 16, centered=(True, True, False))
    )

    # Rack ears and screw slots (front only, for open frame rail mounting).
    ear_t = 6.0
    ear_h = 44.45  # 1U nominal height
    ear_w = 38.0
    ear_x = -depth / 2 - ear_t / 2
    rail_half = HOLDER["rail_hole_spacing"] / 2

    ear_left = (
        cq.Workplane("XY")
        .transformed(offset=(ear_x, -rail_half, base_t))
        .box(ear_t, ear_w, ear_h, centered=(True, True, False))
    )
    ear_right = (
        cq.Workplane("XY")
        .transformed(offset=(ear_x, rail_half, base_t))
        .box(ear_t, ear_w, ear_h, centered=(True, True, False))
    )

    # Front rail arms connect the base tray to rack ears (prevents floating ears).
    arm_x = -depth / 2 + 10
    arm_t = 8.0
    arm_h = 14.0
    arm_y_len = rail_half - (base_w / 2) + 16

    arm_left = (
        cq.Workplane("XY")
        .transformed(offset=(arm_x, -(base_w / 2 + arm_y_len / 2), base_t + 2))
        .box(arm_t, arm_y_len, arm_h, centered=(True, True, False))
    )
    arm_right = (
        cq.Workplane("XY")
        .transformed(offset=(arm_x, (base_w / 2 + arm_y_len / 2), base_t + 2))
        .box(arm_t, arm_y_len, arm_h, centered=(True, True, False))
    )

    # Ear gussets for print strength.
    gusset_left = (
        cq.Workplane("XY")
        .transformed(offset=(ear_x + 3, -rail_half + 9, base_t))
        .box(10, 18, 20, centered=(True, True, False))
    )
    gusset_right = (
        cq.Workplane("XY")
        .transformed(offset=(ear_x + 3, rail_half - 9, base_t))
        .box(10, 18, 20, centered=(True, True, False))
    )

    # Vertical slots for M6-style rack hardware, with tolerance.
    slot_left = (
        cq.Workplane("YZ", origin=(ear_x + 0.2, -rail_half, 0))
        .center(0, base_t + 22)
        .slot2D(7.0, 18.0, 90)
        .extrude(-8)
    )
    slot_right = (
        cq.Workplane("YZ", origin=(ear_x + 0.2, rail_half, 0))
        .center(0, base_t + 22)
        .slot2D(7.0, 18.0, 90)
        .extrude(-8)
    )

    # Tie-down loops for cable management and retention straps.
    loop1 = (
        cq.Workplane("XY")
        .transformed(offset=(-20, -base_w / 2 + 18, base_t + 8))
        .box(14, 8, 9, centered=(True, True, False))
    )
    loop2 = (
        cq.Workplane("XY")
        .transformed(offset=(60, base_w / 2 - 18, base_t + 8))
        .box(14, 8, 9, centered=(True, True, False))
    )
    loop1_void = (
        cq.Workplane("XY")
        .transformed(offset=(-20, -base_w / 2 + 18, base_t + 10))
        .box(8, 4, 5, centered=(True, True, False))
    )
    loop2_void = (
        cq.Workplane("XY")
        .transformed(offset=(60, base_w / 2 - 18, base_t + 10))
        .box(8, 4, 5, centered=(True, True, False))
    )

    holder = base.union(wall_left).union(wall_right).union(adapter_pad).union(bridge)
    holder = holder.union(arm_left).union(arm_right)
    holder = holder.union(ear_left).union(ear_right).union(gusset_left).union(gusset_right)
    holder = holder.cut(channel).cut(slot_left).cut(slot_right)
    holder = holder.union(loop1).union(loop2).cut(loop1_void).cut(loop2_void)
    return holder


def make_vevor_rack() -> cq.Workplane:
    w = RACK["outer_width"]
    d = RACK["outer_depth"]
    h = RACK["outer_height"]
    post = RACK["post_size"]
    beam = RACK["beam_size"]

    # Corner posts.
    posts = None
    for x_pos in (-d / 2 + post / 2, d / 2 - post / 2):
        for y_pos in (-w / 2 + post / 2, w / 2 - post / 2):
            p = (
                cq.Workplane("XY")
                .transformed(offset=(x_pos, y_pos, 0))
                .box(post, post, h, centered=(True, True, False))
            )
            posts = p if posts is None else posts.union(p)

    # Top and bottom perimeter rails.
    def frame(z_base: float) -> cq.Workplane:
        front_back = (
            cq.Workplane("XY")
            .transformed(offset=(0, -w / 2 + beam / 2, z_base))
            .box(d, beam, beam, centered=(True, True, False))
            .union(
                cq.Workplane("XY")
                .transformed(offset=(0, w / 2 - beam / 2, z_base))
                .box(d, beam, beam, centered=(True, True, False))
            )
        )
        sides = (
            cq.Workplane("XY")
            .transformed(offset=(-d / 2 + beam / 2, 0, z_base))
            .box(beam, w - 2 * beam, beam, centered=(True, True, False))
            .union(
                cq.Workplane("XY")
                .transformed(offset=(d / 2 - beam / 2, 0, z_base))
                .box(beam, w - 2 * beam, beam, centered=(True, True, False))
            )
        )
        return front_back.union(sides)

    top_frame = frame(h - beam)
    bottom_frame = frame(0)

    rack = posts.union(top_frame).union(bottom_frame)

    # Add dedicated front/rear rack rails with square cage-nut pattern.
    # This keeps U holes visually aligned with mounted equipment.
    rail_t = 8.0
    rail_w = 20.0
    rail_y = 232.5  # Approx. half of 465 mm horizontal hole spacing.
    rail_x_front = -d / 2 + 16
    rail_x_rear = d / 2 - 16
    rail_z_h = h - 2 * beam

    rails = None
    for x_pos in (rail_x_front, rail_x_rear):
        for y_pos in (-rail_y, rail_y):
            r = (
                cq.Workplane("XY")
                .transformed(offset=(x_pos, y_pos, beam))
                .box(rail_t, rail_w, rail_z_h, centered=(True, True, False))
            )
            rails = r if rails is None else rails.union(r)

    if rails is not None:
        rack = rack.union(rails)

    # 3-hole repeating 1U square pattern on front and rear rails.
    sq = 9.5
    hole_offsets = (7.0, 22.875, 38.75)
    for rail_x in (rail_x_front, rail_x_rear):
        extrude_len = rail_t + 1.0 if rail_x < 0 else -(rail_t + 1.0)
        x_origin = rail_x - rail_t / 2 - 0.5 if rail_x < 0 else rail_x + rail_t / 2 + 0.5
        for y_pos in (-rail_y, rail_y):
            for u in range(RACK["units"]):
                base_z = beam + u * RACK["rack_hole_pitch"]
                for dz in hole_offsets:
                    zc = base_z + dz
                    hole = (
                        cq.Workplane("YZ", origin=(x_origin, y_pos, zc))
                        .rect(sq, sq)
                        .extrude(extrude_len)
                    )
                    rack = rack.cut(hole)

    # Bottom casters (simplified geometry).
    caster_h = RACK["caster_height"]
    wheel_r = RACK["caster_wheel_diameter"] / 2
    casters = None
    for x_pos in (-d / 2 + post / 2, d / 2 - post / 2):
        for y_pos in (-w / 2 + post / 2, w / 2 - post / 2):
            plate = (
                cq.Workplane("XY")
                .transformed(offset=(x_pos, y_pos, -6))
                .box(26, 26, 6, centered=(True, True, False))
            )
            stem = (
                cq.Workplane("XY")
                .transformed(offset=(x_pos, y_pos, -18))
                .cylinder(12, 5, centered=(True, True, False))
            )
            fork = (
                cq.Workplane("XY")
                .transformed(offset=(x_pos, y_pos, -caster_h + 16))
                .box(12, 20, 28, centered=(True, True, False))
            )
            wheel = (
                cq.Workplane("XY")
                .transformed(offset=(x_pos, y_pos, -caster_h))
                .cylinder(RACK["caster_wheel_diameter"], wheel_r, centered=(True, True, False))
            )
            caster = plate.union(stem).union(fork).union(wheel)
            casters = caster if casters is None else casters.union(caster)

    if casters is not None:
        rack = rack.union(casters)

    return rack


def u_bottom_z(u_index: int) -> float:
    return RACK["beam_size"] + (u_index - 1) * RACK["rack_hole_pitch"]


def make_top_panel() -> cq.Workplane:
    panel_t = RACK["top_panel_thickness"]
    return cq.Workplane("XY").box(
        RACK["outer_depth"] - 8,
        RACK["outer_width"] - 8,
        panel_t,
        centered=(True, True, False),
    ).translate((0, 0, RACK["outer_height"]))


def make_shelf(
    depth: float,
    width: float,
    thickness: float,
    z_base: float,
    y_offset: float,
    attach_back: bool,
) -> cq.Workplane:
    deck = cq.Workplane("XY").box(depth, width, thickness, centered=(True, True, False))
    deck = deck.translate((0, y_offset, z_base))

    rear_lip = (
        cq.Workplane("XY")
        .box(depth, 14, 22, centered=(True, True, False))
        .translate((0, y_offset - width / 2 + 7, z_base + thickness))
    )
    side_l = (
        cq.Workplane("XY")
        .box(12, width, 14, centered=(True, True, False))
        .translate((-depth / 2 + 6, y_offset, z_base + thickness))
    )
    side_r = (
        cq.Workplane("XY")
        .box(12, width, 14, centered=(True, True, False))
        .translate((depth / 2 - 6, y_offset, z_base + thickness))
    )

    shelf = deck.union(rear_lip).union(side_l).union(side_r)

    if attach_back:
        back_tabs = (
            cq.Workplane("XY")
            .box(12, 18, 22, centered=(True, True, False))
            .translate((-depth / 2 + 8, y_offset + width / 2 - 9, z_base + thickness))
            .union(
                cq.Workplane("XY")
                .box(12, 18, 22, centered=(True, True, False))
                .translate((depth / 2 - 8, y_offset + width / 2 - 9, z_base + thickness))
            )
        )
        shelf = shelf.union(back_tabs)

    return shelf


def make_homelab_layout() -> dict[str, cq.Workplane]:
    parts: dict[str, cq.Workplane] = {}

    # X = left/right, Y = front/back for Fusion-imported orientation.
    u1_x = 0
    u17_x = 0

    # Installed shelves.
    parts["shelf_u1_large"] = make_shelf(
        470, 430, 2.4, u_bottom_z(1) + 2, y_offset=25, attach_back=True
    )
    parts["shelf_u17_small"] = make_shelf(
        483, 465, 2.4, u_bottom_z(17) + 2, y_offset=0, attach_back=True
    )
    parts["top_panel"] = make_top_panel()

    # 1U rack devices.
    front_face_y = -RACK["outer_width"] / 2

    udm_core = cq.Workplane("XY").box(430, 286, 44, centered=(True, True, False))
    udm_ear_l = cq.Workplane("XY").box(26, 14, 44, centered=(True, True, False)).translate((-228, -136, 0))
    udm_ear_r = cq.Workplane("XY").box(26, 14, 44, centered=(True, True, False)).translate((228, -136, 0))
    udm_pro = udm_core.union(udm_ear_l).union(udm_ear_r)
    udm_pro = udm_pro.translate((0, front_face_y + 286 / 2, u_bottom_z(13) + 2))
    parts["udm_pro_u13"] = udm_pro

    rps_core = cq.Workplane("XY").box(430, 325, 44, centered=(True, True, False))
    rps_ear_l = cq.Workplane("XY").box(26, 14, 44, centered=(True, True, False)).translate((-228, -156, 0))
    rps_ear_r = cq.Workplane("XY").box(26, 14, 44, centered=(True, True, False)).translate((228, -156, 0))
    usp_rps = rps_core.union(rps_ear_l).union(rps_ear_r)
    usp_rps = usp_rps.translate((0, front_face_y + 325 / 2, u_bottom_z(14) + 2))
    parts["usp_rps_u14"] = usp_rps

    patch_panel = cq.Workplane("XY").box(483, 95, 44.5, centered=(True, True, False))
    patch_panel = patch_panel.translate((0, front_face_y + 95 / 2, u_bottom_z(16) + 2))
    parts["patch_panel_u16"] = patch_panel

    # Visible rack standoff blocks at mounting points.
    standoff_y = front_face_y + 8
    for u_idx in (13, 14, 16):
        zc = u_bottom_z(u_idx) + 22
        block_pair = (
            cq.Workplane("XY")
            .box(10, 10, 10, centered=(True, True, True))
            .translate((-232.5, standoff_y, zc))
            .union(
                cq.Workplane("XY")
                .box(10, 10, 10, centered=(True, True, True))
                .translate((232.5, standoff_y, zc))
            )
        )
        parts[f"standoff_u{u_idx}"] = block_pair

    # Rack rail face strips — proper-looking vertical flanges with punched hole pattern.
    # Four strips: front-left, front-right, rear-left, rear-right.
    # Each is a continuous plate (22 mm wide, 3 mm thick) running the full rack height
    # with the standard 3-hole-per-U square pattern cut through it.
    strip_t = 3.0    # Y thickness (front-to-back depth of the face plate)
    strip_w = 22.0   # X width (matches real rack rail flange width)
    strip_h = RACK["outer_height"] - RACK["beam_size"]
    strip_z = RACK["beam_size"]
    hole_x_w = 7.0   # X width of each punched slot
    hole_z_h = 9.5   # Z height of each punched slot
    hole_dz_offsets = (7.0, 22.875, 38.75)
    rear_face_y = RACK["outer_width"] / 2

    rail_strips = None
    for y_start in (front_face_y, rear_face_y - strip_t):
        for x_pos in (-232.5, 232.5):
            strip = (
                cq.Workplane("XY")
                .box(strip_w, strip_t, strip_h, centered=(True, False, False))
                .translate((x_pos, y_start, strip_z))
            )
            # Build all holes as a single compound then cut once for efficiency.
            all_holes = None
            for u in range(1, RACK["units"] + 1):
                u_base_z = strip_z + (u - 1) * RACK["rack_hole_pitch"]
                for dz in hole_dz_offsets:
                    zc = u_base_z + dz
                    hole = (
                        cq.Workplane("XY")
                        .box(hole_x_w, strip_t + 2.0, hole_z_h, centered=(True, True, True))
                        .translate((x_pos, y_start + strip_t / 2, zc))
                    )
                    all_holes = hole if all_holes is None else all_holes.union(hole)
            if all_holes is not None:
                strip = strip.cut(all_holes)
            rail_strips = strip if rail_strips is None else rail_strips.union(strip)

    if rail_strips is not None:
        parts["rack_u_hole_markers"] = rail_strips

    # U15 loose Raspberry Pi on top of RPS.
    rpi = cq.Workplane("XY").box(88, 58, 20, centered=(True, True, False))
    rpi = rpi.translate((145, -120, u_bottom_z(14) + 48))
    parts["raspberry_pi_u15"] = rpi

    # Large shelf contents near U1.
    d4_320 = cq.Workplane("XY").box(222, 179, 154, centered=(True, True, False))
    d4_320 = d4_320.translate((0, 95, u_bottom_z(1) + 6))
    parts["terrmaster_d4_320"] = d4_320

    time_capsule = cq.Workplane("XY").box(98, 98, 168, centered=(True, True, False))
    time_capsule = time_capsule.translate((170, -135, u_bottom_z(1) + 6))
    parts["time_capsule"] = time_capsule

    p52s = cq.Workplane("XY").box(252, 377, 23, centered=(True, True, False))
    p52s = p52s.translate((0, 165, u_bottom_z(1) + 162))
    parts["lenovo_p52s"] = p52s

    # Small shelf contents at U17-U20 zone.
    wii = cq.Workplane("XY").box(45, 158, 216, centered=(True, True, False))
    wii = wii.translate((u17_x + 10, 155, u_bottom_z(17) + 6))
    wii_stand = cq.Workplane("XY").box(80, 110, 12, centered=(True, True, False))
    wii_stand = wii_stand.translate((u17_x + 10, 155, u_bottom_z(17) + 2))
    parts["nintendo_wii"] = wii.union(wii_stand)

    unifi_psu = cq.Workplane("XY").box(90, 55, 32, centered=(True, True, False))
    unifi_psu = unifi_psu.translate((u17_x + 95, -175, u_bottom_z(17) + 6))
    parts["unifi_power_supply"] = unifi_psu

    joycon_l = cq.Workplane("XY").box(20, 35, 100, centered=(True, True, False))
    joycon_l = joycon_l.translate((u17_x - 120, -185, u_bottom_z(17) + 6))
    joycon_r = cq.Workplane("XY").box(20, 35, 100, centered=(True, True, False))
    joycon_r = joycon_r.translate((u17_x - 120, -145, u_bottom_z(17) + 6))
    parts["joycons"] = joycon_l.union(joycon_r)

    # Dock rotated to vertical orientation for tighter footprint.
    n_switch_dock = cq.Workplane("XY").box(170, 40, 104, centered=(True, True, False))
    n_switch_dock = n_switch_dock.translate((u17_x - 35, -105, u_bottom_z(17) + 6))
    parts["nintendo_switch"] = n_switch_dock

    # Sky Mini and Apple TV dimensions are approximate planning envelopes.
    sky_box = cq.Workplane("XY").box(160, 145, 35, centered=(True, True, False))
    sky_box = sky_box.translate((u17_x + 10, -20, u_bottom_z(17) + 6))
    parts["sky_box"] = sky_box

    ms_a1 = cq.Workplane("XY").box(160, 160, 48, centered=(True, True, False))
    ms_a1 = ms_a1.translate((u17_x + 95, 135, u_bottom_z(17) + 6))
    parts["minisforum_ms_a1"] = ms_a1

    hue_big = cq.Workplane("XY").box(89, 89, 26, centered=(True, True, False))
    hue_big = hue_big.translate((u17_x - 5, 170, u_bottom_z(17) + 6))
    hue_small = cq.Workplane("XY").box(64, 64, 20, centered=(True, True, False))
    hue_small = hue_small.translate((u17_x - 5, 170, u_bottom_z(17) + 33))
    parts["hue_bridge"] = hue_big.union(hue_small)

    apple_tv = cq.Workplane("XY").box(93, 93, 31, centered=(True, True, False))
    apple_tv = apple_tv.translate((u17_x + 140, 165, u_bottom_z(17) + 6))
    parts["apple_tv"] = apple_tv

    wii_psu = cq.Workplane("XY").box(60, 45, 30, centered=(True, True, False))
    wii_psu = wii_psu.translate((u17_x + 65, 118, u_bottom_z(17) + 6))
    parts["wii_power_supply"] = wii_psu

    return parts


def make_rack_insertion_markers() -> tuple[cq.Workplane, cq.Workplane, cq.Workplane]:
    # Marker volumes for manual placement in CAD.
    gpu_zone = (
        cq.Workplane("XY")
        .transformed(offset=(0, 0, 140))
        .box(300, 90, 130, centered=(True, True, False))
    )
    oculink_zone = (
        cq.Workplane("XY")
        .transformed(offset=(120, 0, 120))
        .box(210, 85, 70, centered=(True, True, False))
    )
    psu_zone = (
        cq.Workplane("XY")
        .transformed(offset=(40, -120, 120))
        .box(190, 170, 110, centered=(True, True, False))
    )
    return gpu_zone, oculink_zone, psu_zone


def export_part(part: cq.Workplane, name: str) -> None:
    step_path = OUTPUT_DIR / f"{name}.step"
    stl_path = OUTPUT_DIR / f"{name}.stl"
    part.val().exportStep(str(step_path))
    part.val().exportStl(str(stl_path), tolerance=0.1, angularTolerance=0.1)


def export_assembly(
    gpu: cq.Workplane,
    psu: cq.Workplane,
    oculink: cq.Workplane,
    oculink_cable: cq.Workplane,
    holder: cq.Workplane,
) -> None:
    assy = cq.Assembly(name="rackmount_parts")

    assy.add(gpu, name="gpu_frontier_air", color=cq.Color(0.1, 0.4, 0.9))

    psu_loc = cq.Location(cq.Vector(300, 0, 0))
    assy.add(psu, name="psu_rm750x", loc=psu_loc, color=cq.Color(0.8, 0.8, 0.8))

    oculink_loc = cq.Location(cq.Vector(300, 140, 0))
    assy.add(
        oculink,
        name="oculink_adapter",
        loc=oculink_loc,
        color=cq.Color(0.2, 0.8, 0.2),
    )

    assy.add(
        oculink_cable,
        name="oculink_cable",
        loc=oculink_loc,
        color=cq.Color(0.1, 0.1, 0.1),
    )

    holder_loc = cq.Location(cq.Vector(-220, 0, 0))
    assy.add(holder, name="rack_gpu_holder", loc=holder_loc, color=cq.Color(0.3, 0.3, 0.3))

    assy.export(str(OUTPUT_DIR / "rackmount_parts.step"))


def export_holder_fit_assembly(
    gpu: cq.Workplane,
    oculink: cq.Workplane,
    oculink_cable: cq.Workplane,
    holder: cq.Workplane,
) -> None:
    assy = cq.Assembly(name="rack_holder_fit")

    assy.add(holder, name="rack_gpu_holder", color=cq.Color(0.3, 0.3, 0.3))

    # Single GPU in horizontal channel (no duplicate overlap).
    gpu_loc = cq.Location(cq.Vector(20, 0, 11))
    assy.add(gpu, name="gpu_frontier_air", loc=gpu_loc, color=cq.Color(0.1, 0.4, 0.9))

    # Oculink support near rear bridge.
    oculink_loc = cq.Location(cq.Vector(118, 0, 6))
    assy.add(oculink, name="oculink_adapter", loc=oculink_loc, color=cq.Color(0.2, 0.8, 0.2))
    assy.add(oculink_cable, name="oculink_cable", loc=oculink_loc, color=cq.Color(0.1, 0.1, 0.1))

    assy.export(str(OUTPUT_DIR / "rack_holder_fit.step"))


def export_rack_template_assembly(
    rack: cq.Workplane,
    gpu_zone: cq.Workplane,
    oculink_zone: cq.Workplane,
    psu_zone: cq.Workplane,
) -> None:
    assy = cq.Assembly(name="vevor_20u_rack_template")
    assy.add(rack, name="vevor_20u_rack", color=cq.Color(0.2, 0.2, 0.2))
    assy.add(gpu_zone, name="zone_gpu", color=cq.Color(0.1, 0.5, 0.9, 0.35))
    assy.add(oculink_zone, name="zone_oculink", color=cq.Color(0.1, 0.9, 0.3, 0.35))
    assy.add(psu_zone, name="zone_psu", color=cq.Color(0.9, 0.8, 0.2, 0.35))
    assy.export(str(OUTPUT_DIR / "vevor_20u_rack_template.step"))


def export_loaded_homelab_assembly(rack: cq.Workplane, homelab_parts: dict[str, cq.Workplane]) -> None:
    assy = cq.Assembly(name="vevor_20u_loaded")
    assy.add(rack, name="vevor_20u_rack", color=cq.Color(0.2, 0.2, 0.2))

    color_map = {
        "udm_pro_u13": cq.Color(0.6, 0.8, 1.0),
        "usp_rps_u14": cq.Color(1.0, 0.8, 0.2),
        "patch_panel_u16": cq.Color(0.8, 0.8, 0.8),
        "raspberry_pi_u15": cq.Color(0.2, 0.8, 0.2),
        "lenovo_p52s": cq.Color(0.1, 0.1, 0.1),
        "terrmaster_d4_320": cq.Color(0.7, 0.7, 0.75),
        "time_capsule": cq.Color(0.95, 0.95, 0.95),
        "nintendo_wii": cq.Color(0.95, 0.95, 0.95),
        "unifi_power_supply": cq.Color(0.9, 0.9, 0.9),
        "nintendo_switch": cq.Color(0.9, 0.2, 0.2),
        "apple_tv": cq.Color(0.15, 0.15, 0.15),
        "sky_box": cq.Color(0.2, 0.2, 0.25),
        "minisforum_ms_a1": cq.Color(0.6, 0.6, 0.62),
        "hue_bridge": cq.Color(0.95, 0.95, 0.95),
        "wii_power_supply": cq.Color(0.1, 0.1, 0.1),
        "joycons": cq.Color(0.2, 0.4, 0.9),
        "shelf_u1_large": cq.Color(0.1, 0.1, 0.1),
        "shelf_u17_small": cq.Color(0.1, 0.1, 0.1),
        "top_panel": cq.Color(0.12, 0.12, 0.12),
        "standoff_u13": cq.Color(0.85, 0.85, 0.85),
        "standoff_u14": cq.Color(0.85, 0.85, 0.85),
        "standoff_u16": cq.Color(0.85, 0.85, 0.85),
        "rack_u_hole_markers": cq.Color(0.95, 0.95, 0.95),
    }

    for name, part in homelab_parts.items():
        assy.add(part, name=name, color=color_map.get(name, cq.Color(0.6, 0.6, 0.6)))

    assy.export(str(OUTPUT_DIR / "vevor_20u_loaded.step"))


def main() -> None:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    gpu = make_gpu_envelope()
    psu = make_psu_envelope()
    oculink, oculink_cable = make_oculink_envelope()
    holder = make_rack_gpu_holder()
    rack = make_vevor_rack()
    homelab_parts = make_homelab_layout()
    gpu_zone, oculink_zone, psu_zone = make_rack_insertion_markers()

    export_part(gpu, GPU["name"])
    export_part(psu, PSU["name"])
    export_part(oculink, OCULINK["name"])
    export_part(oculink_cable, "oculink_cable")
    export_part(holder, HOLDER["name"])
    export_part(rack, RACK["name"])
    for part_name, part in homelab_parts.items():
        export_part(part, part_name)
    export_part(gpu_zone, "zone_gpu")
    export_part(oculink_zone, "zone_oculink")
    export_part(psu_zone, "zone_psu")
    export_assembly(gpu, psu, oculink, oculink_cable, holder)
    export_holder_fit_assembly(gpu, oculink, oculink_cable, holder)
    export_rack_template_assembly(rack, gpu_zone, oculink_zone, psu_zone)
    export_loaded_homelab_assembly(rack, homelab_parts)

    print("Generated files in:", OUTPUT_DIR.resolve())


if __name__ == "__main__":
    main()
