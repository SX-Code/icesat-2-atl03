import numpy as np


def ismember(a_vec, b_vec, method_type='normal'):
    """ MATLAB equivalent ismember function """
    #  Function to determine members of one array in another
    # Combine multi column arrays into a 1-D array of strings if necessary
    # This will ensure unique rows when using np.isin below
    if (method_type.lower() == 'rows'):

        # Turn a_vec into an array of strings
        a_str = a_vec.astype('str')
        b_str = b_vec.astype('str')

        # Concatenate each column of strings with commas into a 1-D array of strings
        for i in range(0, np.shape(a_str)[1]):
            a_char = np.char.array(a_str[:, i])
            b_char = np.char.array(b_str[:, i])
            if (i == 0):
                a_vec = a_char
                b_vec = b_char
            else:
                a_vec = a_vec + ',' + a_char
                b_vec = b_vec + ',' + b_char

    matchingTF = np.isin(a_vec, b_vec)
    common = a_vec[matchingTF]
    common_unique, common_inv = np.unique(common, return_inverse=True)  # common = common_unique[common_inv]
    b_unique, b_ind = np.unique(b_vec, return_index=True)  # b_unique = b_vec[b_ind]
    common_ind = b_ind[np.isin(b_unique, common_unique, assume_unique=True)]
    matchingInds = common_ind[common_inv]

    return matchingTF, matchingInds
