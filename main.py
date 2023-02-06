import os

video_systems = ["Avatar", "DJI O3", "DJI", "Analog"]
receivers = ["FrSky", "Crossfire", "Ghost", "ELRS", "DJI"]


def new_name_line(video_system, receiver, file_name):
    prefix = file_name.split(" ")[0]
    return f"set name = {prefix} {video_system} {receiver}"


def new_video_system_lines(video_system, file_name):
    new_lines = []
    if video_system == "Avatar":
        new_lines.append("set osd_displayport_device = MSP")
        if file_name.startswith("Cinewhoop" or "Skylite" or "Moongoat"):
            new_lines.append("set displayport_msp_serial = 2")
        else:
            new_lines.append("set displayport_msp_serial = 1")
    elif video_system == "DJI O3":
        new_lines.append("set osd_displayport_device = MSP")
        if file_name.startswith("Cinewhoop" or "Skylite" or "Moongoat"):
            new_lines.append("set displayport_msp_serial = 2")
        else:
            new_lines.append("set displayport_msp_serial = 1")
    elif video_system == "DJI":
        new_lines.append("set osd_displayport_device = AUTO")
    elif video_system == "Analog":
        new_lines.append("set osd_displayport_device = AUTO")
        if file_name.startswith("Cinewhoop" or "Skylite" or "Moongoat"):
            new_lines.append("serial 2 8192 115200 57600 0 115200")
        else:
            new_lines.append("serial 2 8192 115200 57600 0 115200")
    return "\n".join(new_lines)


def new_receiver_lines(receiver):
    new_lines = []
    if receiver == "FrSky":
        new_lines.append("set serialrx_provider = SBUS")
        new_lines.append("map AETR1234")
    elif receiver == "Crossfire":
        new_lines.append("set serialrx_provider = CRSF")
        new_lines.append("map TAER1234")
    elif receiver == "Ghost":
        new_lines.append("set serialrx_provider = GHST")
        new_lines.append("map AETR1234")
    elif receiver == "ELRS":
        new_lines.append("set serialrx_provider = CRSF")
        new_lines.append("map TAER1234")
    elif receiver == "DJI":
        new_lines.append("set serialrx_provider = SBUS")
        new_lines.append("map AETR1234")
    return "\n".join(new_lines)


def new_aux_lines(video_system, receiver):
    new_lines = []
    if video_system == "DJI O3" and receiver == "DJI":
        new_lines.append("aux 0 0 3 1700 2100 0 0")
        new_lines.append("aux 1 1 0 900 1650 0 0")
        new_lines.append("aux 2 13 2 1700 2100 0 0")
        new_lines.append("aux 3 35 1 1700 2100 0 0")
    else:
        new_lines.append("aux 0 0 0 1700 2100 0 0")
        new_lines.append("aux 1 1 1 1700 2100 0 0")
        new_lines.append("aux 2 13 3 1700 2100 0 0")
        new_lines.append("aux 3 35 2 1700 2100 0 0")
    return "\n".join(new_lines)


def new_file_name(file_name, video_system, receiver):
    prefix = file_name.split(" - ")[0]
    return f"{prefix} - {video_system} {receiver}.txt"


def new_file_content(file_contents, video_system, receiver, file_name):
    lines = file_contents.split("\n")
    modified_lines = []
    for line in lines:
        if not line.startswith("save"):
            modified_lines.append(line)

        if line.startswith("save"):
            modified_lines.append(new_name_line(video_system, receiver, file_name))
            modified_lines.append(new_video_system_lines(video_system, file_name))
            modified_lines.append(new_receiver_lines(receiver))
            modified_lines.append(new_aux_lines(video_system, receiver))
            modified_lines.append(line)
    return "\n".join(modified_lines)


def create_file_variants(folder_name):
    source_file = [f for f in os.listdir(folder_name) if f.endswith(".txt")][0]
    file_name = source_file.split(".")[0]
    with open(os.path.join(folder_name, source_file), "r") as f:
        file_contents = f.read()

    variants_folder = os.path.join(folder_name, "variants")
    if not os.path.exists(variants_folder):
        os.makedirs(variants_folder)

    for video_system in video_systems:
        for receiver in receivers:
            if (video_system == "Avatar" or video_system == "Analog") and receiver == "DJI":
                continue
            new_name = new_file_name(file_name, video_system, receiver)
            new_content = new_file_content(
                file_contents, video_system, receiver, file_name)
            with open(os.path.join(variants_folder, new_name), "w") as f:
                f.write(new_content)


if __name__ == "__main__":
    folder_name = "."
    create_file_variants(folder_name)
