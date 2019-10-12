#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sqlparse
from sqlparse.sql import Parenthesis, Comparison, Identifier, Where


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


def get_dimension(dim):
    if dim is not None and ' ' in dim:
        return dim.split(' ')[1]
    else:
        return dim


def output_field(fields, dim, f):
    if len(f.keys()) > 0:
        print(f)
        append_field(fields, dim, f)


def append_field(fields, dim, f):
    if fields.__contains__(dim):
        fields[dim].append(deal(list(f.keys())[0]))
    else:
        fields[dim] = [deal(list(f.keys())[0])]


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


def parse(sql, fields, dimension=None):
    parsed = sqlparse.parse(sql)

    if not parsed:
        print("Failed to parse the input string")
        return ()
    sql_type = sqlparse.sql.Statement(parsed[0]).get_type()
    print("SQL Type: ", sql_type)
    # if sql_type in 'SELECT':
    #     print("Only for SELECT sql statement now")
    #     return ()

    after_from = False
    for token in parsed[0].tokens:
        if token.is_keyword and token.value.lower() == 'from':
            after_from = True
        elif isinstance(token, Where) and dimension is not None:
            parse_where(token, dimension, fields)
        elif isinstance(token, Identifier) and after_from:
            dimension = get_dimension(token.value)
            after_from = False
        elif isinstance(token, Parenthesis):
            sub = token.value[1:len(token.value) - 1].lstrip().rstrip()
            parse(sub, fields)
        else:
            pass


if __name__ == '__main__':
    result = {}
    sql0 = "select x from ab A  where ab.b in (select b from bb B where bb.c>1) and ab.x!=1 order by ab.x;"
    sql1 = '''
    SELECT identifier 
    FROM T temip_alarm 
    WHERE a is not null and (state= 'Outstanding' and additional_text like '%Critical%' escape '^' or fun(identifier)=2
    and event_time>0 and event_time<1234456677) 
    ORDER BY  event_time DESC ,  alarmIdentifier DESC ,  identifier DESC LIMIT 0 , 500;
    '''
    sql2 = '''
        select a from (select a from A where (b>0) group by a limit 1,2)
    '''
    # o(sql2)
    parse(sql1, result)
    print(result)
    # o("""select a from b where state = 'Outstanding' and additional_text like '%Critical%' escape '^'""")
    # test(sql1)
