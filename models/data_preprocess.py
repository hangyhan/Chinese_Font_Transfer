# %%
# encoding=UTF-8
import numpy as np
import matplotlib as plt
from PIL import Image
import os


# %%
def data_preprocess(path='/Users/hangyizhe/GitHub/Chinese_Font_Transfer/Font2img/img_lib/',
                    source_font='heiti',
                    target_font='lixuke'):
    """
        normalize font images to [0,1] and then create the source-target font pairs
    """
    # load the condition font
    source_path = path+'/'+source_font
    source_fonts = list()
    files = os.listdir(source_path)
    mid = np.zeros((128, 128, 1))
    for file in files:
        img = Image.open(source_path+'/'+file)
        img = np.array(img)
        mid[:, :, 0] = img[:, :, 0]
        source_fonts.append(mid)
    source_fonts = np.array(source_fonts)
    source_fonts = source_fonts.astype(np.float32)
    source_fonts /= 255

    # load the label font
    target_path = path + '/' + target_font
    target_fonts = list()
    files = os.listdir(target_path)
    for file in files:
        img = Image.open(target_path + '/'+file)
        img = np.array(img)
        mid[:, :, 0] = img[:, :, 0]
        target_fonts.append(mid)
    target_fonts = np.array(target_fonts)
    target_fonts = target_fonts.astype(np.float32)
    target_fonts /= 255

    return source_fonts, target_fonts


'''img = Image.fromarray(  a[0][:128][:128][0] )
img.show()

b = np.zeros((128,128))
a[:,:,0].shape
a *= 255
img = Image.fromarray(  a )
img.show()'''

# %%


class Dataset:
    def __init__(self, source_fonts, target_fonts, test_frac=0.4, val_frac=0.3, shuffle=False, scale_func=None):
        """
            create the training set, validation set and testing set
        """
        self.data_num = int(len(source_fonts))
        self.val_num = int(self.data_num*(1-test_frac)*val_frac)
        self.train_num = int(self.data_num * (1 - test_frac)) - self.val_num

        self.train = {}
        self.test = {}
        self.valid = {}


        """self.train['source_font'] = np.rollaxis(
            source_fonts[:self.train_num], axis=3)
        self.valid['source_font'] = np.rollaxis(
            source_fonts[self.train_num: self.train_num+self.val_num], axis=3)
        self.test['source_font'] = np.rollaxis(
            source_fonts[self.train_num + self.val_num:], axis=3)

        self.train['target_font'] = np.rollaxis(
            target_fonts[:self.train_num], axis=3)
        self.valid['target_font'] = np.rollaxis(
            target_fonts[self.train_num: self.train_num+self.val_num], axis=3)
        self.test['target_font'] = np.rollaxis(
            target_fonts[self.train_num + self.val_num:], axis=3)"""

        self.train['source_font'] =source_fonts[:self.train_num]
        self.valid['source_font'] =source_fonts[self.train_num: self.train_num+self.val_num]
        self.test['source_font'] = source_fonts[self.train_num + self.val_num:]

        self.train['target_font'] =target_fonts[:self.train_num]
        self.valid['target_font'] =target_fonts[self.train_num: self.train_num+self.val_num]
        self.test['target_font'] =target_fonts[self.train_num + self.val_num:]

        self.shuffle = shuffle

    def get_batches(self, batch_size):
        """
            generate one batch of data
        """
        if self.shuffle:
            idx = np.arrange(len(self.train_num))
            np.random.shuffle(idx)
            self.train['source_font'], self.train['target_font'] = self.train['source_target'][idx], self.train['target_font'][idx]

        # n_batches = self.train_num // batch_size
        for ii in range(0, self.train_num, batch_size):
            source_font = self.train['source_font'][ii:ii+batch_size]
            target_font = self.train['target_font'][ii:ii+batch_size]

            yield source_font, target_font


# %%
source_fonts, target_fonts = data_preprocess()


# %%

dataset = Dataset( source_fonts, target_fonts)
print(dataset.train['source_font'].shape)

# 解决getbatches报错：'KeyValueError target_font'
# %%