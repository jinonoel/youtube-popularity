import random
import argparse
import sys
import math
import pymongo

sys.path.append('/Users/jino/Code/liblinear-1.94/python')
sys.path.append('/Users/jino/Code/YTPopularity/learning')
import liblinearutil
import evaluate


def predict_baseline(test_data, test_features):
    predictions = {}

    for vid in test_data:
        predictions[vid] = {
            'class': 1,
            'score' : test_features[vid][0]
        }

    return predictions

def cross_validate(data, features):
    print 'Getting folds'
    folds = get_folds(data)

    average_acc = 0
    average_pr100 = 0
    for i in range(5):
        print 'Fold', (i+1)
        
        test_data = folds[i]

        print "Predict"
        predictions = predict_baseline(test_data, test_features)

        print "Evaluate"
        score = evaluate_aprf(predictions, test_data)
        pr100 = evaluate_pr100(predictions, test_data)
        accr = score[0]

        #print score[1], score[2], score[3], score[4]
        print "Accuracy:", accr
        print "Pr@100:", pr100
        print

        average_acc += accr
        average_pr100 += pr100

    print "Average Accuracy:", average_acc / 5
    print "Average Pr@100:", average_pr100 / 5
