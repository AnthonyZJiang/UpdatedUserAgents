import json
import logging


def write_local_UA(new_UA):
    with open('useragents.json', 'w') as f:
        json.dump(new_UA, f)
    logging.info('User agents updated.')


def update_local_UA(new_UA):
    print('\n\nNew UA found, update local UA file with the follow?\n')
    print(json.dumps(new_UA, indent=4, sort_keys=False))
    if input('\nY/N:').lower() == 'y':
        write_local_UA(new_UA)
    else:
        logging.info('User refused to update local UA file.')
        input('\n\nPress any key to exit...')
        exit()
