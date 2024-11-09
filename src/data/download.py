# -*- coding: utf-8 -*
from wrappers import *
from utils import compute_centers


def download_sent2(folder):
    CPC_USERNAME, CPC_PASSWORD = os.environ.get('CPC_USERNAME'), os.environ.get('CPC_PASSWORD')
    api = Sentinel2Downloader(CPC_USERNAME, CPC_PASSWORD)
    api.request_products()
    products = api.filter_products(sort_by=['cloudcoverpercentage', 'beginposition'], remove_offline=True)
    print(products[['title', 'cloudcoverpercentage']].to_string())

    api.download('342c57d0-bde8-4391-90f6-a4192ba47a14', folder)


def download_gmaps_api(places, folder='/content/drive/MyDrive/Deep-Learning-for-Solar-Panel-Recognition/src/data'):
    GMAPS_KEY = ''

    gmaps = GoogleMapsAPIDownloader(GMAPS_KEY)

    for name, coords in places.items():

        path = f'{folder}/{name}'
        centers = compute_centers(*coords)
        print(f'Number of tiles: {len(centers)*len(centers[0])} ({len(centers)}x{len(centers[0])})')

        gmaps.parallel_download_grid(
            centers, path,
            split=True,
            maptype='satellite',
            format='png',
            size=(1280, 1280),
            zoom=19, scale=2,
        )


def download_gmaps_web(places, folder='/content/drive/MyDrive/Deep-Learning-for-Solar-Panel-Recognition/src/data'):
    gmaps = GoogleMapsWebDownloader()

    for name, coords in places.items():

        path = f'{folder}/{name}'
        gmaps.download(
            *coords, folder=path,
            zoom=19, style='s', format='png'
        )

        # print('Merging tiles...')
        # gmaps.merge(f'{folder}/merged.png')


def main():
    folder = '/content/drive/MyDrive/Deep-Learning-for-Solar-Panel-Recognition/src/data'
    PLACES = {
        # 'mprincipe': [(40.4123, -3.854), (40.4054, -3.841)],
        # 'leganes': [(40.34, -3.778), (40.337, -3.77)]
        'IIT BHU final': [(25.2631, 82.9897), (25.2608, 82.9922)]
        # 'Karnataka farm1_main': [(13.0947, 78.2825), (13.0911, 78.2894)]
        # 'Karnataka farm2': [(13.0817, 78.2881), (13.0833, 78.2972)]

    }

    # download_sent2(folder)

    download_gmaps_api(PLACES, folder)

    # start_time = time.time()
    # download_gmaps_web(PLACES, folder)

    # final_time = time.time() - start_time
    # total_files = len(os.listdir(folder))
    # print(f'\nDownloaded files: {total_files}')
    # print(f'{total_files / final_time} files/second')
    # print(f'Elapsed time: {final_time}s')


if __name__ == '__main__':
    main()
