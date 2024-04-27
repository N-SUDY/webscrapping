from os import makedirs
from os.path import basename
from requests import get
from bs4 import BeautifulSoup
from concurrent.futures import ThreadPoolExecutor, as_completed
from os.path import basename, join, exists
from pyrogram.types import InputMediaPhoto
from time import sleep
from modules.Client import ID_CHANNEL

class DownloadPhotos:
    def __init__(self, app, msg, url:str=None, folder:str="img") -> None:
        self.url = url
        self.app = app
        self.msg = msg
    
        
    def download_images(self, list_img:list, name:str):
        caption = name.replace('-', ' ')
        
        print(f"Descargando: {caption}\nCantidad de Imagenes: {len(list_img)}", flush=True)
        img_send = []
        with ThreadPoolExecutor() as executor:
            futuros = []
            for img in list_img:
                futuros.append(
                    executor.submit(self.download, img)
                )
            for futuro in as_completed(futuros):
                img_send.append(
                    InputMediaPhoto(futuro.result())
                )
                
        
        print("Enviando Imagenes...")
        sleep(5)
        ids = self.app.send_media_group(self.msg.chat.id, img_send[:10])
        self.app.copy_media_group(ID_CHANNEL, self.msg.chat.id, ids[0].id, captions=f"**{caption.capitalize()}**")
    
    
    def download(self, url):
        folder_path = "downloads"
        if not exists(folder_path):
            makedirs(folder_path)
        name:str = basename(url)
        name = name.replace('webp', 'jpeg')
        
        with open(join(folder_path, name), 'wb') as img:
            print(f"\33[1;32mDescargando: \33[35m{name}\33[0m", flush=True)
            img.write( get(url).content )
            return join(folder_path, name)
    
    
    def get_links(self, element):
        url = element.find('a').get('href')
        return url
    
    
    
    def get_images(self, url_page:str) -> list:
        list_img = []
        for element in self.get_soup(url_page).find(id='lightgallery'):
            link = str(element).split('<a href="')[-1].split('"')[0]
            if link.startswith('http'):
                list_img.append(link)
                
        return list_img
            
            
    def get_soup(self, url:str):
        response = get(url)
        if response.status_code == 200:
            return BeautifulSoup(response.content, 'html.parser')
        else:
            print(f"Error al obtener la página: {response.status_code}")
        
        
        
    def get_pages(self):
        elements = self.get_soup(self.url).find_all(class_='col-md-3 ajax-load')
        with ThreadPoolExecutor() as executor:
            futuros = []
            for element in elements:
                futuros.append( executor.submit(self.get_links, element) )

            for futuro in as_completed(futuros):
                enlace = futuro.result()
                name = basename(enlace)
                self.download_images( self.get_images( enlace ), name )
