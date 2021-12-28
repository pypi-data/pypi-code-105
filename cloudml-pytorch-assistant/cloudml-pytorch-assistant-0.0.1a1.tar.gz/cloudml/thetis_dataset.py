try:
    from torch.utils.data import DataSet
except ImportError:
    print("torch not installed!")
    class DataSet(object):
        pass


from cloudml.adrn_dataset import ThetisAdrnDataSet
from cloudml.dataset_srv_stub import gen_visit_stub_from_adrn

class ThetisDataSet(DataSet):

    def __init__(self, adrn, img_dir, transform=None, target_transform=None):
        img_dir = img_dir
        stub = gen_visit_stub_from_adrn(adrn)
        self.adrn_dataset = ThetisAdrnDataSet(adrn, stub)
        self.transform = transform
        self.target_transform = target_transform

    def __len__(self):
        return len(self.adrn_dataset.item_list())

    def __getitem__(self, idx):
        label, image = self.adrn_dataset.get_label_and_content(idx)  
        if self.transform:
            image = self.transform(image)
        if self.target_transform:
            label = self.target_transform(label)
        return image, label