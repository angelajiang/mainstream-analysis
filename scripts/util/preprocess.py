
def op_to_layer(op_full):
    tensor_name = (op_full.split(":"))[0]
    layer = tensor_name.split("/")[0]
    return layer

def layer_to_number(layer, layers_info):

    layer_names = layers_info["layer_names"]
    for num, name in layer_names.iteritems():
        if op_to_layer(name) == layer:
            return num

    print "[Error] No layer %s found in layers info." % (layer)

def get_num_frozens(csv_file, layers_index, layers_info):
    layers = get_layers(csv_file, layers_index)
    return [layer_to_number(l, layers_info) for l in layers]

def get_layers(csv_file, layers_index):
    layers = []
    with open(csv_file) as f:
        for line in f:
            vals = line.split(',')
            op_full = vals[layers_index]
            layer = op_to_layer(op_full)
            if layer not in layers:
                layers.append(layer)
    return layers

def get_all_layers(csv_file):
    layers = []
    with open(csv_file) as f:
        for line in f:
            vals = line.split(',')
            op_full = vals[0]
            layer = op_to_layer(op_full)
            if layer not in layers:
                layers.append(layer)
    return layers

def get_num_NNs(csv_file):
    num_NNs = []
    with open(csv_file) as f:
        for line in f:
            vals = line.split(',')
            num_NN = int(vals[1])
            if num_NN not in num_NNs:
                num_NNs.append(num_NN)
    return num_NNs

