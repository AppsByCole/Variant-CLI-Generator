import os

video_systems = ["Avatar", "DJI O3", "DJI", "Analog"]
receivers = ["FrSky", "Crossfire", "Ghost", "ELRS", "DJI"]


def new_video_system_lines(line, video_system, file_name):
    if video_system == "Avatar":
        if line.startswith("set osd_displayport_device = "):
            return "set osd_displayport_device = MSP"
        elif line.startswith("set displayport_msp_serial = "):
            if file_name.startswith("Cinewhoop" or "Skylite" or "Moongoat"):
                return "set displayport_msp_serial = 2"
            return "set displayport_msp_serial = 1"
    elif video_system == "DJI O3":
        if line.startswith("set osd_displayport_device = "):
            return "set osd_displayport_device = MSP"
        elif line.startswith("set displayport_msp_serial = "):
            return "set displayport_msp_serial = 1"
        pass
    elif video_system == "DJI":
        if line.startswith("set osd_displayport_device = "):
            return "set osd_displayport_device = AUTO"
    elif video_system == "Analog":
        if line.startswith("set osd_displayport_device = "):
            return "set osd_displayport_device = AUTO"
    return line


def new_receiver_lines(line, receiver):
    if receiver == "FrSky":
        if line.startswith("set serialrx_provider = "):
            return "set serialrx_provider = SBUS"
        elif line.startswith("map "):
            return "map AETR1234"
    elif receiver == "Crossfire":
        if line.startswith("set serialrx_provider = "):
            return "set serialrx_provider = CRSF"
        elif line.startswith("map "):
            return "map TAER1234"
    elif receiver == "Ghost":
        if line.startswith("set serialrx_provider = "):
            return "set serialrx_provider = GHST"
        elif line.startswith("map "):
            return "map AETR1234"
    elif receiver == "ELRS":
        if line.startswith("set serialrx_provider = "):
            return "set serialrx_provider = CRSF"
        elif line.startswith("map "):
            return "map TAER1234"
    elif receiver == "DJI":
        if line.startswith("set serialrx_provider = "):
            return "set serialrx_provider = SBUS"
        elif line.startswith("map "):
            return "map AETR1234"
    return line


def new_name_line(line, video_system, receiver, file_name):
    if line.startswith("set name = "):
        prefix = file_name.split(" ")[0]
        return f"set name = {prefix} {video_system} {receiver}"
    return line


def new_aux_lines(line, video_system, receiver):
    if video_system == "DJI O3" and receiver == "DJI":
        if line.startswith("aux 0"):
            return "aux 0 0 3 1700 2100 0 0"
        elif line.startswith("aux 1"):
            return "aux 1 1 0 900 1650 0 0"
        elif line.startswith("aux 2"):
            return "aux 2 13 2 1700 2100 0 0"
        elif line.startswith("aux 3"):
            return "aux 3 35 1 1700 2100 0 0"
    if line.startswith("aux 0"):
        return "aux 0 0 0 1700 2100 0 0"
    elif line.startswith("aux 1"):
        return "aux 1 1 1 1700 2100 0 0"
    elif line.startswith("aux 2"):
        return "aux 2 13 3 1700 2100 0 0"
    elif line.startswith("aux 3"):
        return "aux 3 35 2 1700 2100 0 0"
    return line


def new_file_name(file_name, video_system, receiver):
    prefix = file_name.split(" - ")[0]
    return f"{prefix} - {video_system} {receiver}.txt"


def new_file_content(file_contents, video_system, receiver, file_name):
    lines = file_contents.split("\n")
    modified_lines = []
    for line in lines:
        modified_line = new_video_system_lines(line, video_system, file_name)
        modified_line = new_receiver_lines(modified_line, receiver)
        modified_line = new_aux_lines(line, video_system, receiver)
        modified_line = new_name_line(
            modified_line, video_system, receiver, file_name)
        modified_lines.append(modified_line)
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
