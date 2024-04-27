from modules.Client import app
from modules.DownloadPhotos import DownloadPhotos
from pyrogram import filters


@app.on_message(filters.command("start"))
def command_start(app, msg):
    msg.reply("Hola")


@app.on_message(filters.command("run"))
def upload_images(app, msg):
    pagina = 1
    DownloadPhotos(app, msg, f'https://hentaidad.com/popular/{pagina}').get_pages()

@app.on_message()
def ver_id(app, msg):
    msg.reply( f'`{msg.chat.id}`' )
    

if __name__ == '__main__':
    print("BOT INICIADO")
    app.run()
