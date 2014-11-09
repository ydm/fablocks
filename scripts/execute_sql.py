#!/usr/bin/env python3

import dj_database_url
import psycopg2


def read_input():
    lines = []
    while 1:
        try:
            line = input()
        except EOFError:
            break
        else:
            lines.append(line)
    inp = '\n'.join(lines)
    return inp


def main():
    config = dj_database_url.config()
    conn = psycopg2.connect(
        database=config['NAME'],
        user=config['USER'],
        password=config['PASSWORD'],
        host=config['HOST'],
        port=config['PORT']
    )
    cur = conn.cursor()
    conn.autocommit = True

    inp = read_input()
    cur.execute(inp)

    # hasattr(cur, 'commit') and cur.commit()
    cur.close()
    conn.close()


if __name__ == '__main__':
    main()
