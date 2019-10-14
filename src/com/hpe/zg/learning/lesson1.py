def x(d):
    d.append(1)


def merge_dict(d1, d2):
    merged = {}
    for k, v in d1.items():
        if d2.__contains__(k):
            merged[k] = [v, d2[k]]
        else:
            merged[k] = [v]
    for k, v in d2.items():
        if d1.__contains__(k):
            pass
        else:
            merged[k] = [v]
    return merged


if __name__ == '__main__':
    # for letter in 'Python':
    #     if letter == 'h':
    #         pass
    # print("this is pass block")
    #     # else:
    #     print('当前字母 :', letter)
    # w = {}
    # w['a'] = 1
    a = {}
    a['a_b'] = 1
    t = [2]
    x(t)

    d1 = {'a': [1, 2], 'b': [4]}
    d2 = {'a': [2, 3], 'd': [5]}

    print([d1['a']] + [d2.get('e')])

    print(merge_dict(d1, d2))
# print(w)
# print("Good bye!")
