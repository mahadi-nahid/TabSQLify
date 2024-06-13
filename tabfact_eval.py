def main():

    import json

    # filename = "outputs/tabfact_col_nov12_B.jsonl"
    filename ="outputs/tabfact_rc_nov12_A.jsonl"
    # filename = "outputs/TabFact_Full_Coll_2.json"
    # filename = "outputs/tf_50_plus_rc.jsonl"

    print('Start', filename)
    correct = 0
    wrong = 0
    sample = 0

    with open(filename, 'r') as f:
        for line in f:
            output = json.loads(line)
            if 'response' in output:
                # pred_answer = output['prediction']
                response = output['response']
                label = output['label']
                # print(pred_answer,target_values, type(pred_answer), type(target_values))

                # if 'not possible to verify' in response:
                #     predict = 2
                # if 'cannot be verified' in response:
                #     predict = 2
                # elif 'no information' in response:
                #     predict = 2
                # elif 'cannot be determined' in response:
                #     predict = 2
                if 'true' in response:
                    predict = 1
                elif 'false' in response:
                    predict = 0
                elif 'support' in response:
                    predict = 1
                else:
                    predict = 0

                if predict == label:
                    correct += 1
                else:
                    wrong += 1
                    print('sample#:', sample, output['key'], predict, label)
            else:
                continue
            sample += 1

            if sample % 100 == 0:
                print('Accuracy', correct / (correct + wrong))
                print('Corect: ', correct, 'Wrong: ', wrong, "Total: ", (correct + wrong))

    print('Accuracy', correct / (correct + wrong))
    print('Corect: ', correct, 'Wrong: ', wrong, "Total: ", (correct+wrong))

if __name__ == '__main__':
    main()

