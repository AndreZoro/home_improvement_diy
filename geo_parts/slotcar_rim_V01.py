import cadquery as cq
# import mmap
import os
import tempfile
# import io


def make_rim_tire(
    geo_part="tire",
    whl_dia=20.0,
    axl_dia=3.0,
    whl_wdt=10.0,
    tre_dia=24.0,
    bck_spc=2.0,
    cnv_dtp=2.0,
    sld_hgt=1.0,
    sld_wdt=5.0,
    sld_pos=2.5,
    n_holes=5,
    main_dia=6.0,
    hole_dia=5.0,
    lyr_hgt=0.12,
    nzl_wdt=0.4,
    spoke_dropdown="Lambo Style",
    sid='none',
):
    # print(f"Creating {geo_part} stl part.")
    # everything in mm
    # base rim
    layer_height = lyr_hgt
    backspacing = bck_spc
    # axl_dia = 3
    # ( axl_dpt = 6 ) gets calculated
    conv_dpt = cnv_dtp
    tot_wdt = whl_wdt
    # whl_dia = 20
    # sld_hgt = 0.8
    # sld_pos = 3
    # sld_wdt = 5

    # tire:
    tire_outer_dia = tre_dia

    # base lambo holes
    # use_lambo_holes = True
    main_lambo_rad = main_dia * 2
    n_lambo_holes = n_holes
    lambo_hole_dia = hole_dia

    # calculated_vals:
    x1 = min(4 * layer_height, 1)
    x2 = 2 * x1
    at = axl_dia / 2 + x1
    axl_cov = 3 * layer_height
    axl_dpt = tot_wdt - conv_dpt - backspacing - axl_cov
    x3 = 1.15 * axl_dia / 2
    x4 = axl_dia / 4.5
    x5 = x4
    x6 = min(3 * layer_height, 1)
    # x7 = sld_hgt*(2**0.5) # WRONG: x7 should be sld_hgt
    out_thk = 0.1 * whl_dia / 2
    x8 = 0.3 * out_thk
    x9 = 2 * x8
    x10 = backspacing + axl_dpt - x5  # Maybe more time x5
    x14 = 2 * x9
    x15 = 2 * x14
    x11 = axl_dia / 2
    x13 = x11
    x16 = whl_dia / 2 - out_thk - x14 - x13 - at - axl_dia / 2

    axl_rad = axl_dia / 2
    xx1 = axl_rad + at
    xx2 = axl_rad + x1
    whl_rad = whl_dia / 2

    messages = []
    # part_io = io.BytesIO()

    if axl_dpt < 2.4 * axl_dia:
        messages.append(f"Pretty small axel depth of {axl_dpt:.2f}mm.")
        messages.append("Try reducing backspacing or concavity.")

    if x16 < 0.1 * whl_dia / 2:
        messages.append(f"DIM X16 is too small ({x16}mm)!")

    if tire_outer_dia < whl_dia * 1.05:
        messages.append("Outer tire diameter is to small")
        tire_outer_dia = whl_dia * 1.05
        messages.append(f"Tire diameter automatically increaed to: {tire_outer_dia}mm.")

    if geo_part == "rim":
        # breakpoint()
        rim_sketch = (
            cq.Sketch()
            # cq.Workplane()
            # .sketch()
            .segment((xx1, backspacing), (xx2, backspacing))
            .segment((axl_rad, backspacing + x2))
            .segment((axl_rad, backspacing + axl_dpt))
            .segment((0, backspacing + axl_dpt))
            .segment((0, backspacing + axl_dpt + axl_cov))
            .segment((x3, backspacing + axl_dpt + axl_cov))
            .segment((x3 + x4, backspacing + axl_dpt + axl_cov - x5))
            .segment((whl_rad - x6, tot_wdt))
            .segment((whl_rad, tot_wdt))
            .segment((whl_rad, tot_wdt - sld_pos))
            .segment((whl_rad + sld_hgt, tot_wdt - sld_pos))
            .segment((whl_rad + sld_hgt, tot_wdt - sld_pos - sld_wdt + sld_hgt))
            .segment((whl_rad + sld_hgt - sld_hgt, tot_wdt - sld_pos - sld_wdt))
            .segment((whl_rad, 0))
            .segment((whl_rad - out_thk + x8, 0))
            .segment((whl_rad - out_thk, x9))  # AA
            .segment((whl_rad - out_thk, x10 - x15))
            .segment((whl_rad - out_thk - x14, x10))
            .segment((xx1 + x13, x10))
            .segment((xx1, backspacing + x11))
            .close()
            .assemble()
        )
        base_rim_revolved = cq.Workplane().placeSketch(rim_sketch).revolve()

        if spoke_dropdown == "Lambo Style":
            # Cut lambo style holes
            base_rim_revolved = (
                base_rim_revolved.faces(">Y")
                .workplane()
                .polygon(n_lambo_holes, main_lambo_rad)
                .vertices()
                .hole(lambo_hole_dia)
                # .cutThruAll()
            )

        part_file_name = f"rim_{sid}.stl"
        print(f"Exporting {geo_part} stl part as {part_file_name}.")
        # cq.exporters.export(base_rim_revolved, part_io, 'STL')

        # Create a temporary file
        fd, temp_file_name = tempfile.mkstemp(prefix=part_file_name[:-4], suffix=part_file_name[-4:])
        # Close the file descriptor
        os.close(fd)


        # with tempfile.NamedTemporaryFile(delete=False, suffix=".stl") as temp_file:
        #     temp_file_path = temp_file.name
        # breakpoint()
        # Export to the temporary file using its path
        cq.exporters.export(base_rim_revolved, temp_file_name, "STL")

        # # Read the STL data from the temporary file
        # with open(temp_file_path, "rb") as file:
        #     stl_data = file.read()
        # stl_data.seek(0)
        return temp_file_name, messages

    if geo_part == "tire":
        tire_sketch = (
            cq.Sketch()
            # .arc
            .segment((whl_dia / 2 + 0.01, tot_wdt), (tire_outer_dia / 2, tot_wdt))
            .segment((tire_outer_dia / 2, 0))
            # .arc
            .segment((whl_dia / 2 + 0.01, 0))
            .close()
            .assemble()
        )
        tire = cq.Workplane().placeSketch(tire_sketch).revolve()

        part_file_name = f"tire_{sid}.stl"
        print(f"Exporting {geo_part} stl part as {part_file_name}.")
        # Create a temporary file
        fd, temp_file_name = tempfile.mkstemp(prefix=part_file_name[:-4], suffix=part_file_name[-4:])
        # Close the file descriptor
        os.close(fd)

        # Create a temporary file
        # with tempfile.NamedTemporaryFile(delete=False, suffix=".stl") as temp_file:
        #     temp_file_path = temp_file.name
        # breakpoint()
        # Export to the temporary file using its path
        cq.exporters.export(tire, temp_file_name, "STL")

        # Read the STL data from the temporary file
        # with open(temp_file_path, "rb") as file:
        #     stl_data = file.read()
        # stl_data.seek(0)

        return temp_file_name, [""]
