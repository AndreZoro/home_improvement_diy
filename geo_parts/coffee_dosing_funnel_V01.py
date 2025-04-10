import io
import tempfile
import os
# import build123d as bd
from build123d import *


def coffee_dosing_build123d_V01(i_dia = 58,
    i_dpth = 8,
    o_dia = 68,
    upper_dia = 80,
    top_height = 20,
    cutout = True,
    cutout_wdth = 24):

    msgs = []

    lower_thickness = 1.2
    upper_thickness = 2.4

    if o_dia <= i_dia + 2:
        o_dia = i_dia + 2
        msgs.append(f"Outer diamater was smaller than the inner diameter. I increased it to: {o_dia:.2f}mm")

    if upper_dia <= o_dia:
        upper_dia = o_dia
        msgs.append(f"Upper funnel diamater was smaller than the inner diameter. I increased it to: {upper_dia:.2f}mm")
    if cutout_wdth * 2.0 > i_dia:
        cutout_wdth = i_dia * 0.5
        msgs.append(f"Cutout width was a bit large. I reduced it to: {cutout_wdth:.2f}mm")

    mid_chpf_lgth = (o_dia - i_dia) / 8

    pts = [
        (i_dia/2.0-lower_thickness, -i_dpth), # 0
        (i_dia/2.0, -i_dpth), # 1
        (i_dia/2.0, 0), # 2
        (o_dia/2.0, 0), # 3
        (upper_dia/2.0, top_height), # 4
        (upper_dia/2.0 - upper_thickness, top_height), # 5
        (i_dia/2.0-lower_thickness, upper_thickness), # 6
        (i_dia/2.0-lower_thickness, -i_dpth), # 0
    ]

    f_lines = Polyline(pts)
    f_sk = make_face(f_lines)
    f_body = revolve(f_sk, Axis.Y)


    try:
        # Lower champfer:
        f_body = chamfer(f_body.edges().sort_by(Axis.Y)[1], length=lower_thickness*0.5)
        # Mid champfer:
        f_body = chamfer(f_body.edges().sort_by(Axis.Y)[7], length=mid_chpf_lgth)
        # Upper Chanpfers:
        f_body = chamfer(f_body.edges().sort_by(Axis.Y)[-2:], length=upper_thickness/4.0)
        # Inner mid radius
        f_body = fillet(f_body.edges().sort_by(Axis.Y)[10], radius=4.0*upper_thickness)

    except:
        pass


    # Time to create the cutout:
    if cutout:
        c_pts = [
            (-upper_thickness, -i_dpth), # 0
            (-upper_thickness, -i_dpth * 0.65), # 1
            (-cutout_wdth/2.0, upper_thickness), # 2
            (-cutout_wdth/2.0 * 1.8, top_height * 2.0), # 3
            ( cutout_wdth/2.0 * 1.8, top_height * 2.0), # 4
            ( cutout_wdth/2.0, upper_thickness), # 5
            ( upper_thickness, -i_dpth * 0.65), # 6
            ( upper_thickness, -i_dpth), # 7
            (-upper_thickness, -i_dpth) # 0
        ]

        c_lines = Polyline(c_pts)
        c_sk = make_face(c_lines)
        c_body = extrude(c_sk, upper_dia * 2)

        f_body -= c_body


    return f_body, msgs



def create_coffee_dosing_funnel_V01(
    i_dia = 58,
    i_dpth = 8,
    o_dia = 68,
    upper_dia = 80,
    top_height = 20,
    cutout = True,
    cutout_wdth = 24,
    # sid=''
):
    params = locals()
    params_string = ""
    for k,v in params.items():
        params_string += f"-{k}-{v}".replace('.','d')
    part_file_name = f"coffee_dosing_funnel{params_string}.stl"

    pyvista_part, messages = coffee_dosing_build123d_V01(i_dia,i_dpth,o_dia,upper_dia,top_height,cutout,cutout_wdth)

#     part_file_name = f"coffee_dosing_funnel{params_string}.stl"
#     # print(f"Exporting to: {part_file_name}")
#     fd, temp_file_name = tempfile.mkstemp(prefix=part_file_name[:-4], suffix=part_file_name[-4:])
#     print(f"Exporting to: {temp_file_name}")
#     export_stl(pyvista_part, temp_file_name)
#     os.close(fd)
#
    # Use tempfile.gettempdir() to get the system temporary directory
    temp_dir = tempfile.gettempdir()
    custom_temp_path = os.path.join(temp_dir, part_file_name)
    # print(f"Exporting to: {custom_temp_path}")
    export_stl(pyvista_part, custom_temp_path)



    # # Write to the custom-named temporary file
    # with open(custom_temp_path, 'w') as temp_file:
    #     temp_file.write("This is a temporary file with a custom name.")


    return custom_temp_path, messages
