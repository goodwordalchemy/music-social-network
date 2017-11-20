from . import json_cache
from . import populate_db


def main():
    json_cache.main()
    populate_db.main()


if __name__ == '__main__':
    main()
