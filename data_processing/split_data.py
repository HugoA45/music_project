import numpy as np

def load(task, sub_task=None):

    data_root = '/root/code/HugoA45/music_project/music_project/data/'

    if task == 'composer':
        X_train = np.load(data_root + 'emopia/emopia_cp_train.npy')
        X_test = np.load(data_root + 'emopia/emopia_cp_test.npy')
        X_valid = np.load(data_root + 'emopia/emopia_cp_valid.npy')

        data = {
                'X_train' : X_train,
                'X_test' : X_test,
                'X_valid' : X_valid
                }

        if sub_task == 'classification':
            y_train = np.load(data_root + 'emopia/emopia_cp_train_ans.npy')
            y_test = np.load(data_root + 'emopia/emopia_cp_test_ans.npy')
            y_valid = np.load(data_root + 'emopia/emopia_cp_valid_ans.npy')

            data =  {
                    'X_train' : X_train,
                    'X_test' : X_test,
                    'X_valid' : X_valid,
                    'y_train' : y_train,
                    'y_test' : y_test,
                    'y_valid' : y_valid
                    }

    return data
