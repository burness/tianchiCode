__author__ = 'burness'
def compute_error(predict_labels, test_labels):
    error = abs(test_labels-predict_labels)/test_labels
    return error.mean()