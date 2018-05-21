from collections import namedtuple
import itertools
import os
import warnings
import pandas as pd


# dataset: [cars, ..]
# architecture: ['inception', 'mobilenets', ..]
# source: [None, 'iii']
MPackage = namedtuple('MPackage', ['dataset', 'architecture', 'source', 'accuracies', 'label'])
MPackage.__new__.__defaults__ = (None, ) * len(MPackage._fields)
MPackage.__repr__ = lambda self: "MPackage(label={}, source={}, len={})".format(self.label, self.source, len(self.accuracies))
ACCURACIES_DIR = "../pre-2018-Spring/" + "output/mainstream/accuracy"

dataset_labels = {
    'redcar': 'Red-Car',
}

architecture_labels = {
    'mobilenets': 'MobileNets-224',
    'resnet': 'ResNets50',
    'inception': 'InceptionV3',
}


def load(filename):
    return pd.read_csv(filename, names=['num_frozen', 'acc', 'acc_inv'], index_col=0)


def ex(filename_fmt, accuracies_dir=ACCURACIES_DIR, **kwargs):
    for k, v in kwargs.items():
        if not isinstance(v, list):
            kwargs[k] = [v]
    keys, vals = zip(*kwargs.items())
    ret = []
    for comb in itertools.product(*vals):
        dct = dict(zip(keys, comb))
        dct['label'] = dataset_labels.get(dct['dataset'], dct['dataset'].capitalize()) + '-' + architecture_labels[dct['architecture']]
        filename = os.path.join(accuracies_dir, filename_fmt.format(**dct))
        if os.path.exists(filename):
            dct['accuracies'] = load(filename)
            ret.append(MPackage(**dct))
    return ret


def all_packages():
    packages = []
    packages += ex("{source}/{dataset}/{source}-{dataset}-accuracy",
                   source="iii",
                   architecture="mobilenets",
                   dataset=["redcar", "scramble", "bus", "schoolbus"])

    packages += ex("{dataset}/{source}/{source}-{architecture}-accuracy",
                   source="atrium",
                   architecture="mobilenets",
                   dataset="pedestrian")

    packages += ex("{dataset}/{dataset}-easy/{dataset}-easy-{architecture}",
                   architecture="mobilenets",
                   dataset="trains")

    packages += ex("{dataset}/{architecture}/{dataset}-40-0.0001",
                   architecture="mobilenets",
                   dataset="flowers")

    packages += ex("{dataset}/{dataset}-{source}-{architecture}-accuracy",
                   architecture="mobilenets",
                   dataset="cars",
                   source="stanford")

    packages += ex("{dataset}/{dataset}-{architecture}-accuracy",
                   architecture="mobilenets",
                   dataset="cats")

    packages += ex("{source}/{dataset}/{source}-{dataset}-{architecture}-accuracy",
                   source="iii",
                   architecture=["inception", "resnet"],
                   dataset=["redcar", "scramble", "bus", "schoolbus"])

    packages += ex("{dataset}/{dataset}-{architecture}-accuracy",
                   architecture="resnet",
                   dataset="cars",
                   source="stanford")

    return packages


def filter(**selectors):
    packages = all_packages()
    for k, v in selectors.items():
        if not isinstance(v, list):
            v = [v]
        packages = [pack for pack in packages if getattr(pack, k) in v]
    for pack in packages:
        if len(pack.accuracies) == 0:
            warnings.warn("Package " + pack.label + " is empty")
    return packages
