#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sqlparse
from sqlparse.sql import Parenthesis, Comparison, Identifier, Where

def remove_duplication(l):
    list1 = []  # 创建一个新的数组来存储无重复元素的数组
    for element in l:
        if element not in list1:
            list1.append(element)
    return list1


def merge_dict(d1, d2):
    merged = {}
    for k, v in d1.items():
        if d2.__contains__(k):
            merged[k] = v + d2[k]
        else:
            merged[k] = v
    for k, v in d2.items():
        if d1.__contains__(k):
            pass
        else:
            merged[k] = v
    return merged

def test(sql):
    # s = sqlparse.format(sql, encoding=None)
    # print(s)
    parsed = sqlparse.parse(sql)
    print(sqlparse.sql.Statement(parsed[0]).get_type())


def o(sql):
    s0 = sqlparse.parse(sql)
    for t in s0[0].tokens:
        print(type(t), t.ttype, t.value)


def deal(field):
    if '(' in field:
        li = field.find('(')
        ri = field.find(')')
        return field[li + 1:ri].lstrip().rstrip()
    else:
        return field


def append_field(fields, dim, f):
    if fields.__contains__(dim):
        fields[dim].append(deal(list(f.keys())[0]))
    else:
        fields[dim] = [deal(list(f.keys())[0])]


def output_field(fields, dim, f):
    if len(f.keys()) > 0:
        # print(f)
        append_field(fields, dim, f)


def parse_where(token, dim, fields):
    f = {}
    k = None

    for t in filter(lambda x: not x.is_whitespace, token.tokens):
        if isinstance(t, Parenthesis):
            output_field(fields, dim, f)
            f = {}
            sub = t.value[1:len(t.value) - 1].lstrip().rstrip()
            # print("a", sub)
            if not sub.startswith('select'):
                sub = 'where ' + sub
            parse(sub, fields, dim)
        elif t.value.lower() == "where":
            pass
        elif isinstance(t, Comparison):
            output_field(fields, dim, f)
            f = {}
            st = list(filter(lambda x: not x.is_whitespace, t.tokens))
            f[st[0].value] = [st[1].value]
            k = st[0].value
        elif isinstance(t, Identifier):
            output_field(fields, dim, f)
            f = {}
            f[t.value] = []
            k = t.value
        elif t.is_keyword:
            if k is not None:
                f[k].append(t.value)
        else:
            pass
    output_field(fields, dim, f)


def _get_dimension(dim):
    if dim is not None and ' ' in dim:
        return dim.split(' ')[1]
    else:
        return dim


def get_dimension(parsed_item):
    get_dim_name = lambda dim: dim.split(' ')[1] if dim is not None and ' ' in dim else dim
    sql_type = sqlparse.sql.Statement(parsed_item).get_type()
    if sql_type in ['SELECT', 'DELETE']:
        after_from = False
        for token in parsed_item.tokens:
            if token.is_keyword and token.value.lower() == 'from':
                after_from = True
            elif isinstance(token, Identifier) and after_from:
                return get_dim_name(token.value)
            else:
                pass
        return None
    elif sql_type == 'UPDATE':
        for token in parsed_item.tokens:
            if isinstance(token, Identifier):
                return get_dim_name(token.value)
            else:
                pass
        return None
    else:
        return None


def parse(sql, fields, dimension=None):
    parsed = sqlparse.parse(sql)

    if not parsed:
        print("Failed to parse the input string")
        return ()
    # sql_type = sqlparse.sql.Statement(parsed[0]).get_type()
    # print("SQL Type: ", sql_type)
    # if sql_type in 'SELECT':
    #     print("Only for SELECT sql statement now")
    #     return ()
    if dimension is None:
        dimension = get_dimension(parsed[0])

    for token in parsed[0].tokens:
        if isinstance(token, Where) and dimension is not None:
            parse_where(token, dimension, fields)
        elif isinstance(token, Parenthesis):
            sub = token.value[1:len(token.value) - 1].lstrip().rstrip()
            parse(sub, fields, dimension)
        else:
            pass


if __name__ == '__main__':

    sql0 = "select x from ab A  where ab.b in (select b from bb B where bb.c>1) and ab.x!=1 order by ab.x;"
    sql1 = '''
    SELECT identifier 
    FROM T A 
    WHERE a is not null and (state= 'Outstanding' and additional_text like '%Critical%' escape '^' or fun(identifier)=2
    and event_time>0 and event_time<1234456677) 
    ORDER BY  event_time DESC ,  alarmIdentifier DESC ,  identifier DESC LIMIT 0 , 500;
    '''
    sql2 = '''
        select a from (select a from A where (b>0) where c>2 group by a limit 1,2)
    '''
    sql3 = '''
    update A set x=1 where x in (select x, y from A where x<y)
    '''
    sql4 = '''
    delete from A where x>1 and y in (select x, y ,z from A where x>z)
    '''
    sql_array = [sql1, sql2, sql3, sql4]
    ss = sql4
    # o(ss)
    # parse(ss, result)
    # print("***********************")
    # print(result)
    # o("""select a from b where state = 'Outstanding' and additional_text like '%Critical%' escape '^'""")
    # test(sql1)

    result = {}
    result1 = {}
    merged = {}
    for sc in sql_array:
        parse(sc, result1)
        for k, v in result1.items():
            result[k] = [remove_duplication(v)]
        merged = merge_dict(merged,  result)
        result = {}
        result1 = {}
    print(merged)
