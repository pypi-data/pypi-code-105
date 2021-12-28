def parse_adrn(adrn):
    rn_list = adrn.split(":")
    try:
        srv_name = rn_list[2]
    except:
        raise Exception("parsing adrn failed! adrn: {}".format(adrn))
    if srv_name in ["data-set", "data-item", "dataset-anno", "data-file"]:
        pass
    else:
        raise Exception("Invalid resource name segment in adrn! adrn: {}".format(adrn))

    index = -1
    if srv_name in ["data-item", "data-file"]:
        try:
            index = rn_list[8]
        except:
            raise Exception("parsing adrn failed! has no index segment. adrn: {}".format(adrn))

    try:
        protocol_name, _, _, _, project_name, res_name, res_type, res_version = rn_list[:8]
    except:
        raise Exception("parsing adrn failed! adrn: {}".format(adrn))

    if protocol_name in ["adrn", "mrn", "adr"]:
        pass
    else:
        raise Exception("Invalid adrn! adrn: {}".format(adrn))

    if project_name:
        pass
    else:
        raise Exception("project_name or teamid or orgid is null in adrn! adrn: {}".format(adrn))

    return srv_name, project_name, res_name, res_type, res_version, index


def get_dataset_name_version_from_adrn(adrn):
    srv_name, _, name, _, version,_ = parse_adrn(adrn)
    return srv_name, name, version


def get_item_index_from_adrn(adrn):
    index = -1
    _, _, _, _, _, index = parse_adrn(adrn)
    if index == -1 or index == '':
        raise Exception("adrn has no index segment!  adrn: {}".format(adrn))
    return index

def get_owerid_from_adrn(adrn):
    _, owner, _, _, _, _ = parse_adrn(adrn)
    return owner